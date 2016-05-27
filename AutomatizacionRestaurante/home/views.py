from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def home(request):
	return render_to_response('home/home.html', {'user':request.user})

@login_required
def perfil(request):
	return render_to_response('home/perfil.html', {'user':request.user})