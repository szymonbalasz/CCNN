from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from datetime import datetime

#extensive use of setters and getters functions. a byproduct from my C++ background. likely a bad habbit in py

class Wallet(models.Model):
	owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
	wallet = JSONField(default=dict)

	def __str__(self):
		return "%s's wallet" % self.owner.username

	def addCoins(self, symbol, amount):
		if symbol in self.wallet:
			self.wallet[symbol] += amount
			self.save()
		else:
			self.wallet[symbol] = amount
			self.save()

	def editCoins(self, symbol, amount):
		if amount > 0:
			self.wallet[symbol] = amount
		else:
			del self.wallet[symbol]
		self.save()

	def getCoins(self):
		return self.wallet

	#arbitrarily decided to ensure somewhat interesting distribution, especially on pie chart
	def populate(self):
		self.wallet = {
			"BTC": 0.7878, 
			"EOS": 200.0, 
			"ETH": 31.751, 
			"LTC": 78.563, 
			"XLM": 1300.0, 
			"ZEC": 129.11, 
			"DOGE": 1000.0,
			"BSV": 40,
			"DASH": 18.4,
			"USDT": 580
			}
		self.save()

class LatestAPI(models.Model):
	prices = JSONField(default=dict)
	news = JSONField(default=dict)
	errorPrices = models.BooleanField(default=False)
	errorNews = models.BooleanField(default=False)
	lastUpdate = models.DateTimeField(default=datetime.now)

	def __str__(self):
		return "LatestAPI. ID: %s" % self.id

	def setPrices(self, priceAPI):
		self.prices = priceAPI
		self.save()

	def setNews(self, newsAPI):
		self.news = newsAPI
		self.save()

	def getPrices(self):
		return self.prices

	def getNews(self):
		return self.news

	def getErrorPrices(self):
		return self.errorPrices

	def getErrorNewsself():
		return self.errorNews

	def setErrorPrices(self, toggle):
		self.errorPrices = toggle
		self.save()

	def setErrorNews(self, toggle):
		self.errorNews = toggle
		self.save()

	def setLastUpdate(self, date):
		self.lastUpdate = date
		self.save()

	def getLastUpdate(self):
		lastUpdate = str(self.lastUpdate)
		return lastUpdate