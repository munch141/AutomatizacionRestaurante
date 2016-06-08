from django.contrib.auth.models import User
from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.test import TestCase
from django.template.loader import render_to_string

from .views import home, ver_clientes
from .models import Administrador
from cuentas.models import Cliente

class PruebasHomeAdmin(TestCase):

    def setUp(self):
       user = User.objects.create(username='admin', password='administrador')
       admin = Administrador.objects.create(usuario=user)

    def test_pagina_principal_devuelve_html_correcto(self):
        request = HttpRequest()
        response = home(request)
        expected_html = render_to_string('administrador/home.html', request=request)
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_url_llama_a_vista_home_administrador(self):
        found = resolve(reverse('home_administrador'))
        self.assertEqual(found.func, home)

    def test_ver_clientes_url_llama_a_vista_ver_clientes(self):
        found = resolve(reverse('ver_clientes'))
        self.assertEqual(found.func, ver_clientes)

    def test_pagina_ver_clientes_devuelve_html_correcto(self):
        request = HttpRequest()
        response = ver_clientes(request)
        expected_html = render_to_string(
            'administrador/ver_clientes.html', request=request)
        self.assertEqual(response.content.decode(), expected_html)

    def test_pagina_ver_clientes_muestra_info_clientes_registrados(self):
        user1 = User.objects.create_user(
                username='cliente1',
                password='pw',
                email='cliente1@mail.com',
                first_name='Uno',
                last_name='Cliente'
            )
        Cliente.objects.create(
            usuario=user1,
            ci='1',
            fecha_nacimiento='1991-1-1',
            sexo='M',
            telefono='1111-1111111',
        )

        user2 = User.objects.create_user(
                username='cliente2',
                password='pw',
                email='cliente2@mail.com',
                first_name='Dos',
                last_name='Cliente'
            )
        Cliente.objects.create(
            usuario=user2,
            ci='2',
            fecha_nacimiento='1992-2-2',
            sexo='F',
            telefono='2222-2222222',
        )

        request = HttpRequest()
        response = ver_clientes(request)

        self.assertIn(user1.username, response.content.decode())
        self.assertIn(
            user1.date_joined.strftime('%d/%m/%Y'),
            response.content.decode())
        
        self.assertIn(user2.username, response.content.decode())
        self.assertIn(
            user2.date_joined.strftime('%d/%m/%Y'),
            response.content.decode())
