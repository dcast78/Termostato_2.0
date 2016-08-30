#!/bin/bash
#ln -s /usr/termostato/root/termoostato /root/termostato
ln -s /usr/termostato/home/pi/termostato /home/pi
ln -s /usr/termostato/home/grav/www/0/termo /home/grav/www/0
ln -s /usr/termostato/home/grav/www/0/user/pages /home/grav/www/0/user

ln -s /usr/termostato/root/termostato /root

mkdir /etc/monit/conf.d
for nome_file in /usr/termostato/etc/monit/conf.d/*
do
 ln -s /usr/termostato/etc/monit/conf.d/`basename $nome_file` /etc/monit/conf.d/`basename $nome_file`
 #echo `basename $nome_file` 
done

ln -s /usr/termostato/etc/sudoers.d/grav /etc/sudoers.d/grav

echo "Ricerca sensori collegati al bus 1Wire"
ls -l /sys/bus/w1/devices/

echo "Ora viene generata una riga da inserire su crontab di root, devi sostituire nome_sensore con una stringa che identifica ad esempio una stanza. Se i sensori vengono usati per piu' istanza devi anche sostituire il valore 0 con il numero di istanza appropriato. Per i dettagli vedi http://www.raspibo.org/wiki/index.php?title=Termostato_2.0"
echo -n "*/5 * * * * /root/termostato/salva_tempo.py termostato_m 0; " ; for id_sensore in `ls -1| grep -v w1_bus_master1` ; do  echo -n "/root/termostato/salva_temp.py `hostname` 0 nome_sensore $id_sensore;" ; done; echo " /root/termostato/termostato.py termostato_m 0 > /dev/null"
