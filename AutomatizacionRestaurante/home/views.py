from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import LogInForm
from django.contrib.auth import authenticate, login

def perfil(request):
	
	return render(request, 'home/perfil.html')

def LogIn(request):
	if request.method == 'POST':
		form = LogInForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['clave']
			user = authenticate(username=username, password = password)
	
			if user is not None:
				return HttpResponseRedirect('perfil')

	else: 
		form = LogInForm()
	return render(request, 'home/login.html', {'form':form})


