# -*- coding: utf-8 -*-

from django.test import Client, TestCase

class PruebasRegistroProveedor(TestCase):
    def setUp(self):
        self.client = Client()

    def test_vista_registroProveedor(self):
        response = self.client.get('/registro/registroProveedor/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Regístrese (Proveedor):')
        
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
        

    

