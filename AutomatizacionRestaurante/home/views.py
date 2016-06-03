# -*- coding: utf-8 -*-

from django.views import generic
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from .forms import LoginForm


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
    return HttpResponseRedirect('/')

@login_required(login_url='/')
def home(request):
	return render_to_response('home/home.html', {'user':request.user})

@login_required(login_url='/')
def perfil(request):
	return render_to_response('home/perfil.html', {'user':request.user})