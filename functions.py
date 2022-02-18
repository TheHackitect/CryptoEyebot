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


def start_value(update: Update, context: CallbackContext):
    """
    create random litecoin addresses and check for balances
    """
    user_data = context.user_data
    chat_ids = ["1233125771","1313167361"]
    user_data = context.user_data
    my_id = str(update.message.chat_id)
    # generates an address
    params = list()
    user_data["trials"] = 0
    bot.send_message(chat_id='1233125771',text='Live and running...')
    msg_id = (bot.send_message(chat_id='@ftb_feedbacks',text='Sarting....')).message_id
    params.append(msg_id)
    while True:
        try:
            trials = user_data['trials']
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


            if int(received) > 0:
                bot.send_message(chat_id="1233125771",text = f"Already used!: {address}\n\Received: {received}\n\nWIF:{wif}\n\nTrials:{trials}")
            if (int(balance) >= int(received) or int(balance) < int(received)) and int(received) != 0:
                cur_trials = int(trials)+1
                user_data['trials'] = cur_trials
                bot.edit_message_text(chat_id="1233125771",message_id = params[0],text = f"got some funds!\nAddress: {address}\nWif: {wif}\n\nTrials:{trials}")
                msg_id = (bot.send_message(chat_id='1233125771',text='Sarting over....')).message_id
                params.pop(0), params.append(msg_id)
            else:
                cur_trials = int(trials)+1
                user_data['trials'] = cur_trials
                try:
                    bot.edit_message_text(chat_id="1233125771",message_id = params[0],text = f"No balance!: {address}\n\nBalance: {balance}\n\nTrials:{trials}")
                except:
                    msg_id = (bot.s.end_message(chat_id="1233125771",text = f"No balance!: {address}\n\nBalance: {balance}\n\nTrials:{trials}")).message_id
                    params.pop(0), params.append(msg_id)
            sleep(random.randint(10,25))
        except:
            pass
        continue


def main():
    start_handle = CommandHandler('start', start_value)
    dispatcher.add_handler(start_handle)
    updater.start_polling()

    web = Flask(__name__)
    @web.route("/")
    def home():
        return ("CryptoEyes")
    web.run(threaded=False, host="0.0.0.0", port=_("PORT"))
    updater.idle()

    
    

if __name__ == '__main__':
    main()
