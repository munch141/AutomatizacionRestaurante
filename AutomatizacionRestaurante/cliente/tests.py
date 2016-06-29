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

        ingrediente = Ingrediente(
            nombre='Ingrediente 1', descripcion='Descripción del ingrediente')
        ingrediente.save()

        ingrediente2 = Ingrediente(
            nombre='Ingrediente 2', descripcion='Descripción del ingrediente 2')
        ingrediente2.save()

        plato1 = Plato(
            nombre='Plato 1',
            descripcion='Descripción del plato1',
            precio=1)
        plato1.save()
        plato1.contiene.add('Ingrediente 1', 'Ingrediente 2')

        plato2 = Plato(
            nombre='Plato 2',
            descripcion='Descripción del plato2',
            precio=2)
        plato2.save()
        plato2.contiene.add('Ingrediente 2')

        menu1 = Menu.objects.create(nombre='Menú 1', actual=True)
        menu1.incluye.add('Plato 1')
        menu1.incluye.add('Plato 2')

        menu2 = Menu.objects.create(nombre='Menú 2', actual=False)
        menu1.incluye.add('Plato 2')

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

    def test_realizar_pedido_puede_guardar_una_solicitud_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['platos'] = ['Plato 1']
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)
        user = authenticate(username='cliente', password='pw')
        request.user = user
        login(request, user)

        response = realizar_pedido(request)

        # FALTAN LOS CHEQUEOS
