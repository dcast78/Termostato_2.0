#!/usr/bin/python
import RPi.GPIO as GPIO
import redis
import time
import os
import sys

channel='rele_ch'

def connect():
	# use default port, db index=0
	r = redis.Redis(host='localhost', port=6379, db=0)
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

def main():
	pid = str(os.getpid())
	pidfile = "/var/run/controllo_rele_0.pid"
	#if os.path.isfile(pidfile):
	#    print "Processo gia attivo vedi file %s" % pidfile
	#    sys.exit()
	#else:
	file(pidfile, 'w').write(pid)
	print pid

	#GPIO.setup(25, GPIO.OUT, initial=GPIO.LOW)
	#GPIO.setup(25, GPIO.OUT)
	#r = redis.StrictRedis(host='localhost', port=6379, db=0)
	#while 1:
	#	rele=int(r.lrange("rele",-1,-1)[0])
	##	print rele
	#	GPIO.output(25, rele)
	#	time.sleep(2)
	data_subscribe()
	GPIO.cleanup()
	os.unlink(pidfile)

main()
