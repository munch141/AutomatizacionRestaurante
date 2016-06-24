from django.core.urlresolvers import resolve, reverse
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import TestCase
from django.template.loader import render_to_string
from importlib import import_module

from .views import realizar_pedido
from .models import Cliente


class PruebasCliente(TestCase):
    def setUp(self):
        user = User.objects.create(
            username='cliente', first_name='Cliente', last_name='Uno')
        user.set_password('pw')
        user.save()
        
        cliente = Cliente.objects.create(
            usuario=user, ci='1', fecha_nacimiento='1991-1-1', sexo='M',
            telefono='123456')
        cliente.save()

    def test_realizar_pedido_url_llama_a_vista_realizar_pedido(self):
        found = resolve(reverse('realizar_pedido'))
        self.assertEqual(found.func, realizar_pedido)

    def test_pagina_realizar_pedido_devuelve_html_correcto(self):
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)
        user = authenticate(username='cliente', password='pw')
        request.user = user
        login(request, user)
        
        response = realizar_pedido(request)
        expected_html = render_to_string(
            'cliente/realizar_pedido.html', request=request)
        self.assertEqual(response.content.decode(), expected_html)
