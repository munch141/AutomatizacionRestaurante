# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic.edit import FormView

from .forms import RegistroClienteForm
from .models import Cliente

from .forms import RegistroProveedorForm
from .models import Proveedor

app_name = 'registro'


def usuarioRegistrado(request):
    return render(request, 'registro/exito.html')


class registroCliente(FormView):
    template_name = 'registro/registroCliente.html'
    form_class = RegistroClienteForm
    success_url = '/registro/registroCliente/exito/'

    def form_valid(self, form):
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
        return super(registroCliente, self).form_valid(form)


class registroProveedor(FormView):
    template_name = 'registro/registroProveedor.html'
    form_class = RegistroProveedorForm
    success_url = '/registro/registroProveedor/exito/'

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['clave'],
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['nombre'],
            last_name=''
        )
        perfil = Proveedor(
            usuario=user,
            rif=form.cleaned_data['rif'],
            telefono=form.cleaned_data['telefono'],
            direccion=form.cleaned_data['direccion']
        )
        user.save()
        perfil.save()
        return super(registroProveedor, self).form_valid(form)
