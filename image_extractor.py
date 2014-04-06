import urllib2
import re, os, sys
from bs4 import BeautifulSoup
from urlparse import urlsplit


class extractor(object):
	
	def __init__(self):
		self.status = ''
		self.no_pages = 0
		
	
	def __check_status(self, a):
		print "A"
		out = re.search(r'("status":")(\w+)', a)
		self.status = out.group(2)
		
		
	def __check(self):
		 
		self.__check_status(a)
		if self.status == "ok":
			return True

			
	def __no_of_pages(self, a):
		if self.__check:
			out = re.search(r'("pageSize":)(\w+)', a)
			self.no_pages = int(out.group(2))
						
	
	def extract_weburls(self, a):
		self.__no_of_pages(a)
		index = 0
		self.urls = []
		if self.no_pages:
			for i in range(self.no_pages):				
				out = re.search(r'("webUrl":")(.+)', a)
				a = a[index:]				
				index = out.end()				
				self.urls.append(out.group(2))
		return self.urls
		
	
class photo_extractor():

	def __init__(self, urls):
		self.urls = urls
		
	def __weburls(self, url):
		print url
		
		try:
			page = urllib2.urlopen(url).read()
		except urllib2.HTTPError, e:
			a = e.fp.read()
		output1 = open("/home/swamydkv/nalashaa/tests/test.txt",'a+')
		output1.write(a)
			
		soup = BeautifulSoup(''.join(a))
		imgTags = soup.findAll('img')
		for imgTag in imgTags:
			imgUrl = imgTag['src']
        	try:
				imgData = urllib2.urlopen(imgUrl).read()
        	except urllib2.HTTPError, e:
				imgData = e.fp.read()
            
        	finally:
        		fileName = os.path.basename(urlsplit(imgUrl)[2])        		
        		fileName1 = "/home/swamydkv/nalashaa/tests/"+fileName
           		output = open(fileName1,'wb')
            	output.write(imgData)
            	output.close()
		
	def __extract_images(self):
		

		if type(self.urls) == type(''):
			self.__weburls(self.urls)
		
		elif type(self.urls) == type([]):
			for url in self.urls:
				self.__weburls(url)
				
	def extract(self):
		self.__extract_images()
			
				
				
class guardian(extractor):
	
	def __init__(self, search, page_format="json"):
		self.search = search
		self.page_format = page_format
		self.search_page = ''

		
	def guardian_search(self):
		guardian_search = "http://content.guardianapis.com/search?q="+self.search+"&format="+self.page_format
		self.search_page = urllib2.urlopen(guardian_search).read()		
		return self.search_page
		
	
##http://content.guardianapis.com/search?q=football&format=json		
obj = guardian("football")
pages = obj.guardian_search()

img = obj.extract_weburls(pages)

ph = photo_extractor(img)

ph.extract()
