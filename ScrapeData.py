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
_pagerequest = 1

def _get_page(pagerequest):
	resp_url = _SESSION.get(_WEBPAGE+pagerequest, headers=_HEADERS, cookies=_COOKIES)
	if resp_url.status_code == 200:
		print (resp_url)
		return resp_url.text
	else:
		print ("No access")

def _get_soup(pagerequest):
    """Return the BeautifulSoup for a page on scholar.google.com"""
    html = _get_page(pagerequest)
    return BeautifulSoup(html, 'html.parser')

def _get_data(pagerequest):
	data = _get_soup(pagerequest)
	return data