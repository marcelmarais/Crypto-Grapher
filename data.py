import json
import requests


def requestsBTC():
    btc_price = requests.get("https://api.mybitx.com/api/1/ticker?pair=XBTZAR")
    btc_price = json.loads(btc_price.text)
    btc_price = btc_price['last_trade']
    return float(btc_price)


def requestsETH():
    eth_price = requests.get("https://api.mybitx.com/api/1/ticker?pair=ETHXBT")
    eth_price = json.loads(eth_price.text)
    eth_price = eth_price['last_trade']
    return float(eth_price)


class prices():
    def __init__(self):
        self.BTC = round(requestsBTC(), 2)
        self.ETH = round(self.BTC * requestsETH(), 2)
