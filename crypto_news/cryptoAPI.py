import requests
import json
from decouple import config
from .models import LatestAPI
from datetime import datetime
from django.utils.timezone import get_current_timezone

def cPrice():
	headers = {
		"X-CMC_PRO_API_KEY" : config('API_KEY')
	}

	priceRequest = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest", headers=headers)
	price = json.loads(priceRequest.content)

	LatestAPI.objects.get(pk=1).setErrorPrices(False)

	if "data" in price:
		LatestAPI.objects.get(pk=1).setPrices(price)
		LatestAPI.objects.get(pk=1).setLastUpdate(datetime.now(tz=get_current_timezone()))
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

def topCoins(price):
	topCoins = {}
	count = 1
	while count < 16:
		for prices in price['data']:
			if prices['cmc_rank'] == count:
				topCoins[count] = prices['symbol']
		count += 1
	return topCoins


#news blocks are seperated on home template. each function pulls news from category and excludes if from future pulls

def businessNews(allNews):
	news = {}
	count = 0
	for article in allNews['Data']:
		if 'Business' in article['categories']:
			news[article['id']] = article
			count += 1
			if count == 2:
				return news
	return news

def coinNews(portfolio, allNews, exclude):
	news = {}
	excludedNews = exclude
	count = 0
	for symbol in portfolio:
		for article in allNews['Data']:
			if symbol in article['categories']:
					if article['id'] not in excludedNews:
						news[article['id']] = article
						excludedNews.update(news)
						count += 1
						if count == 9:
							return news
	return news

def miningNews(allNews, exclude):
	news = {}
	excludedNews = exclude
	count = 0
	for article in allNews['Data']:
		if 'Mining' or 'Blockchain' in article['categories']:
			if article['id'] not in excludedNews:
				news[article['id']] = article
				excludedNews.update(news)
				count += 1
				if count == 3:
					return news
	return news

def regulationNews(allNews, exclude):
	news = {}
	excludedNews = exclude
	count = 0
	for article in allNews['Data']:
		if 'Regulation' or 'Trading' in article['categories']:
			if article['id'] not in excludedNews:
				news[article['id']] = article
				excludedNews.update(news)
				count += 1
				if count == 3:
					return news
	return news

def marketNews(allNews, exclude):
	news = {}
	excludedNews = exclude
	count = 0
	for article in allNews['Data']:
		if 'Market' in article['categories']:
			if article['id'] not in excludedNews:
				news[article['id']] = article
				excludedNews.update(news)
				count += 1
				if count == 3:
					return news
	return news

def ICONews(allNews, exclude):
	news = {}
	excludedNews = exclude
	count = 0
	for article in allNews['Data']:
		if 'ICO' or 'Blockchain' in article['categories']:
			if article['id'] not in excludedNews:
				news[article['id']] = article
				excludedNews.update(news)
				count += 1
				if count == 3:
					return news
	return news