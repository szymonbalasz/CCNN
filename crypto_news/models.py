from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

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

	def getCoins(self):
		return self.wallet