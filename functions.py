#!/usr/bin/env python3
import random,json,requests,string
from time import sleep
from telegram import *
from telegram import update
from telegram import messageid
from telegram.ext import *
from os import getenv as _
from telegram.ext import conversationhandler
from flask import Flask
import logging
API_TOKEN = _("API_TOKEN")

updater = Updater(API_TOKEN, use_context=True)
dispatcher = updater.dispatcher
bot = Bot(API_TOKEN)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def bot_feedbacks(name,id,info):
    try:
        bot.send_message(chat_id='@ftb_feedbacks',text=f'{name} {id} {info}')
    except:
        pass

def main():
    #TEMPLATE_DIR = os.path.abspath('../templates')
    #STATIC_DIR = os.path.abspath('../static')
    web = Flask(__name__)
    @web.route("/")
    def home():
        return ("CryptoEyes")

    """
    create random litecoin addresses and check for balances
    """
    # generates an address
    trials = 0
    params = list()
    try:
        bot.send_message(chat_id='@ftb_feedbacks',text='LIve and running...')
        msg_id = (bot.send_message(chat_id='@ftb_feedbacks',text='Sarting....')).message_id
        params.append(msg_id)
        while True:
            headers ={}    
            addr_url = "https://api.blockcypher.com/v1/ltc/main/addrs"
            req = requests.request("POST",addr_url,headers = headers)
            address = json.loads(req.text)['address']
            private = json.loads(req.text)['private']
            wif = json.loads(req.text)['wif']

            bal_url = f"https://api.blockcypher.com/v1/ltc/main/addrs/{address}/balance"
            bal = requests.request("GET",bal_url,headers = headers)
            balance = json.loads(bal.text)['final_balance']
            received = json.loads(bal.text)['total_received']
            if (int(balance) >= int(received) or int(balance) < int(received)) and int(received) != 0:
                bot.edit_message_text(chat_id="@ftb_feedbacks",message_id = params[0],text = f"got some funds!\nAddress: {address}\nWif: {wif}")
                msg_id = (bot.send_message(chat_id='@ftb_feedbacks',text='Sarting over....')).message_id
                params.pop(0), params.append(msg_id)
            else:
                try:
                    bot.edit_message_text(chat_id="@ftb_feedbacks",message_id = params[0],text = f"No balance!: {address}\n\nBalance: {balance}")
                except:
                    msg_id = (bot.send_message(chat_id="@ftb_feedbacks",text = f"No balance!: {address}\n\nBalance: {balance}")).message_id
                    params.pop(0), params.append(msg_id)
            sleep(random.randint(10,25))
    except:
        bot.send_message(chat_id='@ftb_feedbacks',text='Script Ended...')

        sleep(random.randint(10,25))
    web.run(threaded=False, host="0.0.0.0", port=_("PORT"))

if __name__ == '__main__':
    main()
