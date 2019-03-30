from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from . import cryptoAPI
from .forms import AddCoinForm
from .models import Wallet, LatestAPI
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . import charts


def home(request):
	#cryptoAPI.cPrice() and cNews() returns either the latest or stored api data. adds to loading time of page
	price = cryptoAPI.cPrice()
	topCoins = cryptoAPI.topCoins(price)
	news = cryptoAPI.cNews()
	
	if request.user.is_authenticated:
		portfolio = request.user.wallet.getCoins()
	else:
		portfolio = {}
	
	excludedNews = {}

	#with each news block on the home.html page we exclude whatever news was already assigned to previous slots
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
		'ICONews' : ICONews,
		'topCoins' : topCoins
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
			return redirect('viewPortfolio')
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

	#bokeh charts. using the components feature from the embedded library. haven't found a way to use the heroku
	#free dynos with gunicorn and bokeh running at the same time. solution is a bit slower but for this size website
	#it isn't noticable
	coinChart = charts.pieCoins(portfolio)
	valueChart = charts.pieValue(portfolio, price)
	
	display = {
		'price' : price,
		'portfolio' : portfolio,
		'coinChart' : coinChart,
		'valueChart' : valueChart
	}
	return render(request, 'coins/viewPortfolio.html', display)

@login_required
def editPortfolio(request, symbol):
	#symbol is placed in the url path. user can direcly edit a coin by going directly to editPortfolio/coin page
	portfolio = request.user.wallet.getCoins()
	amount = portfolio[symbol]
	if request.method == 'POST':
		form = AddCoinForm(request.POST or None)
		if form.is_valid():
			request.user.wallet.editCoins(symbol, form.cleaned_data['amount'])
			
			#the editCoins member function on the model deletes the coin when amound entered is 0 or less
			#on the template the user is unable to enter a value of <= 0. Deleting is dependent on button
			if form.cleaned_data['amount'] > 0:
				messages.success(request, ('Coin Successfully Edited'))
			else:
				messages.success(request, ('Coin Deleted'))
			return redirect('viewPortfolio')
		else:
			messages.success(request, ('Error Editing Coin'))
			return render(request, 'coins/editPortfolio.html', {'symbol' : symbol, 'amount' : amount})

	else:
		return render(request, 'coins/editPortfolio.html', {'symbol' : symbol, 'amount' : amount})