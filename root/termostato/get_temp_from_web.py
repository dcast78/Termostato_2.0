#!/usr/bin/python
import urllib
import urllib2
import os
import glob
import time
import redis
import sys
from urllib2 import Request, urlopen, URLError, HTTPError


if len(sys.argv) > 2:
        db_host=sys.argv[1]
        db_id=sys.argv[2]

else:
        print "Attenzione: lo script va lanciato con due argomenti!  "
        print "Lancia lo script: " + sys.argv[0] + "<db_host (es: 127.0.0.1)> <id database (es:0)> tag_camera url"
	sys.exit	

import urllib2
response = urllib2.urlopen(sys.argv[4])
html = response.read()
print html

intestazione,temp=html.split(' ')
temp=float(temp.replace("C",""))
print temp
if temp < 80:
	r = redis.StrictRedis(host=db_host, port=6379, db=db_id,password='Termostato_2.0')
	r.lset(sys.argv[3],-1,temp)

