from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def index(request):
	pass

def logout_user(request):
	logout(request)
	return redirect('/')

def register(request):
	context = {
		'form':UserRegistrationForm(),
	}
	return render(request, 'users/register.html',context)

def create_user(request):
	errors = {}
	if request.POST['password2'] != request.POST['password1']:
		errors['password_mismatch'] = "Passwords do not match!"
		for key, value in errors.items():
				messages.error(request, value)
		return redirect('register')
	else:
		User.objects.create_user(request.POST['username'],
								request.POST['email'],
								request.POST['password1'],)
		return redirect('/')

def login_user(request):

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		print(user)
		if user is not None:
			login(request, user)
			return redirect('/')
		else:
			errors = {}
			errors['login_failed'] = 'Login Failed'
			for key, value in errors.items():
					messages.error(request, value)
			return redirect('login_user')
	else:
		context = {
			'form':AuthenticationForm()
		}
		return render(request, 'users/login.html', context)

