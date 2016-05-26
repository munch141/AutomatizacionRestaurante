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
                                    {'username': 'user1',
                                     'ci': '123456',
                                     'nombre': 'minombre',
                                     'apellido': 'miapellido',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemail@email.com',
                                     'telefono': '1111-1111111',
                                     'clave': '1234',
                                     'clave2': '1234'})
        self.assertEqual(response.status_code, 302)

################################################################################
#-----------------------------CASOS FRONTERA-----------------------------------#
################################################################################

    def test_registro_cliente_sin_username(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'username': '',
                                     'ci': '123456',
                                     'nombre': 'minombre',
                                     'apellido': 'miapellido',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemail@email.com',
                                     'telefono': '1111-1111111',
                                     'clave': '1234',
                                     'clave2': '1234'})
        self.assertEqual(response.status_code, 200)
    
    def test_registro_cliente_cedula_erronea(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'username': 'user1',
                                     'ci': 'fgdgd',
                                     'nombre': 'minombre',
                                     'apellido': 'miapellido',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemail@email.com',
                                     'telefono': '1111-1111111',
                                     'clave': '1234',
                                     'clave2': '1234'})
        self.assertEqual(response.status_code, 200)
        
    def test_registro_cliente_formato_erroneo_correo(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'username': '',
                                     'ci': '123456',
                                     'nombre': 'minombre',
                                     'apellido': 'miapellido',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemailemailcom',
                                     'telefono': '1111-1111111',
                                     'clave': '1234',
                                     'clave2': '1234'})
        self.assertEqual(response.status_code, 200)
        
    def test_registro_cliente_formato_erroneo_tlf(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'username': '',
                                     'ci': '123456',
                                     'nombre': 'minombre',
                                     'apellido': 'miapellido',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemail@email.com',
                                     'telefono': '11',
                                     'clave': '1234',
                                     'clave2': '1234'})
        self.assertEqual(response.status_code, 200)
    
    def test_registro_cliente_error_tlf(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'username': '',
                                     'ci': '123456',
                                     'nombre': 'minombre',
                                     'apellido': 'miapellido',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemail@email.com',
                                     'telefono': 'ffff',
                                     'clave': '1234',
                                     'clave2': '1234'})
        self.assertEqual(response.status_code, 200)
        
    def test_registro_repeticion_clave_invalida(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'username': '',
                                     'ci': '123456',
                                     'nombre': 'minombre',
                                     'apellido': 'miapellido',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemail@email.com',
                                     'telefono': 'ffff',
                                     'clave': '1234',
                                     'clave2': '5681'})
        self.assertEqual(response.status_code, 200)