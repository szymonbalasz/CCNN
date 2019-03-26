from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from . import cryptoAPI
from .forms import AddCoinForm
from .models import Wallet
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def home(request):
	price = cryptoAPI.cPrice()
	news = cryptoAPI.cNews()

	return render(request, 'home.html', {'news' : news, 'price' : price})

def about(request):
	return render(request, 'about.html', {})

@login_required
def addCoin(request):
	if request.method == 'POST':
		form = AddCoinForm(request.POST or None)
		if form.is_valid():
			
			messages.success(request, "Coins Added") 
			return redirect('home')
		else:
			messages.success(request, "Error Adding Coins")
			return render(request, 'coins/addCoin.html', {})
	else:
		return render(request, 'coins/addCoin.html', {})
