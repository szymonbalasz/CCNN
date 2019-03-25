from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from .forms import SignUpForm, EditProfileForm

def loginUser(request):
	if request.method ==  "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ('You Have Successfully Logged In'))
			return redirect('home')
		else:
			messages.success(request, ('Error. Invalud Username/Password'))
			return redirect('login')
	else:
		return render(request, 'auth/login.html', {})

def logoutUser(request):
	logout(request)
	messages.success(request, ('You Have Been Logged Out'))
	return redirect('home')

def registerUser(request):
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(request, username=username, password=password)
			login(request, user)
			messages.success(request, ('You Have Successfully Registered' + user.id))
			return redirect('home')
	else:
		form = SignUpForm()
	context = {'form' : form}
	return render(request, 'auth/register.html', context)

def editProfile(request):
	if request.method == "POST":
		form = EditProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, ('Profile Successfully Updated'))
			return redirect('home')
	else:
		form = EditProfileForm(instance=request.user)

	context = {'form' : form}
	return render(request, 'auth/editProfile.html', context)


def changePassword(request):
	if request.method == "POST":
		form = PasswordChangeForm(data=request.POST, user=request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, ('Password Successfully Updated'))
			return redirect('home')
	else:
		form = PasswordChangeForm(user=request.user)

	context = {'form' : form}
	return render(request, 'auth/changePassword.html', context)