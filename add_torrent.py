#!/usr/bin/env python

import json
import urllib
import urllib.error
import urllib.request
import sys
import os
import base64

#load setting from the config.json file sitting in the same folder as this programs
st = json.load(open(os.path.dirname(os.path.realpath(__file__))+'/config.json'))

headers = {
		'content-type':'application/json',
		'Authorization' : 'Basic ' + str(base64.b64encode(bytes(st['username'] + ':' + st['password'],'utf-8')),'utf-8'),
	}
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
	

req = urllib.request.Request(st['url'], data=bytes(json.dumps(payload),'ascii'), headers = headers)	

try:
	urllib.request.urlopen(req)
except urllib.error.HTTPError as error:
	headers['X-Transmission-Session-Id'] = bytes.decode(error.read()).split(': ')[2][:-11]
	req = urllib.request.Request(st['url'], data=bytes(json.dumps(payload),'ascii'), headers = headers)
	urllib.request.urlopen(req)
