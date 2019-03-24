from django.shortcuts import render, redirect
from . import cryptoAPI

def home(request):
	price = cryptoAPI.cPrice()
	news = cryptoAPI.cNews()

	return render(request, 'home.html', {'news' : news, 'price' : price})
