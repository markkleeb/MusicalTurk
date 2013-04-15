# -*- coding: utf-8 -*-
import os, datetime, json, urllib2, shutil, threading
import re
from unidecode import unidecode

from flask import Flask, request, render_template, redirect, abort, jsonify
import requests

from time import sleep

import OSC
import time, threading, random



# create Flask app
#app = Flask(__name__)   # create our flask app


# --------- Routes ----------

open('loops.txt', 'w').close()




def main():
	
	client = OSC.OSCClient()
	client.connect( ('127.0.0.1', 10000) )
	

	json_url = "http://musicalturk.herokuapp.com/data/loops"

	local_files = []
	try:
		with open('loops.txt', 'r') as f:
			local_files = json.load(f)

	except:
		pass


	
	results = requests.get(json_url)

	
		
	
		# if we receive a 200 HTTP status code, great! 
	if results.status_code == 200:
		loops = results.json['loops']
		diff = [item for item in loops if item not in local_files]
		print("Difference %s" % diff)
		
		for n in diff:
			msg = OSC.OSCMessage()
			msg.setAddress("/test")
			url="http://megaphonosizer.s3.amazonaws.com/%s" % n['path']
			req2 = urllib2.Request(url)
			resp = urllib2.urlopen(req2)

			data = resp.read()

			mp3Name = n['path']
			song = open(mp3Name, "w")
			song.write(data)
			song.close()
			shutil.move("/Users/Kleeb2/Documents/Web/Python/Thesis/"+n['path'], "/Developer/of_0072/apps/myApps/musicalTurk/bin/data/"+n['path'])
			print("name %s" % n['name'])
			
			data = [n['path'], n['name'].replace(' ',''), n['title'].replace(' ',''), n['tag']] 	

			msg.append([data])
			client.send(msg)

			#r = requests.get(url)
			#print len(r.content)
	

		local_files += diff
		with open('loops.txt', 'w') as f:
			json.dump(local_files, f)
		

			
		templateData = {
		'venues' : loops
		}
		#return jsonify(tacos)
		#return render_template('tacos.html', **templateData)

	
	else:
			# Foursquare API request failed somehow
		return "uhoh, something went wrong %s" % results.json
	
			



while True:
	main()
	sleep(2)





	