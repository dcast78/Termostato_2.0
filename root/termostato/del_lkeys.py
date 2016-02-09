#!/usr/bin/python
import sys
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)
if sys.argv[1] == "cancella":
        for x in range(0,30):
                r.lpop("setpoint")
