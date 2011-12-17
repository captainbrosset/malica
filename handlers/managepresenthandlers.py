from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp

import datamodel
import utils

# AddPresent request handler
# Adds a present for the current user in the model
class Add(webapp.RequestHandler):
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
	

# DeletePresent request handler
# Deletes a present for the current user in the model, given its unique key
class Delete(webapp.RequestHandler):
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