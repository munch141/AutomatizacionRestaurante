from django.contrib.auth.models import User
from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.test import TestCase
from django.template.loader import render_to_string

from .views import detalles_cliente, home, ver_clientes
from .models import Administrador
from cuentas.models import Cliente

class PruebasHomeAdmin(TestCase):
    def agregar_cliente(
        self, username, nombre, apellido, ci, email, telefono, sexo,
        fecha_nacimiento
    ):
        user = User.objects.create(
            username=username, password='pw', email=email,
            first_name=nombre, last_name=apellido
        )
        cliente = Cliente.objects.create(
            usuario=user, ci=ci, fecha_nacimiento=fecha_nacimiento,
            sexo=sexo, telefono=telefono,
        )
        user.save()
        cliente.save()
        return user

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
        cliente1 = self.agregar_cliente(
            'cliente1', 'Uno', 'Cliente', '1', 'cliente1@mail.com',
            '1111-1111111', 'M', '1991-1-1')

        cliente2 = self.agregar_cliente(
            'cliente2', 'Dos', 'Cliente', '2', 'cliente2@mail.com',
            '2222-2222222', 'M', '1992-2-2')

        request = HttpRequest()
        response = ver_clientes(request)

        self.assertIn(cliente1.username, response.content.decode())
        self.assertIn(
            cliente1.date_joined.strftime('%d/%m/%Y'),
            response.content.decode())
        
        self.assertIn(cliente2.username, response.content.decode())
        self.assertIn(
            cliente2.date_joined.strftime('%d/%m/%Y'),
            response.content.decode())

    def test_cliente_x_url_llama_a_vista_detalle_cliente(self):
        found = resolve(reverse('detalles_cliente', args=("cliente",)))
        self.assertEqual(found.func, detalles_cliente)

    def test_pagina_detalle_cliente_devuelve_html_correcto(self):
        request = HttpRequest()
        response = detalles_cliente(request, None)
        expected_html = render_to_string(
            'administrador/detalles_cliente.html', request=request)
        self.assertEqual(response.content.decode(), expected_html)
