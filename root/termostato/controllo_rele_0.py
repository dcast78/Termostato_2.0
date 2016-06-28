#!/usr/bin/python
import RPi.GPIO as GPIO
import redis
import time
import os
import sys
import logging
logging.basicConfig(filename='/var/log/termostato.log',level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')

channel='rele_ch'

def connect():
	r = redis.Redis(host='localhost', port=6379, db=0, password='Termostato_2.0')
	return r


def data_subscribe():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(25, GPIO.OUT)
	global channel
	r = connect()
	ps = r.pubsub()
	ps.subscribe(channel)
	for message in ps.listen():
		a=message
		print int(a['data'])
		GPIO.output(25, int(a['data']))
		logging.debug(__file__ + ' Set rele pin 25 value -> ' + str(a['data']))

def main():
	pid = str(os.getpid())
	pidfile = "/var/run/controllo_rele_0.pid"
	file(pidfile, 'w').write(pid)
	print pid

	data_subscribe()
	GPIO.cleanup()
	os.unlink(pidfile)

main()
