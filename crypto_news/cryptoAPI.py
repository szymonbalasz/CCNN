import requests
import json
from decouple import config
from .models import LatestAPI
from datetime import datetime

def cPrice():
	headers = {
		"X-CMC_PRO_API_KEY" : config('API_KEY')
	}

	priceRequest = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest", headers=headers)
	price = json.loads(priceRequest.content)

	LatestAPI.objects.get(pk=1).setErrorPrices(False)

	if "data" in price:
		LatestAPI.objects.get(pk=1).setPrices(price)
		LatestAPI.objects.get(pk=1).setLastUpdate(datetime.now())
	else:
		price = LatestAPI.objects.get(pk=1).getPrices()
		LatestAPI.objects.get(pk=1).setErrorPrices(True)

	return price



def cNews():
	newsRequest = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
	news = json.loads(newsRequest.content)

	LatestAPI.objects.get(pk=1).setErrorNews(False)

	if "Data" in news:
		LatestAPI.objects.get(pk=1).setNews(news)
	else:
		news = LatestAPI.objects.get(pk=1).getNews()
		LatestAPI.objects.get(pk=1).setErrorNews(True)	


	return news

def cNewsRelevant(tags):
	return tags