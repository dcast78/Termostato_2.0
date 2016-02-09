#!/bin/bash
ln -s /usr/termostato/root/termoostato /root/termostato
ln -s /usr/termostato/home/pi/termostato /home/pi/termostato
ln -s /usr/termostato/home/grav/www /home/grav/www
for nome_file in /usr/termostato/etc/monit/conf.d/
do
 ln -s /usr/termostato/etc/monit/conf.d/$nome_file /etc/monit/conf.d/$nome_file
done
