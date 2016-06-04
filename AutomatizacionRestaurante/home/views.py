# -*- coding: utf-8 -*-

from django.views import generic
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User

from registro.models import Cliente
from registro.models import Proveedor
from .forms import EditarPerfilForm, LoginForm


class LoginView(generic.FormView):
    form_class = LoginForm
    success_url = reverse_lazy('home')
    template_name = 'home/login.html'

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


@login_required(login_url='/')
def home(request):
    return render(request, 'home/home.html', {'user': request.user})


@login_required(login_url='/')
def perfil(request):
    return render(request, 'home/perfil.html', {'user': request.user})


@login_required(login_url='/')
def editar_perfil(request):
    try:
        request.user.cliente
        inline_formset = inlineformset_factory(
                User, Cliente, fields=('telefono',), can_delete=False)
    except:
        try:
            request.user.proveedor
            inline_formset = inlineformset_factory(
                User, Proveedor, fields=('telefono', 'direccion',), can_delete=False)
        except:
            messages.error(request, 'El usuario no es ni cliente ni proveedor.')
            return redirect(reverse('logout'))

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
                return redirect(reverse('perfil'))
    else:
        form = EditarPerfilForm(instance=request.user)
        formset = inline_formset(instance=request.user)
    return render(
        request,
        'home/editar_perfil.html',
        {'user': request.user, 'formset': formset, 'form': form})
