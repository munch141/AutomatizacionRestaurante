# -*- coding: utf-8 -*-

from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User

from .models import Cliente
from .models import BilleteraElectronica
from .forms import EditarPerfilForm, CrearBilleteraForm


@login_required(login_url=reverse_lazy('login'))
def home(request):
    return render(request, 'cliente/home.html', {'user': request.user})


@login_required(login_url=reverse_lazy('login'))
def perfil(request):
    return render(request, 'cliente/perfil.html', {'user': request.user})


@login_required(login_url=reverse_lazy('login'))
def editar_perfil(request):
    inline_formset = inlineformset_factory(
        User, Cliente, fields=('telefono',), can_delete=False)

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
                return redirect(reverse('perfil_cliente'))
    else:
        form = EditarPerfilForm(instance=request.user)
        formset = inline_formset(instance=request.user)
    return render(
        request,
        'cliente/editar_perfil.html',
        {'user': request.user, 'formset': formset, 'form': form})

@login_required(login_url=reverse_lazy('login'))
def crear_billetera(request):
	if request.method == 'POST':
		form = CrearBilleteraForm(request.POST)
		if form.is_valid():
			pin = form.cleaned_data['pin']
			billetera = BilleteraElectronica.objects.create(
                usuario=request.user.cliente, pin=pin)
			billetera.save()

			messages.success(request, '✓ Se ha creado su billetera')       

			return redirect(reverse('home_cliente'))
	else:
		form = CrearBilleteraForm()
	return render(request, 'cliente/crear_billetera.html', {'form': form})
