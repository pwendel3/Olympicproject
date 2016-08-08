from __future__ import absolute_import, division, print_function, unicode_literals

from bs4 import BeautifulSoup
import arrow
import bibtexparser
import codecs
import hashlib
import pprint
import random
import re
import requests
import sys
import time


_GOOGLEID = hashlib.md5(str(random.random()).encode('utf-8')).hexdigest()[:16]
_COOKIES = {'GSP': 'ID={0}:CF=4'.format(_GOOGLEID)}
_HEADERS = {
    'accept-language': 'en-US,en',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml'
    }
_SESSION = requests.Session()
_WEBPAGE = "http://www.databaseolympics.com/games/gamesyear.htm?g="
_pagerequest = "1"

def _get_page(pagerequest):
	resp_url = _SESSION.get(_WEBPAGE+pagerequest, headers=_HEADERS, cookies=_COOKIES)
	if resp_url.status_code == 200:
		return resp_url.text
	else:
		print ("No access")

def _get_soup(pagerequest):
    """Return the BeautifulSoup for a page on scholar.google.com"""
    html = _get_page(pagerequest)
    return BeautifulSoup(html, 'html.parser')

'''def _get_data(pagerequest):
	soup = _get_soup(pagerequest)
	return soup'''

def _get_country_data(pagerequest):
	soup = _get_soup(pagerequest)
	temp = soup.find(class_ = 'pt8').findAll('tr')
	#headers = ",".join(temp[0].findAll(text = True))
	#headers = headers.split(',')
	while True:
		for row in range(1,len(temp)):
			yield Medal_Tally(temp[row])
		if row == len(temp):
			"Page Extracted"
		else:
			break

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

class Medal_Tally(object):
	def __init__(self,__data):
		self.medal = dict()
		self.medal['Country_Code'] = __data.find('a')['href'].split("cty=")[1]
		self.medal['Year'] = find_between(__data.find('a')['href'],"g=","&")
		data = ",".join(__data.findAll(text = True))
		data = data.split(",")
		self.medal['Country'] = data[0]
		self.medal['Gold'] = data[1]
		self.medal['Silver'] = data[2]
		self.medal['Bronze'] = data[3]
		self.medal['Total'] = data[4]

	def __str__(self):
		return pprint.pformat(self.__dict__)

if __name__ == '__main__':
	x = _get_country_data("1")
	a = list()
	try:
		for i in x:
			a.append(i)
		#print (a)
	except StopIteration:
		pass
	print (i)

