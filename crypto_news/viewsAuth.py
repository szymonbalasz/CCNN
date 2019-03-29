from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from .forms import SignUpForm, EditProfileForm
from django.contrib.auth.decorators import login_required
from .models import Wallet

def loginUser(request):
	if request.user.is_authenticated:
		messages.success(request, ('Already Logged In'))
		return redirect('home')
	if request.method ==  "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			if user.username == "TestAccount":
				user.wallet.populate()
				messages.success(request, ('Demo account portfolio will be reset after each session'))
			messages.success(request, ('You Have Successfully Logged In'))
			return redirect('home')
		else:
			messages.success(request, ('Error. Invalud Username/Password'))
			return render(request, 'auth/login.html', {})
	else:
		return render(request, 'auth/login.html', {})

@login_required
def logoutUser(request):
	logout(request)
	messages.success(request, ('You Have Been Logged Out'))
	return redirect('home')

def registerUser(request):
	if request.user.is_authenticated:
		messages.success(request, ('Already Logged In'))
		return redirect('home')
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()			
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(request, username=username, password=password)
			login(request, user)
			newWallet = Wallet(owner = request.user)
			newWallet.save()
			messages.success(request, ('You Have Successfully Registered'))
			return redirect('home')
	else:
		form = SignUpForm()
	context = {'form' : form}
	return render(request, 'auth/register.html', context)

@login_required
def editProfile(request):
	if request.method == "POST":
		form = EditProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			if request.user.username == "TestAccount":
				messages.success(request, ("Demo account details can't be changed"))
				return redirect('home')
			form.save()
			messages.success(request, ('Profile Successfully Updated'))
			return redirect('home')
	else:
		form = EditProfileForm(instance=request.user)

	context = {'form' : form}
	return render(request, 'auth/editProfile.html', context)


@login_required
def changePassword(request):
	if request.method == "POST":
		form = PasswordChangeForm(data=request.POST, user=request.user)
		if form.is_valid():
			if request.user.username == "TestAccount":
				messages.success(request, ("Demo account details can't be changed"))
				return redirect('home')
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, ('Password Successfully Updated'))
			return redirect('home')
	else:
		form = PasswordChangeForm(user=request.user)

	context = {'form' : form}
	return render(request, 'auth/changePassword.html', context)