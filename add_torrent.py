#!/usr/bin/env python

import json
import requests
import sys
import os
import base64

#load setting from the config.json file sitting in the same folder as this programs
st = json.load(open(os.path.dirname(os.path.realpath(__file__))+'/config.json'))

headers = {'content-type':'application/json'}
payload = {'arguments': {}, 'method': 'torrent-add'}

#if the file passed in has magnet:? in the name we assume it's a magnet link being passed in
if "magnet:?" in sys.argv[1]:
	payload['arguments']['filename'] = sys.argv[1]
	

#anything else is taken as a torrent file	
else:
	#open the torrent file
	f = open(sys.argv[1],'rb')
	#encode the torrent file as base64, make it a string, ripe off the extra crap on the front and tail
	payload['arguments']['metainfo'] = str(base64.b64encode(f.read()))[2:][:-1]
	f.close()
	
#make the add torrent POST
r = requests.post(st['url'],auth=(st['username'],st['password']),data=json.dumps(payload),headers=headers)

#if there is a 409 error get the session id and retry
if "409: Conflict" in r.text:
	#parsing the id out of the response. dirty but easy
	headers['X-Transmission-Session-Id'] = r.text.split(': ')[2][:-11]
	r = requests.post(st['url'],auth=(st['username'],st['password']),data=json.dumps(payload),headers=headers)
	
