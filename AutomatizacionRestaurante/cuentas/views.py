# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import generic

from AutomatizacionRestaurante.decorators import login_check
from .forms import LoginForm, RegistroClienteForm, RegistroProveedorForm
from .models import Cliente, Proveedor

app_name = 'cuentas'


@login_check
def usuario_registrado(request):
    return render(request, 'cuentas/exito.html')


@login_check
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
            return redirect(reverse('exito'))
    else:
        form = RegistroClienteForm()
    return render(request, 'cuentas/registro.html', {'form': form})


@login_check
def registro_proveedor(request):
    if request.method == 'POST':
        form = RegistroProveedorForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['clave'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['nombre']
            )
            perfil = Proveedor(
                usuario=user,
                rif=form.cleaned_data['rif'],
                telefono=form.cleaned_data['telefono'],
                direccion=form.cleaned_data['direccion']
            )
            user.save()
            perfil.save()
            return redirect(reverse('exito'))
    else:
        form = RegistroProveedorForm()
    return render(request, 'cuentas/registro.html', {'form': form})


@method_decorator(login_check, name='dispatch')
class LoginView(generic.FormView):
    form_class = LoginForm
    success_url = reverse_lazy('home')
    template_name = 'cuentas/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


def home(request):
    try:
        request.user.cliente
        return redirect(reverse('home_cliente'))
    except:
        return redirect(reverse('home_proveedor'))