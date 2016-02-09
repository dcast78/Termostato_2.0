#!/usr/bin/python
import sys
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)
if sys.argv[1] == "accoda":
        for x in range(0,30):
                r.lpush("setpoint",22.25)
