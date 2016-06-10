# -*- coding: utf-8 -*-

from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from cuentas.models import Cliente
from .models import Ingrediente, Menu, Plato
from .forms import CrearMenuForm


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

def crear_menu(request):
    if request.method == 'POST':
        form = CrearMenuForm(request.POST)

        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            actual = form.cleaned_data['actual']
            platos = form.cleaned_data['incluye']

            menu = Menu.objects.create(nombre=nombre, actual=actual)
            print(platos)
            menu.incluye.add(platos)
            messages.success(request, '✓ Se creó un nuevo menú "%s"!' % nombre)
            return redirect(reverse('home_administrador'))
    else:
        form = CrearMenuForm()
    return render(request, 'administrador/crear_menu.html', {'form': form})
