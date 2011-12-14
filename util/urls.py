from urlparse import urlparse

def getAbsoluteResourceUrl(resourcePath, siteUrl):
	if resourcePath[0:4] == "http":
		return resourcePath
	else:
		siteUrlObject = urlparse(siteUrl)
		if resourcePath[0:2] == "//":
			return siteUrlObject.scheme + "://" + resourcePath[2:]
		elif resourcePath[0:1] == "/":
			return siteUrlObject.scheme + "://" + siteUrlObject.netloc + resourcePath
		else:
			return siteUrlObject.scheme + "://" + siteUrlObject.netloc + siteUrlObject.path[0:siteUrlObject.path.rfind("/")] + "/" + resourcePath

"""
print getAbsoluteResourceUrl("//images/myImage.png", "http://mydomain.com/servlet/test/page.html")
print getAbsoluteResourceUrl("images/myImage.png", "http://mydomain.com/servlet/test/page.html")
print getAbsoluteResourceUrl("/images/myImage.png", "http://mydomain.com/servlet/test/page.html")
print getAbsoluteResourceUrl("http://mydomain.com/images/myImage.png", "http://mydomain.com/servlet/test/page.html")
"""