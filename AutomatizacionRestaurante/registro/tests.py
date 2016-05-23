from django.test import Client, TestCase

class PruebasRegistroCliente(TestCase):
    def setUp(self):
        self.client = Client()

    def test_vista_registroCliente(self):
        response = self.client.get('/registro/registroCliente/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Regístrese:')
        
    def test_cliente_registrado(self):
        response = self.client.post('/registro/registroCliente/',
                                    {'nombre': 'minombre',
                                     'apellido': 'miapellido',
                                     'ci': 'mici',
                                     'fecha_nacimiento': 'mifecha',
                                     'email': 'miemail@email.com',
                                     'telefono': '111-11111',
                                     'sexo': 'M',
                                     'clave1': '1234',
                                     'clave2': '1234',})
        self.assertEqual(response.status_code, 302)