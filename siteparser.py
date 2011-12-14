from urlparse import urlparse
import urllib2
import re
import string

from util.urls import getAbsoluteResourceUrl

class ParserFactory():
	def getInstanceForUrl(self, url):
		# Verify the URL (for now, simple verification only)
		if url.startswith("http://") == False:
			url = "http://" + url
		
		# Split URL to find out which parser should be instantiated and returned
		urlObject = urlparse(url)
		domain = urlObject.netloc
		parser = None
		
		if domain.find("amazon.") != -1:
			parser = AmazonParser(url)
		elif domain.find("fnac.") != -1:
			parser = FnacParser(url)
		elif domain.find("ebay.") != -1:
			parser = EbayParser(url)
		else:
			parser = BaseParser(url)
		
		# Return the parser intance
		return parser


class BaseParser(object):
	"""Base parser implementation, should be extended by specific site parsers to inherit from the base URL open logic"""
	# init method connects to the URL and retrieves the page content and stores it on self
	def __init__(self, url):
		self.url = url
		
		if self.url.startswith("http://") == False:
			self.url = "http://" + self.url
		try:
			self.pageContent = ''.join(urllib2.urlopen(self.url).read())
		except:
			self.pageContent = ""
	
	# base implementation of getTitle: gets the <title> tag in the page,
	# specific implements may decide to override
	def getTitle(self):
		try:
			return re.findall('<title>(.*?)</title>', self.pageContent, re.DOTALL)[0]
		except:
			return ""
			
	# base implementation of getPrice: returns 0
	def getPrice(self):
		return 0
		
	# base implementation of getImageUrls, returns all <img> tags found on the page
	def getImageUrls(self):
		imgPaths = re.findall('<img .*?src="(.*?)"', self.pageContent)
		return self.getCleanImageUrls(imgPaths)
	
	# utility function to get the full URLs of images found on the site
	def getCleanImageUrls(self, urls):
		paths = []
		for imgPath in urls:
			paths.append(getAbsoluteResourceUrl(imgPath, self.url))
		return paths
	
	# utility function to transform a price string with currency into a clean float string
	def getCleanPriceString(self, str):
		try:
			m = re.findall('([0-9]+)([\.,][0-9]+)*', str)
			if len(m) > 0:
				return m[0][0]
			else:
				return ''
		except:
			return ""
			
	# utility function to transform a title containing html tags into a clean string
	def getCleanTitle(self, str):
		return string.join(re.split("<.*?>", str), " ")


class AmazonParser(BaseParser):
	"""Specific Amazon parser"""
	def getTitle(self):
		try:
			str = re.findall('<span .*?id="btAsinTitle".*?>(.*?)</span>', self.pageContent, re.DOTALL)[0]
			return self.getCleanTitle(str)
		except:
			return super(AmazonParser, self).getTitle()
	def getPrice(self):
		try:
			priceString = re.findall('<b .*?class="priceLarge".*?>(.*?)</b>', self.pageContent, re.DOTALL)[0]
			return self.getCleanPriceString(priceString)
		except:
			return super(AmazonParser, self).getPrice()
	def getImageUrls(self):
		try:
			productImageArea = re.findall('<table .*?class="productImageGrid".*?>(.*?)</table>', self.pageContent, re.DOTALL)[0]
			urls = re.findall('<img .*?src="(.*?)"', productImageArea)
			return self.getCleanImageUrls(urls)
		except:
			return super(AmazonParser, self).getImageUrls()


class FnacParser(BaseParser):
	"""Specific Fnac parser"""
	def getTitle(self):
		try:
			str = re.findall('<strong .*?class="titre dispeblock".*?>(.*?)</strong>', self.pageContent, re.DOTALL)[0].strip()
			return self.getCleanTitle(str)
		except:
			return super(FnacParser, self).getTitle()
	def getPrice(self):
		try:
			priceString = re.findall('<span .*?class="price.*?>(.*?)</span>', self.pageContent, re.DOTALL)[0]
			return self.getCleanPriceString(priceString)
		except:
			return super(FnacParser, self).getPrice()
	def getImageUrls(self):
		try:
			productImageArea = re.findall('<div .*?class="nav-diaporama posrel".*?>(.*?)</div>', self.pageContent, re.DOTALL)[0]
			urls = re.findall('<img .*?src="(.*?)"', productImageArea)
			return self.getCleanImageUrls(urls)
		except:
			return super(FnacParser, self).getImageUrls()


class EbayParser(BaseParser):
	"""Specific Ebay parser"""
	def getTitle(self):
		try:
			str = re.findall('<h1 .*?class="vi-is1-titleH1".*?>(.*?)</h1>', self.pageContent, re.DOTALL)[0].strip()
			return self.getCleanTitle(str)
		except:
			return super(EbayParser, self).getTitle()
	def getPrice(self):
		try:
			priceString = re.findall('<span .*?class="vi-is1-prcp.*?>(.*?)</span>', self.pageContent, re.DOTALL)[0]
			return self.getCleanPriceString(priceString)
		except:
			return super(EbayParser, self).getPrice()
	def getImageUrls(self):
		try:
			productImageArea = re.findall('<center>(.*?)</center>', self.pageContent, re.DOTALL)[0]
			urls = re.findall('<img .*?src="(.*?)"', productImageArea)
			return self.getCleanImageUrls(urls)
		except:
			return super(EbayParser, self).getImageUrls()