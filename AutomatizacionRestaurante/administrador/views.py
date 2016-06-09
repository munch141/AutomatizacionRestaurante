# -*- coding: utf-8 -*-

from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from cuentas.models import Cliente


def home(request):
    return render(request, 'administrador/home.html')

def ver_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'administrador/ver_clientes.html', {'clientes': clientes})

def detalles_cliente(request, username):
    try:
        cliente = User.objects.get(username=username).cliente
    except:
        cliente = None
    return render(request, 'administrador/detalles_cliente.html', {'cliente': cliente})

