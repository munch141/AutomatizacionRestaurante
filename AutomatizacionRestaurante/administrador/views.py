# -*- coding: utf-8 -*-

from decimal import Decimal

from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory, formset_factory

from cliente.models import Cliente
from proveedor.models import Proveedor, Inventario
from .models import Ingrediente, Ingrediente_inventario, Menu, Plato, Tiene
from .forms import CrearMenuForm, CrearPlatoForm, AgregarIngredienteForm,\
                   EditarMenuForm, DetallesIngredientePlatoForm, IngredientePlatoFormSetHelper


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
        inventario = proveedor.usuario.inventario.ingrediente_inventario_set.all()
    except:
        proveedor = None
        inventario = None
    return render(
        request,
        'administrador/detalles_proveedor.html',
        {'proveedor': proveedor, 'inventario': inventario})


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
            contiene = form.cleaned_data['contiene']
                
            request.session['plato_nombre'] = form.cleaned_data['nombre']
            request.session['plato_descripcion'] = form.cleaned_data['descripcion']
            request.session['plato_precio'] = str(form.cleaned_data['precio'])
            request.session['plato_contiene'] = [i.nombre for i in contiene]

            return redirect(reverse('detalles_ingredientes_plato'))
    else:
        form = CrearPlatoForm()

    return render(request, 'administrador/crear_plato.html', {'form': form})


def detalles_ingredientes_plato(request):
    user = request.user
    session = request.session
    contiene = []

    for i in session['plato_contiene']:
        contiene.append(Ingrediente.objects.get(nombre=i))

    print(session['plato_precio'])

    plato = Plato(
        nombre=session['plato_nombre'],
        descripcion=session['plato_descripcion'],
        precio=Decimal(session['plato_precio']),
        disponible=False)

    
    IngredienteFormset = formset_factory(
        DetallesIngredientePlatoForm, extra=0)

    if request.method == 'POST':
        formset = IngredienteFormset(request.POST)

        if formset.is_valid():
            n = 0
            for form in formset.cleaned_data:
                requiere = form['requiere']
                Tiene.objects.create(
                    plato=plato, ingrediente=contiene[n], requiere=requiere)
                n += 1

            plato.save()
            messages.success(request, '✓ Se creó el plato "%s"!' % plato.nombre)
            return redirect(reverse('home_administrador'))
        helper = IngredientePlatoFormSetHelper()

    else:
        initial_data = []
        for i in contiene:
            initial_data.append(
                {'ingrediente': i, 'requiere': 0})
        formset = IngredienteFormset(initial=initial_data)
        helper = IngredientePlatoFormSetHelper()

    return render(
        request,
        'administrador/detalles_ingredientes_plato.html',
        {'formset': formset, 'helper': helper, 'user': user})


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
        tiene = Tiene.objects.filter(plato=plato)
        print(tiene)
    except:
        plato = None
    return render(
        request,
        'administrador/detalles_plato.html',
        {'plato': plato, 'tiene':tiene})

def ver_ingredientes(request):
    ingredientes = Ingrediente.objects.all()
    return render(request, 'administrador/ver_ingredientes.html', {'ingredientes': ingredientes})

def ver_inventario(request):
    user = request.user
    ingredientes = user.inventario.ingrediente_inventario_set.all()
    return render(request, 'administrador/ver_inventario.html', {'ingredientes': ingredientes})
