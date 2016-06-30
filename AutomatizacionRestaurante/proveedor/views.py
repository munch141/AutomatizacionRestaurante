# -*- coding: utf-8 -*-

from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import inlineformset_factory, formset_factory
from django.contrib.auth.models import User

from administrador.models import Ingrediente

from .models import Proveedor, Ingrediente_inventario, Inventario
from .forms import EditarPerfilForm, AgregarIngredienteForm, \
                   CrearInventarioForm1, IngredienteInventarioForm, \
                   IngredienteInventarioFormSetHelper


@login_required(login_url=reverse_lazy('login'))
def home(request):
    return render(request, 'proveedor/home.html', {'user': request.user})


@login_required(login_url=reverse_lazy('login'))
def perfil(request):
    return render(request, 'proveedor/perfil.html', {'user': request.user})


@login_required(login_url=reverse_lazy('login'))
def editar_perfil(request):
    inline_formset = inlineformset_factory(
        User, Proveedor, fields=('telefono', 'direccion'), can_delete=False)

    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        formset = inline_formset(request.POST, instance=request.user)

        if form.is_valid():
            created_user = form.save(commit=False)
            formset = inline_formset(
                request.POST, instance=created_user)

            if formset.is_valid():
                created_user.save()
                formset.save()
                messages.success(request, '✓ Se actualizaron los datos!')
                return redirect(reverse('perfil_proveedor'))
    else:
        form = EditarPerfilForm(instance=request.user)
        formset = inline_formset(instance=request.user)
    return render(
        request,
        'proveedor/editar_perfil.html',
        {'user': request.user, 'formset': formset, 'form': form})


@login_required(login_url=reverse_lazy('login'))
def agregar_ingrediente(request):
	if request.method == 'POST':
		form = AgregarIngredienteForm(request.POST)
		if form.is_valid():
			nombre = form.cleaned_data['nombre']
			ingrediente = Ingrediente.objects.create(nombre=nombre)
			ingrediente.save()   

			messages.success(request, '✓ Se agrego ingrediente "%s"' % nombre)       

			return redirect(reverse('crear_inventario_1'))
	else:
		form = AgregarIngredienteForm()
	return render(request, 'proveedor/agregar_ingrediente.html', {'form': form})


@login_required(login_url=reverse_lazy('login'))
def crear_inventario_1(request):
    if request.method == 'POST':
        form = CrearInventarioForm1(request.POST)

        if form.is_valid():
            ingredientes = [i.nombre for i in form.cleaned_data['ingredientes']]
            request.session['ingredientes'] = ingredientes

            return redirect(reverse('crear_inventario_2'))
    else:
        form = CrearInventarioForm1()
    return render(
        request,
        'proveedor/crear_inventario_1.html',
        {'form':form, 'user': request.user})


@login_required(login_url=reverse_lazy('login'))
def crear_inventario_2(request):
    user = request.user
    ingredientes = []

    for nombre in request.session['ingredientes']:
        ingrediente = Ingrediente.objects.get(nombre=nombre)
        try:
            i = Ingrediente_inventario.objects.get(
                inventario=user.inventario,
                ingrediente=ingrediente)
        except:
            i = Ingrediente_inventario.objects.create(
                inventario=user.inventario,
                ingrediente=ingrediente,
                cantidad=0,
                precio=0)
        ingredientes.append(i)
    
    IngredienteFormset = formset_factory(
        IngredienteInventarioForm, extra=0)
    
    initial_data = []
    for i in ingredientes:
        initial_data.append(
            {'ingrediente': i.ingrediente,
             'cantidad': 0,
             'precio': 0})

    formset = IngredienteFormset(initial=initial_data)
    helper = IngredienteInventarioFormSetHelper()

    return render(
        request,
        'proveedor/crear_inventario_2.html',
        {'formset': formset, 'helper': helper, 'user': user})
		
