from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from . import cryptoAPI
from .forms import AddCoinForm
from .models import Wallet, LatestAPI
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def home(request):
	price = cryptoAPI.cPrice()
	news = cryptoAPI.cNews()
	if request.user.is_authenticated:
		portfolio = request.user.wallet.getCoins()
	else:
		portfolio = {}
	excludedNews = {}
	businessNews = cryptoAPI.businessNews(news)
	excludedNews.update(businessNews)
	coinNews = cryptoAPI.coinNews(portfolio, news, excludedNews)
	excludedNews.update(coinNews)
	miningNews = cryptoAPI.miningNews(news, excludedNews)
	excludedNews.update(miningNews)
	regulationNews = cryptoAPI.regulationNews(news, excludedNews)
	excludedNews.update(regulationNews)
	marketNews = cryptoAPI.marketNews(news, excludedNews)
	excludedNews.update(marketNews)
	ICONews = cryptoAPI.ICONews(news, excludedNews)

	if LatestAPI.objects.get(pk=1).errorPrices:
		messages.success(request, "API Error. Using stored crypto price data from: " + LatestAPI.objects.get(pk=1).getLastUpdate())

	if LatestAPI.objects.get(pk=1).errorNews:
		messages.success(request, "API Error. Using stored crypto news data")

	display = {
		'news' : news,
		'price' : price,
		'portfolio' : portfolio,
		'businessNews' : businessNews,
		'coinNews' : coinNews,
		'miningNews' : miningNews,
		'regulationNews' : regulationNews,
		'marketNews' : marketNews,
		'ICONews' : ICONews
	}

	return render(request, 'home.html', display)

def about(request):
	return render(request, 'about.html', {})

@login_required
def addCoin(request):
	price = cryptoAPI.cPrice()
	if request.method == 'POST':
		form = AddCoinForm(request.POST or None)
		if form.is_valid():
			data = form.cleaned_data
			request.user.wallet.addCoins(data['symbol'], data['amount'])
			messages.success(request, "Coins Added") 
			return redirect('home')
		else:
			messages.success(request, "Error Adding Coins")
			return render(request, 'coins/addCoin.html', {'price' : price})
	else:
		return render(request, 'coins/addCoin.html', {'price' : price})

@login_required
def viewPortfolio(request):
	price = cryptoAPI.cPrice()
	if LatestAPI.objects.get(pk=1).errorPrices:
		messages.success(request, "API Error. Using stored crypto price data from: " + LatestAPI.objects.get(pk=1).getLastUpdate())
	portfolio = request.user.wallet.getCoins()
	return render(request, 'coins/viewPortfolio.html', {'price' : price, 'portfolio' : portfolio})
