from urlparse import urlparse
import siteparser
from google.appengine.api import users
from htmlentitydefs import name2codepoint
from django.core.paginator import ObjectPaginator, InvalidPage
import os
import re
import urllib2
import datamodel
import logging
from google.appengine.api import users
import urllib, hashlib

# Sniff the user agent to tell people they should use decent browsers ...
def is_supported_browser():
	ua = os.environ.get("HTTP_USER_AGENT", "N/A")
	
	logging.debug(ua)
	
	# For now, only a simple find string is used and only gecko and webkit are supported
	webkit = ua.find("AppleWebKit") != -1
	ff = ua.find("Gecko") != -1
	
	return ff or webkit


# Simply returns the real path of the template file given its relative path
def get_template_path(template):
	return os.path.join(os.path.dirname(__file__), template)


# Utility method that returns the list of URLs of all <img> tags found on a page located at a given URL
def get_image_urls_and_title_from_page(url):
	factory = siteparser.ParserFactory()
	parser = factory.getInstanceForUrl(url)

	return {
		'img': parser.getImageUrls(),
		#'title': htmlentitydecode(parser.getTitle()),
		'title': parser.getTitle(),
		'price': parser.getPrice()
	}


# Decode HTML entities
def htmlentitydecode(s):
	return re.sub('&(%s);' % '|'.join(name2codepoint), lambda m: unichr(name2codepoint[m.group(1)]), s)

def get_gravatar_url(email):
	# FIXME: not working. I guess it requires a true globally available URL
	default = "/statics/images/noImage.png"
	size = 40
	gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
	gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
	return gravatar_url
	
	
# Utility method that returns the base template values to be used in most request handlers: current user and login/logout links
def prepare_base_template_values(request):
	if users.get_current_user():
		um_url = users.create_logout_url("/")
		um_link_text = "se d&eacute;connecter"
		gravatar_url = get_gravatar_url(users.get_current_user().email())
	else:
		um_url = users.create_login_url("/")
		um_link_text = "se connecter"
		gravatar_url = None
	return {
		'um_url': um_url,
		'um_link_text': um_link_text,
		'current_user': users.get_current_user(),
		'gravatar_url': gravatar_url
	}


def get_current_sort(requestedSort):
	sort = "-dateAdded"
	if requestedSort == "dateAdded" or requestedSort == "-approximatePrice" or requestedSort == "approximatePrice":
		sort = requestedSort
	return sort

def is_email_in_datamodel(email):
	user = users.User(email)
	query = datamodel.Present.all().filter("user = ", user)
	logging.info(query.fetch(1))
	presents = query.fetch(1)
	if len(presents) == 1:
		return True
	else:
		return False

def prepare_present_list_for_template(presents):
	list = []
	for present in presents:
		if present.url:
			urlObject = urlparse(present.url)
			shortUrl = urlObject.scheme + "://" + urlObject.netloc
		else:
			shortUrl = ""
		
		list.append({
			'shortUrl': shortUrl,
			'key': present.key,
			'title': present.title,
			'approximatePrice': present.approximatePrice,
			'url': present.url,
			'image': present.image,
			'user': present.user
		})
	return list

PAGESIZE = 16

def get_presents_and_pages(user, order):
	query = datamodel.Present.all().order(order).filter("user = ", user)

	presents = prepare_present_list_for_template(query.fetch(1000))

	return {
		'presents': presents,
		'atLeastOnePresent': len(presents),
	}


def get_current_sort_urls(currentSort, searchedUser = False):
	if searchedUser:
		urlStart = "/liste/" + searchedUser + "?sort="
	else:
		urlStart = "?sort="
		
	sortSign = "-"
	if currentSort == "-approximatePrice": sortSign = ""
	priceUrl = urlStart + sortSign + "approximatePrice"
	
	sortSign = "-"
	if currentSort == "-dateAdded": sortSign = ""
	dateUrl = urlStart + sortSign + "dateAdded"
	
	return {
		'priceUrl': priceUrl,
		'dateUrl': dateUrl
	}