# -*- coding: utf-8 -*-
import os, datetime, json, urllib, urllib2, shutil, threading
import re, wave
from unidecode import unidecode
from urllib2 import URLError, HTTPError, urlopen, Request

from flask import Flask, request, render_template, redirect, abort, jsonify
import requests

from time import sleep

import OSC
import time, threading, random

count = 0


receive_address = ('127.0.0.1', 8080)
s = OSC.OSCServer(receive_address)
s.addDefaultHandlers()




# define a message-handler function for the server to call.
def printing_handler(addr, tags, stuff, source):
    print "---"
    print "received new osc msg from %s" % OSC.getUrlStr(source)
    print "with addr : %s" % addr
    print "typetags %s" % tags
    print "data %s" % stuff
    print "---"

    url="http://www.musicalturk.com/loops/add"
 

    shutil.move('/Users/Kleeb2/Documents/MaxPatches/MusicalTurk/'+ str(stuff[0]), "/Users/Kleeb2/Documents/Web/Python/Thesis/"+str(stuff[0])) 
    filename = str(stuff[0])
    #filename =  '/Users/Kleeb2/Documents/Web/Python/LocalThesis/max.py'
    title = 'test'#str(count).zfill(3)
    date = str(datetime.date.today()) 
    values = [('title', title), ('postedby',date)]
    try:
    	files = {'loop': open(filename, 'rb')}
    except:
    	print 'no file'
    try:
    	r = requests.post(url, files=files, data=values)
    	print r.text
    except:
    	print 'Fail'
  
    #count = count +1
    #print count




s.addMsgHandler("/print", printing_handler) # adding our function

print "Registered Callback-functions are :"
for addr in s.getOSCAddressSpace():
    print addr


   # Start OSCServer
print "\nStarting OSCServer. Use ctrl-C to quit."
st = threading.Thread( target = s.serve_forever )
st.start()


try :
    while 1 :

        sleep(5)

except KeyboardInterrupt :
    print "\nClosing OSCServer."
    s.close()
    print "Waiting for Server-thread to finish"
    st.join() ##!!!
    print "Done"
        