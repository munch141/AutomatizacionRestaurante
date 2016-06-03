# -*- coding: utf-8 -*-

from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import RegistroClienteForm, RegistroProveedorForm
from .models import Cliente, Proveedor

app_name = 'registro'


def usuario_registrado(request):
    return render(request, 'registro/exito.html')


def registro_cliente(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['clave'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['nombre'],
                last_name=form.cleaned_data['apellido']
            )
            perfil = Cliente(
                usuario=user,
                ci=form.cleaned_data['ci'],
                fecha_nacimiento=form.cleaned_data['fecha_nacimiento'],
                sexo=form.cleaned_data['sexo'],
                telefono=form.cleaned_data['telefono']
            )
            user.save()
            perfil.save()
            messages.success(request, 'Registro Exitoso!')
            return redirect(reverse('login'))
    else:
        form = RegistroClienteForm()
    return render(request, 'registro/registro.html', {'form': form})

def registro_proveedor(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['clave'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['nombre'],
                last_name=form.cleaned_data['apellido']
            )
            perfil = Proveedor(
                usuario=user,
                rif=form.cleaned_data['rif'],
                telefono=form.cleaned_data['telefono'],
                direccion=form.cleaned_data['direccion']
            )
            user.save()
            perfil.save()
            messages.success(request, 'Registro Exitoso!')
            return redirect(reverse('exito'))
    else:
        form = RegistroClienteForm()
    return render(request, 'registro/registro.html', {'form': form})