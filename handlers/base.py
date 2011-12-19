import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class BaseHandler(webapp.RequestHandler):
	def writeTemplateToResponse(self, tpl, data):
		path = os.path.join(os.path.dirname(__file__), "../templates/" + tpl)
		self.response.out.write(template.render(path, data))