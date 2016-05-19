from django.shortcuts import render
from django.template.context_processors import request
from django.http.response import HttpResponse

def registroCliente(request):
    return HttpResponse("Registro")