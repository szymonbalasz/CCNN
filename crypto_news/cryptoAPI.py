import requests
import json
from decouple import config

def cPrice():
	headers = {
		"X-CMC_PRO_API_KEY" : config('API_KEY')
	}

	priceRequest = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest", headers=headers)
	price = json.loads(priceRequest.content)

	if "data" in price:
		price = price["data"]
	else:
		price = {}

	return price



def cNews():
	newsRequest = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
	news = json.loads(newsRequest.content)
	return news

def cNewsRelevant(tags):
	return tags