import random
import logging

from google.appengine.ext import webapp
from django.utils import simplejson
from google.appengine.ext.webapp import xmpp_handlers
from google.appengine.ext.webapp import template
from google.appengine.api import users

import utils
import datamodel

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