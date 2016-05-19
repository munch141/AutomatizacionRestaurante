from django.shortcuts import render
from django.http import HttpResponse
from django.template.context_processors import request

app_name = 'registro'

def registroCliente(request):
    return HttpResponse("Registro")