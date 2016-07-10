#!/usr/bin/python

import httplib2, re, urllib, sys, time
from bs4 import BeautifulSoup

checkedUrls = []
def naiveLookForUrl (original, dest, deep, path):
	toRet = 1000
	if (deep > MAX_DEEP or original in checkedUrls):
		return toRet
	print "try deep of " + str(deep) + " with path: " + urllib.unquote(str(path)).decode('utf8')
	checkedUrls.append(original)
	status, response = http.request(original)
	soup = BeautifulSoup(response, 'html.parser')
	for link in getAnchors(original):
		href = link.get('href')
		#print(href)
		newList = path[:]
		newList.append(PREFIX + href)
		if (PREFIX + href == dest):
			print "found!! deep: " + str(deep) + " path: " + str(newList)
			return deep
		d = naiveLookForUrl(PREFIX + href, dest, deep + 1, newList)
		if (d < toRet):
			toRet = d
	return toRet
def getAnchors (url):
	print "getAnchors of: " + url
	status, response = http.request(url)
	soup = BeautifulSoup(response, 'html.parser')
	return set(soup.find_all('a', href=re.compile(r"^/wiki/.*[^.jpg]$")))
def betterLookForUrl (curList, dest, deep):
	curDeep = deep
	found = False
	while found == False:
		if (curDeep > MAX_DEEP):
			return -1
		print "try deep of " + str(curDeep) #+ " with path: " + urllib.unquote(str(path)).decode('utf8')
		#checkedUrls.append(original)
		nextList = []	
		for address in curList:
			if isinstance(address, basestring):
				url = address
			else:
				url = address.get('href')
			if not url.startswith(PREFIX):
				url = PREFIX + url
			if url == dest:
				found = True
				print "FOUND!!!"
				return deep
			for a in getAnchors(url):
				link = a.get('href')
				if a.parent.get('class') != 'citation web' and a.parent.get('class') != 'citation book' and a.parent.get('class') != 'reference-text' and not 'Category:' in link and not 'Special:' in link and link != '/wiki/Main_Page' and not link in checkedUrls:
					if PREFIX + link == dest:
						found = True
						print "FOUND!!!"
						return deep
					nextList.append(link)
					checkedUrls.append(link)
		curDeep += 1
		curList = nextList
	return -1
length = len(sys.argv)
lang = 'en'
if length < 3:
	print "Not enough args to start the script"
	exit()
if length > 3:
	lang = str(sys.argv[3])
PREFIX = 'https://' + lang + '.wikipedia.org'	
MAX_DEEP = 3
http = httplib2.Http()
#num = naiveLookForUrl(str(sys.argv[1]), str(sys.argv[2]), 0, [])
start = time.time()
num = betterLookForUrl([str(sys.argv[1])], str(sys.argv[2]), 0)
end = time.time()
print "min: " + str(num) + " - run " + int(end - start) + " seconds"
