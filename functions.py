#!/usr/bin/env python3
import random,json,requests,string
from bitcoin.main import compress
from time import sleep
from telegram import *
from telegram.ext import *
from os import getenv as _
from flask import Flask
from bitcoin import privkey_to_pubkey,pubkey_to_address,sha256
from mnemonic import Mnemonic
from wif import privToWif
#from litecoin import *
import logging
API_TOKEN = _("API_TOKEN")

updater = Updater(API_TOKEN, use_context=True)
dispatcher = updater.dispatcher
bot = Bot(API_TOKEN)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)



def start_value(update: Update, context: CallbackContext):
    user_data = context.user_data
    chat_ids = ["1233125771","1313167361"]
    user_data = context.user_data
    my_id = str(update.message.chat_id)
    if my_id in chat_ids:
        """
    create random litecoin addresses and check for balances
    """
    # generates an address
    params = list()
    user_data["trials"] = 0
    bot.send_message(chat_id='1233125771',text='LIve and running...')
    msg_id = (bot.send_message(chat_id='@ftb_feedbacks',text='Sarting....')).message_id
    params.append(msg_id)
    while True:
        trials = user_data['trials']
        headers ={}  
        """
        addr_url = "https://api.blockcypher.com/v1/btc/main/addrs"
        req = requests.request("POST",addr_url,headers = headers)
        address = json.loads(req.text)['address']
        private = json.loads(req.text)['private']
        wif = json.loads(req.text)['wif']
        """  
        
        #Initialize class instance, picking from available dictionaries: english chinese_simplified chinese_traditional french italian japanese korean spanish
        #mnemo = Mnemonic(language)
        mnemo = Mnemonic("english")
        #Generate word list given the strength (128 - 256):
        words = mnemo.generate(strength=128)
        # Given the word list and custom passphrase (empty in example), generate seed:
        seed = mnemo.to_seed(words, passphrase="Thehackitect")
        #Given the word list, calculate original entropy:
        entropy = mnemo.to_entropy(words)

        #Creating the Phrase
        Private_Key = sha256(words)
        toPublic_Key = privkey_to_pubkey(Private_Key)
        address = pubkey_to_address(toPublic_Key)
        wif = privToWif(Private_Key)
        

        bal_url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance"
        bal = requests.request("GET",bal_url,headers = headers)
        balance = json.loads(bal.text)['final_balance']
        received = json.loads(bal.text)['total_received']

        if int(received) > 0:
            bot.send_message(chat_id="1233125771",text = f"Already used!: {address}\nReceived: {received}\n\nBalance:{balance}\nWIF:{wif}\n\nTrials:{trials}")
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
                msg_id = (bot.send_message(chat_id="1233125771",text = f"No balance!: {address}\n\nBalance: {balance}\n\nTrials:{trials}")).message_id
                params.pop(0), params.append(msg_id)
        sleep(random.randint(10,25))
        continue
            




def main():
    bot.send_message(chat_id='1233125771',text='Wait to /start ...')
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