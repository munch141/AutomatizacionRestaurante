# -*- coding: utf-8 -*-

from django.views import generic
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User

# Create your views here.
#@login_required(login_url='/')
def administrador(request):
    return render(request, 'administrador/administrador.html', {'user': request.user})

#@login_required(login_url='/')
def nuevo_menu(request):
    return render(request, 'administrador/administrador.html', {'user': request.user})

#@login_required(login_url='/')
def nuevo_plato(request):
    return render(request, 'administrador/administrador.html', {'user': request.user})
