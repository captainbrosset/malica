import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from util.gaesessions import get_current_session

def requires_user_access(obj):
	session = get_current_session()
	if session.is_active() and session.has_key("user_info"):
		return obj
	else:
		return obj

class BaseHandler(webapp.RequestHandler):
	def writeTemplateToResponse(self, tpl, data):
		path = os.path.join(os.path.dirname(__file__), "../templates/" + tpl)
		self.response.out.write(template.render(path, data))