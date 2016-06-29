# -*- coding: utf-8 -*-

from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User

from administrador.models import Ingrediente

from .models import Proveedor, Inventario
from .forms import EditarPerfilForm, AgregarIngredienteForm, CrearInventarioForm


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

			return redirect(reverse('crear_inventario'))
	else:
		form = AgregarIngredienteForm()
	return render(request, 'proveedor/agregar_ingrediente.html', {'form': form})


@login_required(login_url=reverse_lazy('login'))
def crear_inventario(request):
    if request.method == 'POST':
        form = CrearInventarioForm(request.POST)

        if form.is_valid():
            ingredientes = form.cleaned_data['ingredientes']

            inventario = Inventario.objects.create(usuario=request.user)
            inventario.ingredientes.add(ingredientes)
            i = [ingrediente.nombre for ingrediente in ingredientes]
            messages.success(
                request,
                '✓ Se creó el inventario con los ingredientes "%s"' % str(i))
            return redirect(reverse('home_proveedor'))
    else:
        form = CrearInventarioForm()
    return render(request, 'proveedor/crear_inventario.html', {'form':form, 'user': request.user})
		
