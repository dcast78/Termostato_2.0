#!/usr/bin/python
import redis
import time
import calendar
import datetime
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


#Dichiarazione lista con nome giorni della settimana
giorni = ["dom","lun","mar","mer","gio","ven","sab"]
ora=time.strftime("%H")
#div_tempo inidica una unita' di tempo in cui regolare la temperatura e si calcola dividendo un giorno per il numero di step_programmazioni che impostiamo
#86400 sono i secondi in un giorno, se impostiamo step_programmazione a 24 otteniamo 3600 cioe' il numero di secondi che compongono un'ora
n_step_programmazione=48
div_tempo=86400/n_step_programmazione
#Calcolo in quale unita' di tempo sta girando lo script
now = datetime.datetime.now()
midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
seconds_since_midnight = (now - midnight).seconds
#tempo_attuale e' un numero che corrisponde all'ora se ho deciso una programmazione su base oraria (step_programmazione=24) o mezz'ora (step_programmazione=48) ecc....
tempo_attuale=seconds_since_midnight//div_tempo
print ("tempo attuale: "+str(tempo_attuale))
#n_giorno contiene una stringa di tre lettere con il nome del giorno della settimana ricavata dalla lista giorni
n_giorno=giorni[int(datetime.date.today().strftime("%w"))]
#connessione a redis
r = redis.StrictRedis(host='localhost', port=6379, db=db_id, password='Termostato_2.0')
#carico da redis la lista delle stanze
i=0
camere=[]
while i < r.llen("camere"):
        camere.append(r.lrange("camere",i,i)) #Su redis per ottenere lrange ricava il range indicando start e stop degli elementi da leggere, quindi i (indice) va ripetuto due volte
        i = i + 1
print("Camere: " + str(camere))
temperature=[]
i=0
while i < len(camere):
	temperature.append(r.lrange(camere[i][0],-1,-1)) #Per ottenere la stringa corrispondente alla variabile ricavata da redis oltre all'elemento va aggiunto [0] 
	i = i + 1
print("Temperature: " + str(temperature))
#n_setpoint e' la temperatura che il termostato deve mantenere, viene espressa con un carattere G (Giorno),N (Notte), S (Spento)
n_setpoint=r.lindex(n_giorno,tempo_attuale)
print n_giorno + " " + ora + " " + n_setpoint
#stanza e' la camera in cui la temperatura e' da misurare per mantere la temperatura ad esempio giorno cucina, notte camere da letto
stanza=r.lindex("c_"+n_giorno,tempo_attuale)
print stanza
#input contiene il valore dell'ultima lettura di temperatura dal sensore posto in quella stanza
input=r.lrange(stanza,-1,-1)[0]
print "Temperatura attuale nella stanza: " + str(input)
#setpoint e' la temperatura in gradi da raggiungere
setpoint=r.get(n_setpoint+"_max")
print "Temperatura da raggiungere:" + str(setpoint)
r.rpush("setpoint",setpoint)

t_min=r.get(n_setpoint+"_min")
print "Temperatura minima: " + str(t_min)
#Routine termostato
rele=r.lrange("rele",-1,-1)[0]

if float(input) > float(setpoint) :
	rele=0
else:
	if float(input) < float(t_min):
		rele=1

#s_blocc e' un sensore in grado di inibire l'accensione della caldaia o spegnerla se e' accesa, puo' essere ad esempio piazzato su una finestra, se la finestra e' aperta e' inutile accendere la caldaia
s_blocc=r.lrange("s_blocc",-1,-1)[0]
if s_blocc==1:
	rele=0

s_forceoff=r.get("s_forceoff")
if s_forceoff==1:
	rele=0
	print "Spegnimento forzato impostato"

s_forceon=r.get("s_forceon")
if s_forceon==1:
	rele=1
	print "Accensione forzata impostata"

r.rpush("rele",rele)
#pubblica sul canale rele_ch lo stato del rele per i client che hanno sottoscritto il canale con pusub
r.publish("rele_ch", rele)
#p_blocc e' un'uscita utilizzabile per bloccare una perifarica che non deve stare accesa mentre la caldaia e' in funzione 
#r.rpush("p_blocc",not rele)

print ("rele: " + str(rele))
