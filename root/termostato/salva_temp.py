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


 
os.system('/sbin/modprobe w1-gpio')
os.system('/sbin/modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + sys.argv[4])[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
	if temp_c < 50:
        	return temp_c
	
print(device_folder + " " + str(read_temp()))	
r = redis.StrictRedis(host=db_host, port=6379, db=db_id,password='Termostato_2.0')
r.lset(sys.argv[3],-1,float(read_temp()))
