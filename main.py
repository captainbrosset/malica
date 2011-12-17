import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from handlers import specialhandlers
from handlers import mainsitehandlers
from handlers import managepresenthandlers

handlerMapping = [
	('/_ah/xmpp/message/chat/', specialhandlers.XmppHandler),
	('/ajouter', managepresenthandlers.Add),
	('/effacer', managepresenthandlers.Delete),
	('/json_getInfoFromUrl', specialhandlers.GetInfoFromUrl),
	('/([^/]+)', mainsitehandlers.List),
	('/', mainsitehandlers.Home)
]

webapp.template.register_template_library('templatetags.templateFilters')

application = webapp.WSGIApplication(handlerMapping, debug=True)

def main():
	logging.getLogger().setLevel(logging.DEBUG)
	run_wsgi_app(application)

if __name__ == "__main__":
    main()