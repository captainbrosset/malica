import urllib, hashlib
from urlparse import urlparse
import os
import re
import urllib2
import logging

from google.appengine.api import users
from htmlentitydefs import name2codepoint
from django.core.paginator import ObjectPaginator, InvalidPage
from google.appengine.api import users

from util.gaesessions import get_current_session
from model.present import Present
import siteparser

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
	session = get_current_session()
	is_logged_in = False
	user_info = {}
	if session.is_active() and session.has_key("user_info"):
		is_logged_in = True
		user_info = session["user_info"]

	return {
		'is_logged_in': is_logged_in,
		'user_info': user_info
	}


def get_current_sort(requestedSort):
	sort = "-dateAdded"
	if requestedSort == "dateAdded" or requestedSort == "-approximatePrice" or requestedSort == "approximatePrice":
		sort = requestedSort
	return sort

def is_username_in_datamodel(username):
	query = Present.all().filter("user = ", username)
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

def get_presents_and_pages(username, order):
	query = Present.all().order(order).filter("user = ", username)

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