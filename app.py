
import json, config, time, sys, os

from binance.enums import ORDER_TYPE_MARKET
from flask import Flask, request, jsonify, render_template
from binance.client import Client

app = Flask(__name__)

client = Client(config.API_KEY, config.API_SECRET)

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        client.futures_change_leverage(leverage=3)
        order = client.futures_create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return order

@app.route('/')
def welcome():
    return "welcome to the bot, please keep this window open"

@app.route('/webhook', methods=['POST'])
def webhook():
    #print(request.data)
    data = json.loads(request.data)
    
    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return {
            "code": "error",
            "message": "Nice try, invalid passphrase"
        }

    side = data['strategy']['order_action'].upper()
    quantity = data['strategy']['order_contracts']
    sym = data['ticker'].upper()
    order_response = order(symbol=sym, side=side, quantity=quantity)

    if order_response:
        print("order success")
        return {
            "code": "success",
            "message": "order executed"
        }
    else:
        print("order failed")

        return {
            "code": "error",
            "message": "order failed"
        }
