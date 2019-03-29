from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from datetime import datetime

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

	def populate(self):
		self.wallet = {
			"BTC": 0.78, 
			"EOS": 200.0, 
			"ETH": 48.75, 
			"LTC": 178.56, 
			"XLM": 2500.0, 
			"ZEC": 270.0, 
			"DOGE": 100.0
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