from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import handlers
import logging

handlerMapping = [
	('/ajouter', handlers.AddPresent),
	('/effacer', handlers.DeletePresent),
	('/json_getInfoFromUrl', handlers.GetInfoFromUrl),
	('/([^/]+)', handlers.List),
	('/', handlers.Home)
]

webapp.template.register_template_library('templatetags.templateFilters')

application = webapp.WSGIApplication(handlerMapping, debug=True)

def main():
	logging.getLogger().setLevel(logging.DEBUG)
	run_wsgi_app(application)

if __name__ == "__main__":
    main()