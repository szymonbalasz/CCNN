from django.shortcuts import render, redirect
from . import cryptoAPI

def home(request):
	price = cryptoAPI.cPrices()
	news = cryptoAPI.cNews()

	return render(request, 'home.html', {'news' : news, 'price' : price})
