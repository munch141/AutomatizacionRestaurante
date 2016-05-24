# -*- coding: utf-8 -*-

from django.test import Client, TestCase

class PruebasRegistroCliente(TestCase):
    def setUp(self):
        self.client = Client()

    def test_vista_registroCliente(self):
        response = self.client.get('/registro/registroCliente/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Regístrese:')
        
    def test_registro_cliente_redireccion(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'nombre': 'minombre',
                                     'apellido': 'miapellido',
                                     'ci': '123456',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemail@email.com',
                                     'telefono': '1111-1111111',
                                     'sexo': 'M',
                                     'clave': '1234',
                                     'clave2': '1234',})
        self.assertEqual(response.status_code, 302)