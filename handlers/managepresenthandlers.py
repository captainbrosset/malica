from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp

from model.present import Present, PresentCounter
import utils
import base
from util.gaesessions import get_current_session

# AddPresent request handler
# Adds a present for the current user in the model
class Add(base.BaseHandler):
	#@base.requires_user_access
	def get(self):
		session = get_current_session()
		if session.is_active():
			data = utils.prepare_base_template_values(self)

			self.writeTemplateToResponse('pages/Add.html', data)
		else:
			self.redirect('/?msg=needToBeLoggedToAdd')
			
	#@base.requires_user_access
	def post(self):
		session = get_current_session()
		if session.is_active() and self.request.get('title'):
			present = Present(title=self.request.get('title'), user=session["user_info"]["username"])
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
				counter = PresentCounter.all().fetch(1)[0]
			except:
				counter = PresentCounter(count=0)
			counter.count += 1
			counter.put()
			
		self.redirect('/?msg=addOk')
	

# DeletePresent request handler
# Deletes a present for the current user in the model, given its unique key
class Delete(base.BaseHandler):
	#@base.requires_user_access
	def get(self):
		session = get_current_session()
		if session.is_active():
			present = Present.get(self.request.get('key'))
			if present.user == session["user_info"]["username"]:
				present.delete();
				#increment counter
				counter = PresentCounter.all().fetch(1)[0]
				counter.count -= 1
				counter.put()
		self.redirect('/?msg=deleteOk')