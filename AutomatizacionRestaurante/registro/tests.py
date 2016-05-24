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

################################################################################
#-----------------------------CASOS FRONTERA-----------------------------------#
################################################################################

    def test_registro_cliente_sin_ci(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'ci': '',
                                     'nombre': 'minombre',
                                     'apellido': 'miapellido',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemail@email.com',
                                     'telefono': '1111-1111111',
                                     'sexo': 'M',
                                     'clave': '1234',
                                     'clave2': '1234',})
        self.assertEqual(response.status_code, 200)

    def test_registro_cliente_sin_nombre(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'ci': '123456',
                                     'nombre': '',
                                     'apellido': 'miapellido',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemail@email.com',
                                     'telefono': '1111-1111111',
                                     'sexo': 'M',
                                     'clave': '1234',
                                     'clave2': '1234',})
        self.assertEqual(response.status_code, 200)

    def test_registro_cliente_sin_apellido(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'ci': '123456',
                                     'nombre': 'minombre',
                                     'apellido': '',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemail@email.com',
                                     'telefono': '1111-1111111',
                                     'sexo': 'M',
                                     'clave': '1234',
                                     'clave2': '1234',})
        self.assertEqual(response.status_code, 200)

    def test_registro_cliente_sin_email(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'ci': '123456',
                                     'nombre': 'minombre',
                                     'apellido': 'miapellido',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': '',
                                     'telefono': '1111-1111111',
                                     'sexo': 'M',
                                     'clave': '1234',
                                     'clave2': '1234',})
        self.assertEqual(response.status_code, 200)

    def test_registro_cliente_sin_telefono(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'ci': '123456',
                                     'nombre': 'minombre',
                                     'apellido': 'miapellido',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemail@email.com',
                                     'telefono': '',
                                     'sexo': 'M',
                                     'clave': '1234',
                                     'clave2': '1234',})
        self.assertEqual(response.status_code, 200)

    def test_registro_cliente_sin_sexo(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'ci': '123456',
                                     'nombre': 'minombre',
                                     'apellido': 'miapellido',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemail@email.com',
                                     'telefono': '1111-1111111',
                                     'sexo': '',
                                     'clave': '1234',
                                     'clave2': '1234',})
        self.assertEqual(response.status_code, 200)

    def test_registro_cliente_sin_clave1(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'ci': '123456',
                                     'nombre': 'minombre',
                                     'apellido': 'miapellido',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemail@email.com',
                                     'telefono': '1111-1111111',
                                     'sexo': 'M',
                                     'clave': '',
                                     'clave2': '1234',})
        self.assertEqual(response.status_code, 200)

    def test_registro_cliente_sin_clave2(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'ci': '123456',
                                     'nombre': 'minombre',
                                     'apellido': 'miapellido',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemail@email.com',
                                     'telefono': '1111-1111111',
                                     'sexo': 'M',
                                     'clave': '1234',
                                     'clave2': '',})
        self.assertEqual(response.status_code, 200)

    def test_registro_cliente_ci_caracteres(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'ci': 'hola',
                                     'nombre': 'minombre',
                                     'apellido': 'miapellido',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemail@email.com',
                                     'telefono': '1111-1111111',
                                     'sexo': 'M',
                                     'clave': '1234',
                                     'clave2': '1234',})
        self.assertEqual(response.status_code, 200)

    def test_registro_cliente_ci_num_float(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'ci': '2.3',
                                     'nombre': 'minombre',
                                     'apellido': 'miapellido',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemail@email.com',
                                     'telefono': '1111-1111111',
                                     'sexo': 'M',
                                     'clave': '1234',
                                     'clave2': '1234',})
        self.assertEqual(response.status_code, 200)

    def test_registro_cliente_ci_entero_negativo(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'ci': '-12345',
                                     'nombre': 'minombre',
                                     'apellido': 'miapellido',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemail@email.com',
                                     'telefono': '1111-1111111',
                                     'sexo': 'M',
                                     'clave': '1234',
                                     'clave2': '1234',})
        self.assertEqual(response.status_code, 200)