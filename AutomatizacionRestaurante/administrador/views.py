# -*- coding: utf-8 -*-

from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from cliente.models import Cliente
from .models import Ingrediente, Menu, Plato
from .forms import CrearMenuForm, CrearPlatoForm, AgregarIngredienteForm


def home(request):
    try:
        menu_actual = Menu.objects.get(actual=True)
    except:
        menu_actual = None
    return render(request, 'administrador/home.html', {'menu_actual': menu_actual})

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
                
            for p in platos:
                plato = Plato.objects.get(nombre=p.nombre)
                menu.incluye.add(plato)

            messages.success(request, '✓ Se creó un nuevo menú "%s"!' % nombre)
            return redirect(reverse('home_administrador'))
    else:
        form = CrearMenuForm()
    return render(request, 'administrador/crear_menu.html', {'form': form})

def crear_plato(request):
    if request.method == 'POST':
        form = CrearPlatoForm(request.POST)

        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            precio = form.cleaned_data['precio']
            ingredientes = form.cleaned_data['contiene']

            plato = Plato.objects.create(
                nombre=nombre, descripcion=descripcion, precio=precio)
                
            for i in ingredientes:
                ingrediente = Ingrediente.objects.get(nombre=i.nombre)
                plato.contiene.add(ingrediente)
                
            messages.success(request, '✓ Se creó un nuevo plato "%s"!' % nombre)
            return redirect(reverse('home_administrador'))
    else:
        form = CrearPlatoForm()
    return render(request, 'administrador/crear_plato.html', {'form': form})


def agregar_ingrediente(request):
    if request.method == 'POST':
        form = AgregarIngredienteForm(request.POST)

        if form.is_valid():
            nombre = form.cleaned_data['nombre']

            ingrediente = Ingrediente.objects.create(nombre=nombre)
                
            messages.success(request, '✓ Se agregó el ingrediente "%s"!' % nombre)
            return redirect(reverse('home_administrador'))
    else:
        form = AgregarIngredienteForm()
    return render(request, 'administrador/agregar_ingrediente.html', {'form': form})


def ver_menus(request):
    menus = Menu.objects.all()
    return render(request, 'administrador/ver_menus.html', {'menus': menus})

def detalles_menu(request, nombre):
    try:
        menu = Menu.objects.get(nombre=nombre)
    except:
        menu = None
    return render(request, 'administrador/detalles_menu.html', {'menu': menu})
