#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
import sys
sys.path.append("/home/pi/")
import telegram
from telegram import Updater
import logging
import mytokens

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

# Setup config redis
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
#

r = redis.StrictRedis(host='localhost', port=6379, db=db_id, password='Termostato_2.0')

import os
import subprocess

pid = str(os.getpid())
pidfile = "/var/run/telegram/telegram-bot_" + db_id + ".pid"
#if os.path.isfile(pidfile):
#    print "Processo gia attivo vedi file %s" % pidfile
#    sys.exit()
#else:
file(pidfile, 'w').write(pid)
print pid

import urllib2

try:
   u = urllib2.urlopen("https://telegram.org/")
except Exception as e:
   #inform them that a general error has occurred 
   print ("Errore generico")
   sys.exit(1024)


menu_keyboard = telegram.ReplyKeyboardMarkup([['/accendi_30_min','/spegni_30_min','/auto'],['/dettaglio','/get_rele','/help']])
menu_keyboard.one_time_keyboard=False
menu_keyboard.resize_keyboard=True


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='/start', reply_markup=menu_keyboard)
    bot.sendMessage(update.message.chat_id, text='/help', reply_markup=menu_keyboard)
    bot.sendMessage(update.message.chat_id, text='/accendi_30_min Accende la caldaia per 30 minuti indipendentemente dalla temperatura')
    bot.sendMessage(update.message.chat_id, text='/spegni_30_min Spegne la caldaia per 30 minuti indipendentemente dalla temperatura')
    bot.sendMessage(update.message.chat_id, text='/auto Rimuove accensione e spegnimento forzati e riabilita il funzionamento normale')
    bot.sendMessage(update.message.chat_id, text='/dettaglio Visualizza la situazione attuale')
    bot.sendMessage(update.message.chat_id, text='/get_rele Richiedi lo stato del rele')

def get_rele(bot, update):
    rele=r.lrange("rele",-1,-1)[0]
    if rele == "0":
	s_rele="Spento"
    else:
	s_rele="Acceso"
    bot.sendMessage(update.message.chat_id, text='Stato Rele=' + s_rele)

def forceoff(bot, update):
    rele=r.delete("s_forceon")
    rele=r.set("s_forceoff",1)
    rele=r.expire("s_forceoff",1800)
    rele=r.publish("rele_ch",0)
    rele=r.lset("rele",-1,0)
    bot.sendMessage(update.message.chat_id, text='Forzato spegnimento Rele per 30 minuti')

def forceon(bot, update):
    rele=r.delete("s_forceoff")
    rele=r.set("s_forceon",1)
    rele=r.expire("s_forceon",1800)
    rele=r.publish("rele_ch",1)
    rele=r.lset("rele",-1,0)
    bot.sendMessage(update.message.chat_id, text='Forzata accensione Rele per 30 minuti')

def auto(bot, update):
    print "Auto"
    rele=r.delete("s_forceon")
    rele=r.delete("s_forceoff")
    cmd='sudo /root/termostato/termostato.py ' + db_host + ' ' + db_id
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out = proc.stdout.read()
    bot.sendMessage(update.message.chat_id, text=out)

def dettaglio(bot, update):
    print "dettaglio"
    cmd='sudo /root/termostato/termostato.py ' + db_host + ' ' + db_id
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out = proc.stdout.read()
    bot.sendMessage(update.message.chat_id, text=out)



def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(mytokens.token_string)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("help", help)
    dp.addTelegramCommandHandler("get_rele", get_rele)
    dp.addTelegramCommandHandler("accendi_30_min", forceon)
    dp.addTelegramCommandHandler("spegni_30_min", forceoff)
    dp.addTelegramCommandHandler("auto", auto)
    dp.addTelegramCommandHandler("dettaglio", dettaglio)

    # on noncommand i.e message - echo the message on Telegram
    dp.addTelegramMessageHandler(echo)

    # log all errors
    dp.addErrorHandler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()

