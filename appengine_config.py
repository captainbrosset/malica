import os

from util.gaesessions import SessionMiddleware

def webapp_add_wsgi_middleware(app):
	# The cookie key will be different everytime the app is deployed, which means existing sessions will be lost.
	# This is not a big problem for now, and at least avoids sharing the secret with everyone on github
	app = SessionMiddleware(app, cookie_key=os.urandom(64))
	return app