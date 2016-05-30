# -*- coding: utf-8 -*-

import unittest
from django.test import Client, TestCase

class PruebasRegistro(TestCase):
    def setUp(self):
        self.client = Client()

    def test_vista_registroProveedor(self):
        response = self.client.get('/registro/registroProveedor/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Regístrese (Proveedor):')

    def test_vista_registroCliente(self):
        response = self.client.get('/registro/registroCliente/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Regístrese (Cliente):')
        
    def test_registro_proveedor_redireccion(self):
        response = self.client.post('/registro/registroProveedor/',
                                    {'username': 'user1',
                                     'rif': '123456',
                                     'nombre': 'minombre',
                                     'email': 'miemail@email.com',
						             'direccion': 'Caurimare',
                                     'telefono': '1111-1111111',
                                     'clave': '1234',
                                     'clave2': '1234'})
        self.assertEqual(response.status_code, 302)

    def test_registro_cliente_redireccion(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'username': 'user1',
                                     'ci': '123456',
                                     'nombre': 'minombre',
                                     'email': 'miemail@email.com',
                                     'fecha_nacimiento': '11/15/1993',
                                     'sexo': 'M',
                                     'telefono': '1111-1111111',
                                     'clave': '1234',
                                     'clave2': '1234'})
        self.assertEqual(response.status_code, 302)

################################################################################
#-----------------------------CASOS FRONTERA-----------------------------------#
################################################################################

    def test_registro_proveedor_sin_username(self):
        response = self.client.post('/registro/registroProveedor/',
                                    {'username': '',
                                     'rif': '123456',
                                     'nombre': 'minombre',
                                     'email': 'miemail@email.com',
									 'direccion': 'Caurimare',
                                     'telefono': '1111-1111111',
                                     'clave': '1234',
                                     'clave2': '1234'})
        self.assertEqual(response.status_code, 200)

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
    
    def test_registro_proveedor_sin_rif(self):
        response = self.client.post('/registro/registroProveedor/',
                                    {'username': 'user1',
                                     'rif': '',
                                     'nombre': 'minombre',
                                     'email': 'miemail@email.com',
									 'direccion': 'Caurimare',
                                     'telefono': '1111-1111111',
                                     'clave': '1234',
                                     'clave2': '1234'})
        self.assertEqual(response.status_code, 200)                                     

    def test_registro_cliente_sin_cedula(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'username': 'user1',
                                     'ci': '',
                                     'nombre': 'minombre',
                                     'apellido': 'miapellido',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemail@email.com',
                                     'telefono':'1111-1111111',
                                     'clave': '1234',
                                     'clave2': '1234'})
        self.assertEqual(response.status_code, 200)                                     

    def test_registro_proveedor_sin_nombre(self):
        response = self.client.post('/registro/registroProveedor/',
                                    {'username': 'user1',
                                     'rif': '123456',
                                     'nombre': '',
                                     'email': 'miemail@email.com',
									 'direccion': 'Caurimare',
                                     'telefono': '1111-1111111',
                                     'clave': '1234',
                                     'clave2': '1234'})
        self.assertEqual(response.status_code, 200)

    def test_registro_cliente_sin_nombre(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'username': 'user1',
                                     'ci': '123',
                                     'nombre': '',
                                     'apellido': 'miapellido',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemail@email.com',
                                     'telefono':'1111-1111111',
                                     'clave': '1234',
                                     'clave2': '1234'})
        self.assertEqual(response.status_code, 200)
    
    def test_registro_proveedor_sin_correo(self):
        response = self.client.post('/registro/registroProveedor/',
                                    {'username': 'user1',
                                     'rif': '123456',
                                     'nombre': 'minombre',
                                     'email': '',
									 'direccion': 'Caurimare',
                                     'telefono': '1111-1111111',
                                     'clave': '1234',
                                     'clave2': '1234'})
        self.assertEqual(response.status_code, 200)

    def test_registro_cliente_sin_apellido(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'username': 'user1',
                                     'ci': '123',
                                     'nombre': 'minombre',
                                     'apellido': '',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemail@email.com',
                                     'telefono':'1111-1111111',
                                     'clave': '1234',
                                     'clave2': '1234'})
        self.assertEqual(response.status_code, 200)
    
    def test_registro_cliente_sin_correo(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'username': 'user1',
                                     'ci': '123',
                                     'nombre': 'minombre',
                                     'apellido': 'apellido',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': '',
                                     'telefono':'1111-1111111',
                                     'clave': '1234',
                                     'clave2': '1234'})
        self.assertEqual(response.status_code, 200)

    def test_registro_proveedor_sin_telefono(self):
        response = self.client.post('/registro/registroProveedor/',
                                    {'username': 'user1',
                                     'rif': '123456',
                                     'nombre': 'minombre',
                                     'email': 'miemail@email.com',
									 'direccion': 'Caurimare',
                                     'telefono': '',
                                     'clave': '1234',
                                     'clave2': '1234'})
        self.assertEqual(response.status_code, 200)

    def test_registro_proveedor_sin_clave_principal(self):
        response = self.client.post('/registro/registroProveedor/',
                                    {'username': 'user1',
                                     'rif': '123456',
                                     'nombre': 'minombre',
                                     'email': 'miemail@email.com',
						 'direccion': 'Caurimare',
                                     'telefono': '1111-1111111',
                                     'clave': '',
                                     'clave2': '1234'})
        self.assertEqual(response.status_code, 200)                                

    def test_registro_cliente_sin_telefono(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'username': 'user1',
                                     'ci': '123',
                                     'nombre': 'minombre',
                                     'apellido': 'apellido',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemail@email.com',
                                     'telefono':'',
                                     'clave': '1234',
                                     'clave2': '1234'})
        self.assertEqual(response.status_code, 200)
  
    def test_registro_cliente_sin_clave_principal(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'username': '',
                                     'ci': '123456',
                                     'nombre': 'minombre',
                                     'apellido': 'miapellido',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemail@email.com',
                                     'telefono': '1111-1111111',
                                     'clave': '',
                                     'clave2': '1234'})
        self.assertEqual(response.status_code, 200)

    def test_registro_proveedor_sin_confirmacion_clave(self):
        response = self.client.post('/registro/registroProveedor/',
                                    {'username': 'user1',
                                     'rif': '123456',
                                     'nombre': 'minombre',
                                     'email': 'miemail@email.com',
						             'direccion': 'Caurimare',
                                     'telefono': '1111-1111111',
                                     'clave': '1234',
                                     'clave2': ''})
        self.assertEqual(response.status_code, 200)                                     

    def test_registro_cliente_sin_confirmacion_clave(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'username': '',
                                     'ci': '123456',
                                     'nombre': 'minombre',
                                     'apellido': 'miapellido',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemail@email.com',
                                     'telefono': '1111-1111111',
                                     'clave': '1234',
                                     'clave2': ''})
        self.assertEqual(response.status_code, 200)

    def test_registro_proveedor_sin_claves(self):
        response = self.client.post('/registro/registroProveedor/',
                                    {'username': 'user1',
                                     'rif': '123456',
                                     'nombre': 'minombre',
                                     'email': 'miemail@email.com',
						 'direccion': 'Caurimare',
                                     'telefono': '1111-1111111',
                                     'clave': '',
                                     'clave2': ''})
        self.assertEqual(response.status_code, 200)                                     
    
    def test_registro_cliente_sin_claves(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'username': '',
                                     'ci': '123456',
                                     'nombre': 'minombre',
                                     'apellido': 'miapellido',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemail@email.com',
                                     'telefono': '1111-1111111',
                                     'clave': '',
                                     'clave2': ''})
        self.assertEqual(response.status_code, 200)

    def test_registro_proveedor_rif_erroneo(self):
        response = self.client.post('/registro/registroProveedor/',
                                    {'username': 'user1',
                                     'rif': 'jjhh',
                                     'nombre': 'minombre',
                                     'email': 'miemail@email.com',
						 'direccion': 'Caurimare',
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
        
    def test_proveedor_cliente_formato_erroneo_correo(self):
        response = self.client.post('/registro/registroProveedor/',
                                    {'username': 'user1',
                                     'rif': '123456',
                                     'nombre': 'minombre',
                                     'email': 'miemailemailcom',
						             'direccion': 'Caurimare',
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

    def test_proveedor_repeticion_clave_invalida(self):
        response = self.client.post('/registro/registroProveedor/',
                                    {'username': 'user1',
                                     'rif': '123456',
                                     'nombre': 'minombre',
                                     'email': 'miemail@email.com',
									 'direccion': 'Caurimare',
                                     'telefono': '1111-1111111',
                                     'clave': '1234',
                                     'clave2': '1254'})
        self.assertEqual(response.status_code, 200)

    def test_proveedor_sin_direccion(self):
        response = self.client.post('/registro/registroProveedor/',
                                    {'username': 'user1',
                                     'rif': '123456',
                                     'nombre': 'minombre',
                                     'email': 'miemail@email.com',
									 'direccion': '',
                                     'telefono': '1111-1111111',
                                     'clave': '1234',
                                     'clave2': '1254'})
        self.assertEqual(response.status_code, 200)

    def test_registro_repeticion_clave_invalida(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'username': 'user1',
                                     'ci': '123456',
                                     'nombre': 'minombre',
                                     'apellido': 'miapellido',
                                     'fecha_nacimiento': '11/15/1993',
                                     'email': 'miemail@email.com',
                                     'telefono':'1111-1111111',
                                     'clave': '1234',
                                     'clave2': '5681'})
        self.assertEqual(response.status_code, 200)