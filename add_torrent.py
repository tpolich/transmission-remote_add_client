#!/usr/bin/env python

import json
import requests
import sys
import os

#load setting from the config.json file sitting in the same folder as this programs
settings = json.load(open(os.path.dirname(os.path.realpath(__file__))+'/config.json'))

username = settings['username']
password = settings['password']
url = settings['url']
torrent_url = sys.argv[1]
headers = {'content-type':'application/json'}
payload = {
           'arguments': {
				 'filename': torrent_url
	         },
	         'method': 'torrent-add',
	      }
		  
r = requests.post(url,auth=(username,password),data=json.dumps(payload),headers=headers)

#if there is a 409 error get the session id and retry
if "409: Conflict" in r.text:
	#parsing the id out of the response. dirty but easy
	headers['X-Transmission-Session-Id'] = r.text.split(': ')[2][:-11]
	r = requests.post(url,auth=(username,password),data=json.dumps(payload),headers=headers)
	
