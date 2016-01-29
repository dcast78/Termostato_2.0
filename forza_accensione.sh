#!/usr/bin/python
import sys
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)
r.set("accendi",1)
r.expire("accendi",900)
ttl=r.ttl("accendi")
print("Accensione forzata per: " + str(ttl) + " secondi")
