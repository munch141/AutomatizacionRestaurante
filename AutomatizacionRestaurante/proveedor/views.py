# -*- coding: utf-8 -*-

from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User

from cuentas.models import Proveedor
from .forms import EditarPerfilForm


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
