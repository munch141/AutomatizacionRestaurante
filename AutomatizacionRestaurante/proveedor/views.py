# -*- coding: utf-8 -*-

from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import inlineformset_factory, formset_factory
from django.contrib.auth.models import User

from administrador.models import Ingrediente,Ingrediente_inventario

from .models import Proveedor, Inventario
from .forms import EditarPerfilForm, AgregarIngredienteForm, \
                   ElegirIngredientesForm, DetallesIngredienteInventarioForm, \
                   IngredienteInventarioFormSetHelper, EliminarIngredientesForm


@login_required(login_url=reverse_lazy('login'))
def home(request):
    return render(
        request, 'proveedor/home.html',
        {'user': request.user,
         'inventario': request.user.inventario.ingrediente_inventario_set.all()})


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

			messages.success(request, '✓ Se agregó ingrediente "%s"' % nombre)

			return redirect(reverse('elegir_ingredientes_inventario'))
	else:
		form = AgregarIngredienteForm()
	return render(request, 'proveedor/agregar_ingrediente.html', {'form': form})


@login_required(login_url=reverse_lazy('login'))
def elegir_ingredientes_inventario(request):
    if request.method == 'POST':
        form = ElegirIngredientesForm(request.POST)

        if form.is_valid():
            ingredientes = [i.nombre for i in form.cleaned_data['ingredientes']]
            request.session['ingredientes'] = ingredientes

            return redirect(reverse('detalles_ingredientes_inventario'))
    else:
        form = ElegirIngredientesForm()
    return render(
        request,
        'proveedor/elegir_ingredientes.html',
        {'form':form, 'user': request.user})


@login_required(login_url=reverse_lazy('login'))
def detalles_ingredientes_inventario(request):
    user = request.user
    ingredientes = []

    for nombre in request.session['ingredientes']:
        ingrediente = Ingrediente.objects.get(nombre=nombre)
        try:
            i = Ingrediente_inventario.objects.get(
                inventario=user.inventario,
                ingrediente=ingrediente)
        except:
            i = Ingrediente_inventario(
                inventario=user.inventario,
                ingrediente=ingrediente,
                cantidad=0,
                precio=0)
        ingredientes.append(i)
    
    IngredienteFormset = formset_factory(
        DetallesIngredienteInventarioForm, extra=0)

    if request.method == 'POST':
        formset = IngredienteFormset(request.POST)

        if formset.is_valid():
            n = 0
            for form in formset.cleaned_data:
                ingrediente = ingredientes[n].ingrediente
                precio = form['precio']

                ing, created = Ingrediente_inventario.objects.update_or_create(
                    inventario=user.inventario,
                    ingrediente=ingrediente,
                    cantidad=0,
                    precio=precio)

                ing.save()
                n += 1
            messages.success(request, '✓ Se actualizó el inventario!')
            return redirect(reverse('editar_inventario'))
        helper = IngredienteInventarioFormSetHelper()

    else:
        initial_data = []
        for i in ingredientes:
            initial_data.append(
                {'ingrediente': i.ingrediente, 'precio': i.precio})
        formset = IngredienteFormset(initial=initial_data)
        helper = IngredienteInventarioFormSetHelper()

    return render(
        request,
        'proveedor/detalles_ingredientes.html',
        {'formset': formset, 'helper': helper, 'user': user})


@login_required(login_url=reverse_lazy('login'))
def editar_inventario(request):
    user = request.user
    ingredientes = [i for i in user.inventario.ingrediente_inventario_set.all()]    
    IngredienteFormset = formset_factory(
        DetallesIngredienteInventarioForm, extra=0)

    if request.method == 'POST':
        formset = IngredienteFormset(request.POST)

        if formset.is_valid():
            n = 0
            for form in formset:
                ingrediente = ingredientes[n].ingrediente
                precio = form.cleaned_data['precio']

                i = Ingrediente_inventario.objects.get(ingrediente=ingrediente)
                i.precio = precio
                i.save()

                n += 1
            messages.success(request, '✓ Se actualizó el inventario!')
            return redirect(reverse('home_proveedor'))

    else:
        if ingredientes == []:
            formset = None
            helper = None
        else:
            initial_data = []
            for i in ingredientes:
                initial_data.append(
                    {'ingrediente': i.ingrediente,
                     'cantidad': i.cantidad,
                     'precio': i.precio})
            formset = IngredienteFormset(initial=initial_data)
            helper = IngredienteInventarioFormSetHelper()

    return render(
        request,
        'proveedor/editar_inventario.html',
        {'formset': formset, 'helper': helper, 'user': user})


@login_required(login_url=reverse_lazy('login'))
def eliminar_ingredientes_inventario(request):
    inventario = request.user.inventario
    queryset = inventario.ingrediente_inventario_set.all()

    if request.method == 'POST':
        form = EliminarIngredientesForm(queryset, request.POST)

        if form.is_valid():
            eliminados = []
            ingredientes = form.cleaned_data['ingredientes']
            for i in ingredientes:
                eliminados.append(i.ingrediente.nombre)
                i.delete()

            messages.success(request, '✓ Se eliminaron los ingredientes "%s"' % eliminados)
            return redirect(reverse('editar_inventario'))
    else:
        form = EliminarIngredientesForm(queryset)

    return render(
        request,
        'proveedor/eliminar_ingredientes.html',
        {'form':form, 'user': request.user})
