#!/usr/bin/python
import sys
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)
if sys.argv[1] == "crea":
        for x in range(0,47):
                r.rpush("c_lun","cucina")
                r.rpush("c_mar","cucina")
                r.rpush("c_mer","cucina")
                r.rpush("c_gio","cucina")
                r.rpush("c_ven","cucina")
                r.rpush("c_sab","cucina")
                r.rpush("c_dom","cucina")

print(r.lrange("c_lun",0,-1))
print(r.lrange("c_mar",0,-1))
print(r.lrange("c_mer",0,-1))
print(r.lrange("c_gio",0,-1))
print(r.lrange("c_ven",0,-1))
print(r.lrange("c_sab",0,-1))
print(r.lrange("c_dom",0,-1))
