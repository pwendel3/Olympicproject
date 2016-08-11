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
_WEBPAGE = "http://www.sports-reference.com/olympics/summer/"
_ATHLETESPAGE = "http://www.sports-reference.com/"

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

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def _get_data(pagerequest):
	soup = _get_soup(pagerequest)
	data = soup.findAll('table',class_ = "sortable  suppress_all stats_table")
	table = data[0].findAll('tr')
	participants = soup.findAll('div',id = "info_box")
	#print (participants)

	while True:
		for row in range(1,(len(table[1:])+1)):
			yield Medal_Tally(table[row])
		if row == (len(table[1:])+1):
			print ("Year Extracted")
		else:
			break

class Medal_Tally(object):
	def __init__(self,__data):
		self.medal = dict()
		self.medal['Country_Code'] = find_between(__data.find('a')['href'],"countries/","/summer")
		#self.medal['Year'] = find_between(__data.find('a')['href'],"g=","&")
		self.medal['Year'] = __data.find('a')['title'][0:4]
		self.medal['Id'] = self.medal['Country_Code'] + '_' + self.medal['Year']
		self.medal['url'] = __data.find('a')['href']
		data = ",".join(__data.findAll(text = True))
		medals = data.split(",")
		self.medal['Country'] = medals[3]
		self.medal['Gold'] = medals[5]
		self.medal['Silver'] = medals[7]
		self.medal['Bronze'] = medals[9]
		self.medal['Total'] = medals[11]
		self.filled = False
	
	def fill(self):
		#self.Athletes = dict()
		self.Athletes = list()
		soup = _get_soup(_ATHLETESPAGE+self.medal['url'])
		data = soup.findAll('table',class_ = 'sortable  stats_table',id = "athletes")
		table = data[0].findAll('tr')
		participants = soup.findAll('div',id = "info_box")
		participants = participants[0].findAll('br')
		
		# Get total Participants
		participants = (participants[2].text).split(":")
		participants_total = find_between(participants[1],"","(")
		participants_men = find_between(participants[1],"(","men")
		participants_women = find_between(participants[1], "and","women")
		self.medal['Total_Participants'] = participants_total.strip()
		self.medal['Men'] = participants_men.strip()
		if participants_women.strip() != "":
			self.medal['Women'] = participants_women.strip()
		else:
			self.medal['Women'] = 0
		
		# Get athlete details
		for row in table[1:]:
			data = list()
			temp = row.findAll('td')
			if len(temp) == 9:
				for i in temp:
					text  = i.find(text = True)
					if text is None:
						text = 0
					data.append(unicode(text))
			data.extend([self.medal['Id'],self.medal['Year']])
			self.Athletes.append(data)
		self.filled = True
		return self

	def __str__(self):
		return pprint.pformat(self.__dict__)


if __name__ == '__main__':
	sqlSetup.mysqlConn()
	for i in range(0,9):
		year = str(1980+4*i)
		olympics_gen = _get_data(_WEBPAGE+year) #Generator Object
		olympics_data = list()
		athletes_data = list()
		#Iterate over a generator object
		try:
			for j in olympics_gen:
				print (j.medal['Country'],j.medal['Year'])
				athletes = j.fill()
				olympics_data.append([j.medal['Id'],j.medal['Year'],j.medal['Country'],j.medal['Country_Code'],j.medal['Gold'],
									j.medal['Silver'],j.medal['Bronze'],j.medal['Total'],j.medal['Total_Participants'],
									j.medal['Men'],j.medal['Women']])
				
				athletes_data.append(athletes.Athletes)
		except StopIteration:
			pass
		#Update SQL table
		print ("Update Country Medal Tally")
		sqlSetup.update_CountryMedals(olympics_data) #Olympic Medals By Country
		print ("Update Athletes")
		for item in athletes_data:
			sqlSetup.update_Athlete(item)