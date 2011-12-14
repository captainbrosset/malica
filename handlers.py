from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import xmpp_handlers
from google.appengine.ext import db
from django.utils import simplejson
from urlparse import urlparse
from google.appengine.api import mail
import datamodel
import utils
import urllib2
import datetime
import logging
import random

# Home handler, shows main page when not logged in, list when logged in
class Home(webapp.RequestHandler):
	def get(self):
		# Show some presents on the home page
		data = utils.prepare_base_template_values(self)
		data['presents'] = utils.prepare_present_list_for_template(datamodel.Present.all().order("-dateAdded").fetch(12))
		path = utils.get_template_path('templates/pages/Home.html')
		self.response.out.write(template.render(path, data))
			
# List request handler
# Lists the presents of the current user if any
class List(webapp.RequestHandler):
    def get(self, email):
		email = email.replace("%40", "@")
		data = utils.prepare_base_template_values(self)
		
		if utils.is_email_in_datamodel(email):
			sort = utils.get_current_sort(self.request.get("sort"))

			presentsAndPages = utils.get_presents_and_pages(users.User(email), sort)
			data.update(presentsAndPages)
			data['currentSort'] = sort
			data['sortUrls'] = utils.get_current_sort_urls(sort)
			data['isLoggedIn'] = False
			data['currentListEmail'] = email

			if users.get_current_user():
				# get the public user list URL
				o = urlparse(self.request.url)
				data['isLoggedIn'] = True
				data['userPublicUrl'] = o.scheme + "://" + o.netloc + o.path + "/" + users.get_current_user().email()

			path = utils.get_template_path('templates/pages/List.html')
			self.response.out.write(template.render(path, data))
		
		else:
			path = utils.get_template_path('templates/pages/ListNotFound.html')
			self.response.out.write(template.render(path, data))


# Handler called by the cron job to send statistics email
class SendReportEmail(webapp.RequestHandler):
	def get(self):
		# get all presents added this week
		lastWeek = datetime.datetime.today() + datetime.timedelta(weeks = -1)
		presents = datamodel.Present.all().filter("dateAdded >= ", lastWeek).fetch(100)
		out = "Weekly malica report\n"
		out = "(There are " + str(datamodel.PresentCounter.all().fetch(1)[0].count) + " presents in the datastore)\n"
		for p in presents:
			out += "  - " + p.user.email() + " added on " + p.dateAdded.ctime() + " present: " + p.title + "\n"
		
		mail.send_mail(sender="patrickbrosset@gmail.com",
		              to="patrickbrosset@gmail.com",
		              subject="weekly stats",
		              body=out)
		
		self.response.out.write("done")


# Handler called by the cron job to fix 404 images
class FixImage404Errors(webapp.RequestHandler):
	def get(self):
		# Get a number of images to fix
		query = datamodel.Present.all().filter("imageFixed = ", False)
		presents = query.fetch(10)
		
		out = ""
		for p in presents:
			if p.image:
				out += "fixing " + str(p) + " ...<br/>"
				try:
					req = urllib2.urlopen(p.image)
				except:
					out += "fixed broken image " + str(p.image)
					p.image = ""
				out += "<hr />"
				p.imageFixed = True	
				p.put()
		
		self.response.out.write(out)
		

# Same as SearchUser handler below, except it is called via /liste/<userid>[/<pageNb>]
class UserPublicPage(webapp.RequestHandler):
	def get(self, user):
		# TODO: there's probably a better way to do this ...
		user = user.replace("%40", "@")
		data = utils.prepare_base_template_values(self)
		searched_user = users.User(user)
		if searched_user == users.get_current_user():
			self.redirect('/?msg=searchedUserIsYou')
		
		sort = utils.get_current_sort(self.request.get("sort"))
		
		presentsAndPages = utils.get_presents_and_pages(searched_user, sort)
		data.update(presentsAndPages)
		data['currentSort'] = sort
		data['sortUrls'] = utils.get_current_sort_urls(sort, searched_user.email())
		
		if len(data['presents']) == 0:
			self.redirect("/?msg=userNotFound-" + user);
		
		data['searched_user'] = searched_user.email()
		path = utils.get_template_path('templates/searchUser.html')
		self.response.out.write(template.render(path, data))
	

# AddPresent request handler
# Adds a present for the current user in the model
class AddPresent(webapp.RequestHandler):
	def get(self):
		if users.get_current_user():
			data = utils.prepare_base_template_values(self)
			self.response.out.write(template.render('templates/pages/Add.html', data))
		else:
			self.redirect('/?msg=needToBeLoggedToAdd')
	def post(self):
		if users.get_current_user() and self.request.get('title'):
			present = datamodel.Present(title=self.request.get('title'), user=users.get_current_user())
			if self.request.get('approximatePrice'):
				present.approximatePrice = int(self.request.get('approximatePrice'))
			if self.request.get('url'):
				present.url = self.request.get('url')
			if self.request.get('image'):
				present.image = self.request.get('image')
			present.imageFixed = False
			present.put()
			
			#increment counter
			try:
				counter = datamodel.PresentCounter.all().fetch(1)[0]
			except:
				counter = datamodel.PresentCounter(count=0)
			counter.count += 1
			counter.put()
			
		self.redirect('/?msg=addOk')
	

# GetInfoFromUrl request handler
# Called through XHR request to return a list of images corresponding to the given URL as json array, and the title of the page
class GetInfoFromUrl(webapp.RequestHandler):
	def get(self):
		if self.request.get('url'):
			info = utils.get_image_urls_and_title_from_page(self.request.get('url'))
			if info:
				data = simplejson.dumps(info)
			else:
				data = simplejson.dumps({})
		else:
			data = simplejson.dumps({})
		self.response.out.write(data)
	

# DeletePresent request handler
# Deletes a present for the current user in the model, given its unique key
class DeletePresent(webapp.RequestHandler):
	def get(self):
		if users.get_current_user():
			present = datamodel.Present.get(self.request.get('key'))
			if present.user == users.get_current_user():
				present.delete();
				#increment counter
				counter = datamodel.PresentCounter.all().fetch(1)[0]
				counter.count -= 1
				counter.put()
		self.redirect('/?msg=deleteOk')


# XMPP handler to add presents through googleTalk/jabber
class XmppHandler(xmpp_handlers.CommandHandler):
	def text_message(self, message=None):
		email = message.sender.split("/")[0]
		if message.arg == "bonjour":
			message.reply("Bonjour " + email + ". Veuillez tapper une adresse de site internet pour ajouter un cadeau a votre liste")
		elif message.arg == "bite":
			r = random.Random()
			nb = r.choice((2,3,4,5,6,7))
			str = "c"
			i = 1
			while i <= nb:
				str += "="
				i += 1
			str += "3"
			message.reply(str)
		else:
			self.ajouter_command(message)
	def ajouter_command(self, message=None):
		#who = db.IM("xmpp", message.sender)
		url = message.arg
		logging.debug('Wants to add present from URL ' + url)
		data = {
			"isAdded": False
		}
		email = message.sender.split("/")[0]
		logging.debug('XMPP handler started via /ajouter command. User ' + email + ". URL: " + url)
		try:
			info = utils.get_image_urls_and_title_from_page(url)
			if info['title']:
				present = datamodel.Present(title=info['title'], user=users.User(email))
				present.approximatePrice = int(info['price'])
				present.url = url
				# We're going to have to choose the first image anyway ...
				present.image = info['img'][0]
				present.imageFixed = False
				present.put()
				
				data["isAdded"] = True
				data["present"] = present
			else:
				data["error"] = "Could not parse website"
		except StandardError, e:
			data["error"] = e
		message.reply(template.render('templates/chatReplies.html', data))


class QuickAddWhenLoggedIn(webapp.RequestHandler):
	"""
	var img = document.createElement("img");
	var url = encodeURIComponent(document.location.href)
	img.style.display = "none";
	document.body.appendChild(img);
	img.src = "http://malistedecadeaux.appspot.com/quickAdd?site="+url
	"""
	def get(self):
		if users.get_current_user():			
			url = urllib2.unquote(self.request.get('site'))
			try:
				info = utils.get_image_urls_and_title_from_page(url)
				if info['title']:
					present = datamodel.Present(title=info['title'], user=users.get_current_user())
					present.approximatePrice = int(info['price'])
					present.url = url
					# We're going to have to choose the first image anyway ...
					present.image = info['img'][0]
					present.imageFixed = False
					present.put()
					self.response.out.write("OK -- " + url)
				else:
					self.response.out.write("KO -- no title extracted")
			except StandardError, e:
				self.response.out.write("KO -- error parsing")
		else:
			self.response.out.write("KO -- not logged in")