#!/usr/bin/python
import os
import glob
import time
import redis
import sys

if len(sys.argv) > 2:
        db_host=sys.argv[1]
        db_id=sys.argv[2]
	
else:
        print "Attenzione: lo script va lanciato con due argomenti!  "
        print "Lancia lo script: " + sys.argv[0] + "<db_host (es: 127.0.0.1)> <id database (es:0)>" 
	db_host='termostato_m'
	db_id=0
	print "Utilizzo i parametri di default: " + db_host + " " + str(db_id)

r = redis.StrictRedis(host=db_host, port=6379, db=db_id,password='Termostato_2.0')
r.rpush("timestamp",time.strftime("%s"))
r.rpush("setpoint","18")
r.rpush("rele","16")
i=0
while i < r.llen("camere"):
        r.rpush(r.lrange("camere",i,i)[0],"16") 
        i = i + 1

