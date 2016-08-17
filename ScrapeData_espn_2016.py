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
import sqlSetup


_GOOGLEID = hashlib.md5(str(random.random()).encode('utf-8')).hexdigest()[:16]
_COOKIES = {'GSP': 'ID={0}:CF=4'.format(_GOOGLEID)}
_HEADERS = {
    'accept-language': 'en-US,en',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml'
    }
_SESSION = requests.Session()
_WEBPAGE = "http://www.espn.com/olympics/summer/2016/medals/_/view/overall"



def _get_page(pagerequest):
	resp_url = _SESSION.get(pagerequest, headers=_HEADERS, cookies=_COOKIES)
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
	data = soup.findAll('table',class_ = 'medals olympics has-team-logos')
	table = data[0].findAll('tr')
	while True:
		for row in range(1,(len(table))):
			yield Medal_Tally(table[row])
		if row == (len(table)):
			print ("Year Extracted")
		else:
			break

class Medal_Tally(object):
	def __init__(self,__data):
		self.medal = dict()
		td = __data.findAll('td')	
		#self.medal['Country'] = text[0].strip()
		self.medal['Country_Code'] = td[0].text.strip()
		#self.medal['url'] = __data.find('a')['href']
		self.medal['Year'] = "2016"
		self.medal['Id'] = self.medal['Country_Code'] + '_' + self.medal['Year']
		self.medal['Gold'] = td[1].text.strip()
		self.medal['Silver'] = td[2].text.strip()
		self.medal['Bronze'] = td[3].text.strip()
		self.medal['Total'] = td[4].text.strip()
		self.filled = False

if __name__ == '__main__':
	olympic_gen = _get_data(_WEBPAGE) # Create generator object to extract wikipedia table
	olympics_data = list()
	try:
		for item in olympic_gen:
			print (item.medal['Country_Code'])
			olympics_data.append([item.medal['Id'],item.medal['Year'],item.medal['Country_Code'],
				item.medal['Gold'],item.medal['Silver'],item.medal['Bronze'],item.medal['Total']])
	except StopIteration:
		pass
	print ('Update SQL')
	sqlSetup.mysqlConn()
	sqlSetup.update_CountryMedals_2016(olympics_data)

	'''
	x = _get_soup(_WEBPAGE)
	table = x.findAll('table',class_ = 'medals olympics has-team-logos') # Find the table
	for item in table[0].findAll('tr')[1:]:
		td = item.findAll('td')		
		country_code = td[0].text.strip()
		gold = td[1].text.strip()
		silver = td[2].text.strip()
		bronze = td[3].text.strip()
		total = td[4].text.strip()
	print (table[0].findAll('tr'))
	'''