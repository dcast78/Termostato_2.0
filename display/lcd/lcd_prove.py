#!/usr/bin/python
import lcddriver
from time import *
import time

import getopt
import sys

#import os
import subprocess

import redis

#print 'ARGV      :', sys.argv[1:]

#options, remainder = getopt.getopt(sys.argv[1:], 'o:v', ['output=','verbose','version=',])
#print 'OPTIONS   :', options

#print (type(sys.argv[1:]))
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)
lcd = lcddriver.lcd()
lcd.lcd_clear();
lcd.lcd_backlight()
x=0
j=0 
#j si incrementa per capire se e il primo ciclo 
disp_riga1_old=0
disp_riga1=0
disp_riga2_old=0
disp_riga2=0
riga2=""
lungh_riga2=0
while True:
 if time.strftime("%M:%S") == "00:00" or j == 100 : 
#  riga2=subprocess.check_output("/usr/bin/google --cal=franca.fazioli@gmail.com calendar today | grep -v \"gmail.com\" | grep -v \"^$\"| head -3",shell=True)
#  riga2="."
  lungh_riga2=len(riga2)
  riga2=riga2[:len(riga2)-1]
 if time.strftime("%S") == "00" or j == 0 : 
  temp_3=r.lrange('temp_3',-1,-1)
  temp_2=r.lrange('temp_2',-1,-1)
  temp_1=r.lrange('temp_1',-1,-1)
  temp_3=str(round((float(temp_3[0])),1)).split()
  temp_2=str(round((float(temp_2[0])),1)).split()
  temp_1=str(round((float(temp_1[0])),1)).split()
  rele=r.lrange('rele',-1,-1)
  if rele == 0 :
   stato_rele=["S"]
  else :
   stato_rele=["A"]
  ora=time.strftime("%H:%M").split()
  j=j+1
  #print("Aggiornamento ora")
  disp_riga1=''.join(temp_3 + stato_rele + temp_2 + [" "] + temp_1 + [" "]  + ora)
  #print(disp_riga1)
 print disp_riga1, disp_riga1_old
 if disp_riga1 != disp_riga1_old :
  lcd.lcd_clear();
  print disp_riga1
  lcd.lcd_display_string(disp_riga1, 1)
  disp_riga1_old=disp_riga1
 
 disp_riga2=riga2[0+x:20+x]
 if disp_riga2 != disp_riga2_old :
  print disp_riga2
  lcd.lcd_display_string(disp_riga2, 2)
  disp_riga2_old=disp_riga2

 if x > lungh_riga2-22:
  x=-1
 x=x+1
 time.sleep(.4)
#lcd.lcd_display_string("My name is", 2)
#lcd.lcd_display_string("picorder", 3)
#lcd.lcd_display_string("I am a Raspberry Pi", 4)
