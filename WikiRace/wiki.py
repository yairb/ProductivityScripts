#!/usr/bin/python

import httplib2, re, urllib, sys, time
from bs4 import BeautifulSoup

# globals
checkedUrls = []
MAX_DEEP = 30
COUNTER = 0

def getAnchors (url):
	global COUNTER
	print str(COUNTER) + " getAnchors of: " + url
	COUNTER += 1
	status, response = http.request(url)
	soup = BeautifulSoup(response, 'html.parser')
	return set(soup.find_all('a', href=re.compile(r"^/wiki/.*[^.jpg]$")))
def isValue (value):
	link = value.get('href')
	return value.parent.get('class') != 'citation web' and value.parent.get('class') != 'citation book' and value.parent.get('class') != 'reference-text' and not 'Category:' in link and not 'Special:' in link and not 'Help:' in link and link != '/wiki/Main_Page' and not link in checkedUrls

def naiveLookForUrl (original, dest, deep, path):
	toRet = MAX_DEEP + 1
	if (deep > MAX_DEEP or original in checkedUrls):
		return toRet
	print "try deep of " + str(deep) + " with path: " + urllib.unquote(str(path)).decode('utf8')
	checkedUrls.append(original)
	for link in getAnchors(original):
		if not isValue(link):
			continue
		href = link.get('href')
		newList = path[:]
		newList.append(PREFIX + href)
		if (PREFIX + href == dest):
			print "found!! deep: " + str(deep) + " path: " + str(newList)
			return deep
		d = naiveLookForUrl(PREFIX + href, dest, deep + 1, newList)
		if (d < toRet):
			toRet = d
	return toRet

def betterLookForUrl (curList, dest, deep):
	curDeep = deep
	found = False
	while found == False:
		if (curDeep > MAX_DEEP):
			print "MAX deep!!!!"
			return []
		print "===========try deep of " + str(curDeep) + "============="#+ " with path: " + urllib.unquote(str(path)).decode('utf8')
		
		nextList = []	
		for address in curList:
			url = address[-1]
			if not url.startswith(PREFIX):
				url = PREFIX + url
			if url == dest:
				found = True
				print "FOUND!!!"
				return address + [link]
			for a in getAnchors(url):
				link = a.get('href')
				if isValue(a):
					if PREFIX + link == dest:
						found = True
						print "FOUND!!!"
						return address + [link]
					nextList.append(address + [link])
					#print "adding to list: " + str(address + [link])
					checkedUrls.append(link)
		curDeep += 1
		curList = nextList
	return []

# main() starts here:
length = len(sys.argv)
lang = 'en'
if length < 3:
	print "Not enough args to start the script: origin, dest, language[optional]"
	exit()
if length > 3:
	lang = str(sys.argv[3])
PREFIX = 'https://' + lang + '.wikipedia.org'	


http = httplib2.Http()
#deepFound = naiveLookForUrl(str(sys.argv[1]), str(sys.argv[2]), 0, [])

#measure time
start = time.time()
l = betterLookForUrl([[str(sys.argv[1])]], str(sys.argv[2]), 0)
end = time.time()
print "list: " + str(l) + " - run " + str(end - start) + " seconds"
