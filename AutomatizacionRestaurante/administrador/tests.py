from django.contrib.auth.models import User
from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.test import TestCase
from django.template.loader import render_to_string

from .views import home
from .models import Administrador

class PruebasHomeAdmin(TestCase):

    def setUp(self):
       user = User.objects.create(username='admin', password='administrador')
       admin = Administrador.objects.create(usuario=user)

    def test_pagina_principal_devuelve_html_correcto(self):
        request = HttpRequest()
        response = home(request)
        expected_html = render_to_string('administrador/home.html', request=request)
        self.assertEqual(response.content.decode(), expected_html)

    def test_url_llama_a_vista_home_administrador(self):
        found = resolve(reverse('home_administrador'))
        self.assertEqual(found.func, home)

    
