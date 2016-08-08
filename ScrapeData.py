from __future__ import absolute_import, division, print_function, unicode_literals

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import random
import hashlib
import requests
import sys
import time
import codecs


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

def _get_data(pagerequest):
	soup = _get_soup(pagerequest)
	return soup

def _get_country_data(pagerequest):
	soup = _get_data(pagerequest)
	while True:
		for row in soup.findAll('table',class_ = 'pt8'):
			return (row)
			#yield Medal_Tally(row)

class Medal_Tally(object):
	def __init__(self,__data):
		self.medal = dict()
		self.medal['Country_Code'] = __data.find('tr',class_ = 'c12')
		self.medal['Gold'] = __data.find('td',class_ = 'cen')
		self.medal['Silver'] = __data.find('td',class_ = 'cen')
		self.medal['Bronze'] = __data.find('td',class_ = 'cen')
		self.medal['Total'] = __data.find('td',class_ = 'cen')

	def __str__(self):
		return pprint.pformat(self.__dict__)

if __name__ == '__main__':
	x = _get_country_data("1")
	print (x.find('td',class_ = 'cen'))
	#print (x)
	#print (y.Country_Code)
