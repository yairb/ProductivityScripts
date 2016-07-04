#!/usr/bin/python

import httplib2, re, urllib, sys
from bs4 import BeautifulSoup

checkedUrls = []
def lookForUrl (original, dest, deep, path):
	toRet = 1000
	if (deep > MAX_DEEP or original in checkedUrls):
		return toRet
	print "try deep of " + str(deep) + " with path: " + urllib.unquote(str(path)).decode('utf8')
	checkedUrls.append(original)
	status, response = http.request(original)
	soup = BeautifulSoup(response, 'html.parser')
	for link in set(soup.find_all('a', href=re.compile(r"^/wiki/.*[^.jpg]$"))):
		href = link.get('href')
		#print(href)
		newList = path[:]
		newList.append(PREFIX + href)
		if (PREFIX + href == dest):
			print "found!! deep: " + str(deep) + " path: " + str(newList)
			return deep
		d = lookForUrl(PREFIX + href, dest, deep + 1, newList)
		if (d < toRet):
			toRet = d
	return toRet

length = len(sys.argv)
lang = 'en'
if length < 3:
	print "Not enough args to start the script"
	exit()
if length > 3:
	lang = str(sys.argv[3])
PREFIX = 'https://' + lang + '.wikipedia.org'	
MAX_DEEP = 2
http = httplib2.Http()
PREFIX = 'https://he.wikipedia.org'
num = lookForUrl(str(sys.argv[1]), str(sys.argv[1]), 0, [])
print "min: " + str(num)
