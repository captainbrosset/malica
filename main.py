from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import handlers
import utils
import logging

handlerMapping = [
	('/ajouter', handlers.AddPresent),
	('/effacer', handlers.DeletePresent),
	('/json_getInfoFromUrl', handlers.GetInfoFromUrl),
	('/([^/]+)', handlers.List),
	('/', handlers.Home)
]

# adding cron job handlers (not depending on the user agent)
#handlerMapping.append(('/fixImage404Errors', handlers.FixImage404Errors))
#handlerMapping.append(('/sendReportEmail', handlers.SendReportEmail))
#handlerMapping.append(('/_ah/xmpp/message/chat/', handlers.XmppHandler))
#handlerMapping.append(('/quickAdd', handlers.QuickAddWhenLoggedIn))

webapp.template.register_template_library('templatetags.templateFilters')

application = webapp.WSGIApplication(handlerMapping, debug=True)

def main():
	logging.getLogger().setLevel(logging.DEBUG)
	run_wsgi_app(application)

if __name__ == "__main__":
    main()