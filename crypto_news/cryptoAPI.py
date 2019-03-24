import requests
import json

def cPrices():
	priceRequest = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,XRP,BCH,EOS,LTC,XLM,ADA,USDT,MIOTA,TRX&tsyms=USD")
	price = json.loads(priceRequest.content)
	return price

def cNews():
	newsRequest = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
	news = json.loads(newsRequest.content)
	return news