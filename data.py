import json
import requests


def api_data():
    btc_data = requests.get("https://api.mybitx.com/api/1/ticker?pair=XBTZAR")

    btc_data = json.loads(btc_data.text)

    btc_price = round(float(btc_data.get('last_trade')), 2)

    time = btc_data.get('timestamp')
    keyStore = {"btc_price": btc_price, "Timestamp": time}
    
    return keyStore
