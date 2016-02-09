#!/usr/bin/python
import RPi.GPIO as GPIO
import redis
import time
import os
import sys

channel='rele_ch'

def connect():
	r = redis.Redis(host='localhost', port=6379, db=1, password='Termostato_2.0')
	return r


def data_subscribe():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(22, GPIO.OUT)
	global channel
	r = connect()
	ps = r.pubsub()
	ps.subscribe(channel)
	for message in ps.listen():
		a=message
		print int(a['data'])
		GPIO.output(22, int(a['data']))

def main():
	pid = str(os.getpid())
	pidfile = "/var/run/controllo_rele_1.pid"
	file(pidfile, 'w').write(pid)
	print pid

	data_subscribe()
	GPIO.cleanup()
	os.unlink(pidfile)

main()
