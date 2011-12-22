from urlparse import urlparse

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users

import utils
from model.present import Present
import base
from util.gaesessions import get_current_session

# Home handler, shows main page when not logged in, list when logged in
class Home(base.BaseHandler):
	def get(self):
		# Show some presents on the home page
		data = utils.prepare_base_template_values(self)
		data['presents'] = utils.prepare_present_list_for_template(Present.all().order("-dateAdded").fetch(12))

		self.writeTemplateToResponse('pages/Home.html', data)

# List request handler
# Lists the presents of the current user if any
class List(base.BaseHandler):
    def get(self, username):
		data = utils.prepare_base_template_values(self)

		if utils.is_username_in_datamodel(username):
			sort = utils.get_current_sort(self.request.get("sort"))

			presentsAndPages = utils.get_presents_and_pages(username, sort)
			data.update(presentsAndPages)
			data['currentSort'] = sort
			data['sortUrls'] = utils.get_current_sort_urls(sort)
			data['isLoggedIn'] = False

			session = get_current_session()
			if session.is_active():
				# get the public user list URL
				o = urlparse(self.request.url)
				data['isLoggedIn'] = True
				data['userPublicUrl'] = o.scheme + "://" + o.netloc + o.path + "/" + username

			self.writeTemplateToResponse('pages/List.html', data)

		else:
			self.writeTemplateToResponse('pages/ListNotFound.html', data)