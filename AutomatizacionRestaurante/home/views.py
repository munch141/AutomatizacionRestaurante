from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect

from .forms import LogInForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

@login_required
def perfil(request):
	return render_to_response('home/perfil.html', {'user':request.user})

def LogIn(request):
	if request.method == 'POST':
		form = LogInForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['clave']
			user = authenticate(username=username, password = password)
	
			if user is not None:
				login(request, user)
				return HttpResponseRedirect('perfil')

	else: 
		form = LogInForm()
	return render(request, 'home/login.html', {'form':form})


