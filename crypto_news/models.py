from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

class Wallet(models.Model):
	owner = models.OneToOneField(User, on_delete=models.CASCADE)
	wallet = JSONField(default=dict)

	def __str__(self):
		return "%s's wallet" % self.owner.username

