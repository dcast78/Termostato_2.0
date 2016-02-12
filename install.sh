#!/bin/bash
#ln -s /usr/termostato/root/termoostato /root/termostato
ln -s /usr/termostato/home/pi/termostato /home/pi
ln -s /usr/termostato/home/grav/www/0/termo /home/grav/www/0
ln -s /usr/termostato/home/grav/www/0/user/pages /home/grav/www/0/user

ln -s /usr/termostato/root/termostato /root

for nome_file in /usr/termostato/etc/monit/conf.d/*
do
 ln -s /usr/termostato/etc/monit/conf.d/`basename $nome_file` /etc/monit/conf.d/`basename $nome_file`
 #echo `basename $nome_file` 
done

ln -s /usr/termostato/etc/sudoers.d/grav /etc/sudoers.d/grav
