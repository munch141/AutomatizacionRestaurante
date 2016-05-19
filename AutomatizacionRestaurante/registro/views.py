from django.shortcuts import render
from django.template.context_processors import request

app_name = 'registro'

def registroCliente(request):
    return render(request, 'registro/registroCliente.html')