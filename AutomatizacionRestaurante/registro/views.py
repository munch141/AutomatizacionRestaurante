# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.template.context_processors import request
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView

from .forms import ClienteForm

app_name = 'registro'

def clienteRegistrado(request):
    return render(request, 'registro/clienteRegistrado.html') 

class registroCliente(FormView):
    template_name = 'registro/registroCliente.html'
    form_class = ClienteForm
    success_url = '/registro/registroCliente/clienteRegistrado/'

    def form_valid(self, form):
        form.save(commit=True)
        return super(registroCliente, self).form_valid(form)