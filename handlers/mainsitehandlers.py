from urlparse import urlparse

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users

import utils
import datamodel

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