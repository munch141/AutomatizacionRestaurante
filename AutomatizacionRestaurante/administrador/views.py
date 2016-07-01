# -*- coding: utf-8 -*-

from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory

from cliente.models import Cliente
from proveedor.models import Proveedor, Inventario
from .models import Ingrediente, Ingrediente_inventario, Menu, Plato
from .forms import CrearMenuForm, CrearPlatoForm, AgregarIngredienteForm, EditarMenuForm


def home(request):
    try:
        menu_actual = Menu.objects.get(actual=True)
    except:
        menu_actual = None

    return render(request, 'administrador/home.html', {'menu_actual': menu_actual})

def ver_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'administrador/ver_clientes.html', {'clientes': clientes})

def ver_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'administrador/ver_proveedores.html', {'proveedores': proveedores})


def detalles_cliente(request, username):
    try:
        cliente = User.objects.get(username=username).cliente
    except:
        cliente = None
    return render(request, 'administrador/detalles_cliente.html', {'cliente': cliente})

def detalles_proveedor(request, username):
    try:
        proveedor = User.objects.get(username=username).proveedor
    except:
        proveedor = None
    return render(request, 'administrador/detalles_proveedor.html', {'proveedor': proveedor})


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
    user = request.user
    inventario = user.inventario

    if request.method == 'POST':
        form = CrearPlatoForm(request.POST)

        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            precio = form.cleaned_data['precio']
            ingredientes = form.cleaned_data['contiene']

            plato = Plato.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                disponible=False)
                
            for ingrediente in ingredientes:
                try:
                    i = inventario.ingrediente_inventario_set.get(
                        ingrediente=ingrediente)
                except:
                    ingrediente = Ingrediente_inventario.objects.create(
                        inventario=inventario,
                        ingrediente=ingrediente,
                        cantidad=0,
                        precio=0)

                plato.contiene.add(i)
            plato.esta_disponible(inventario)
                
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

def editar_menu(request, nombre):
    menu = Menu.objects.get(nombre=nombre)
    
    if request.method == 'POST':

        form = EditarMenuForm(request.POST, instance=menu)

        if form.is_valid():
            n_nombre = form.cleaned_data['nombre']
            actual = form.cleaned_data['actual']
            platos = form.cleaned_data['incluye']


            menu.nombre = n_nombre
            menu.actual = actual
            menu.save()

            menu.incluye.clear()
            for plato in platos:
                p = Plato.objects.get(nombre=plato.nombre)
                menu.incluye.add(p)
            messages.success(
                request, '✓ Se actualizó el menú "%s"!' % menu.nombre)
            return redirect(reverse('home_administrador'))
            
    else:
        form = EditarMenuForm(instance=menu)
    return render(
        request, 'administrador/editar_menu.html', {'menu': menu, 'form': form})


def ver_platos(request):
    platos = Plato.objects.all()
    return render(request, 'administrador/ver_platos.html', {'platos': platos})


def detalles_plato(request, nombre):
    try:
        plato = Plato.objects.get(nombre=nombre)
    except:
        plato = None
    print(nombre)
    return render(request, 'administrador/detalles_plato.html', {'plato': plato})

def ver_ingredientes(request):
    ingredientes = Ingrediente.objects.all()
    return render(request, 'administrador/ver_ingredientes.html', {'ingredientes': ingredientes})

def ver_inventario(request):
    user = request.user
    ingredientes = user.inventario.ingrediente_inventario_set.all()
    return render(request, 'administrador/ver_inventario.html', {'ingredientes': ingredientes})








    