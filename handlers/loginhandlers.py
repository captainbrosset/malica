from util import oauth
import base
from util.gaesessions import get_current_session

class OAuthTwitterLogin(base.BaseHandler):
	
	OAUTH_KEY = "JaqkgrUjbEtXJyX3dzjg"
	OAUTH_SECRET = "97NcAG8P24sge05QXzEy3kC8HXGdUmPgjAPf4KbXNU"
	API_KEY = "17022950-dGANUb4svlucDN6kkLCMvxpqbKoWaOQyiTFzpNexa"
	API_SECRET = "sfEtVuv4aZcV0VnxegUHndTGdrTbELKfrm0wLgVuQ"
	CALLBACK_URL = "http://localhost:8080/connect/twitter/response"
	
	def get(self, mode=""):
		client = oauth.TwitterClient(OAuthTwitterLogin.OAUTH_KEY, OAuthTwitterLogin.OAUTH_SECRET, OAuthTwitterLogin.CALLBACK_URL)
		
		if mode == "request":			
			self.redirect(client.get_authorization_url())
			
		if mode == "response":
			auth_token = self.request.get("oauth_token")
			auth_verifier = self.request.get("oauth_verifier")
			user_info = client.get_user_info(auth_token, auth_verifier=auth_verifier)
			
			session = get_current_session()
			if session.is_active():
				session.terminate()
			
			session["user_info"] = user_info
			
			self.redirect("/")

class Logout(base.BaseHandler):
	def get(self):
		session = get_current_session()
		session.terminate()
		
		self.redirect("/")