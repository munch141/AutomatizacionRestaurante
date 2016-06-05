# -*- coding: utf-8 -*-

import unittest
from django.test import TestCase
from django.contrib.auth.models import User

from .forms import RegistroClienteForm, RegistroProveedorForm
from .models import Cliente
from .models import Proveedor


class PruebasFormRegistroCliente(TestCase):
    """
    Pruebas de validación del form de registro de cliente
    """

    def test_validacion_datos_correctos(self):
        """
        Se prueba que el formulario sea válido si todos los campos cumplen con
        sus requisitos
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_validacion_username_vacio(self):
        """
        Se prueba que el formulario no sea válido cuando el username es vacío
        """
        form_data = {
            'username': '',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }
        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        

    def test_validacion_cedula_vacia(self):
        """
        Se prueba que el formulario no sea válido cuando la cédula es vacía
        """
        form_data = {
            'username': 'cliente1',
            'ci': '',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('ci', form.errors)

    def test_validacion_cedula_entero_negativo(self):
        """
        Se prueba que el formulario no sea válido cuando la cédula es un entero
        negativo
        """
        form_data = {
            'username': 'cliente1',
            'ci': '-10000000',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('ci', form.errors)

    def test_validacion_cedula_caracteres(self):
        """
        Se prueba que el formulario no sea válido cuando la cédula es un
        string
        """
        form_data = {
            'username': 'cliente1',
            'ci': 'asdfghjkl',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('ci', form.errors)

    def test_validacion_nombre_vacio(self):
        """
        Se prueba que el formulario no sea válido cuando el nombre es vacío
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': '',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    def test_validacion_nombre_con_numeros(self):
        """
        Se prueba que el formulario no sea válido cuando el nombre tiene números
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo1',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    def test_validacion_nombre_con_caracteres_especiales(self):
        """
        Se prueba que el formulario no sea válido cuando el nombre tiene algún
        carater que no sea una letra o un espacio en blanco
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo-',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    def test_validacion_nombre_empieza_con_espacio(self):
        """
        Se prueba que el formulario no sea válido cuando el nombre empieza con
        un espacio en blanco
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': ' Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    def test_validacion_nombre_solo_espacios(self):
        """
        Se prueba que el formulario no sea válido cuando el nombre está formado
        por espacios en blanco
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': '    ',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    def test_validacion_nombre_termina_en_espacios(self):
        """
        Se prueba que el formulario no sea válido cuando el nombre termina con
        un espacio en blanco
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo ',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    def test_validacion_apellido_vacio(self):
        """
        Se prueba que el formulario no sea válido cuando el apellido es vacío
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': '',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('apellido', form.errors)

    def test_validacion_apellido_con_numeros(self):
        """
        Se prueba que el formulario no sea válido cuando el apellido tiene números
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente1',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('apellido', form.errors)

    def test_validacion_apellido_con_caracteres_especiales(self):
        """
        Se prueba que el formulario no sea válido cuando el apellido tiene algún
        carater que no sea una letra o un espacio en blanco
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente-',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('apellido', form.errors)

    def test_validacion_apellido_empieza_con_espacio(self):
        """
        Se prueba que el formulario no sea válido cuando el apellido empieza con
        un espacio en blanco
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': ' Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('apellido', form.errors)

    def test_validacion_apellido_solo_espacios(self):
        """
        Se prueba que el formulario no sea válido cuando el apellido está formado
        por espacios en blanco
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': '    ',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('apellido', form.errors)

    def test_validacion_apellido_termina_en_espacios(self):
        """
        Se prueba que el formulario no sea válido cuando el apellido termina con
        un espacio en blanco
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente ',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('apellido', form.errors)

    def test_validacion_fecha_vacia(self):
        """
        Se prueba que el formulario no sea válido cuando la fecha de nacimiento
        es vacía
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('fecha_nacimiento', form.errors)

    def test_validacion_email_vacio(self):
        """
        Se prueba que el formulario no sea válido cuando el email es vacío
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': '',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_validacion_email_sin_usuario(self):
        """
        Se prueba que el formulario no sea válido cuando el email no tiene
        nombre de usuario
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': '@hola.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_validacion_email_sin_arroba(self):
        """
        Se prueba que el formulario no sea válido cuando el email no tiene
        @
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mailhola.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_validacion_email_sin_dominio(self):
        """
        Se prueba que el formulario no sea válido cuando el email no tiene
        dominio
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_validacion_email_dominio_invalido(self):
        """
        Se prueba que el formulario no sea válido cuando el email no tiene
        un dominio válido
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_validacion_telefono_vacio(self):
        """
        Se prueba que el formulario no sea válido cuando el teléfono es vacío
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('telefono', form.errors)

    def test_validacion_telefono_sin_guion(self):
        """
        Se prueba que el formulario no sea válido cuando el teléfono no tiene
        guión
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '11111111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('telefono', form.errors)

    def test_validacion_telefono_digitos_insuficientes_antes_guion(self):
        """
        Se prueba que el formulario no sea válido cuando el teléfono tiene
        tiene menos de 4 dígitos antes del guión
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('telefono', form.errors)

    def test_validacion_telefono_sin_digitos_antes_guion(self):
        """
        Se prueba que el formulario no sea válido cuando el teléfono no tiene
        dígitos antes del guión
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('telefono', form.errors)

    def test_validacion_telefono_digitos_insuficientes_despues_guion(self):
        """
        Se prueba que el formulario no sea válido cuando el teléfono no tiene
        suficientes después del guión
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-11111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('telefono', form.errors)

    def test_validacion_telefono_sin_digitos_despues_guion(self):
        """
        Se prueba que el formulario no sea válido cuando el teléfono no tiene
        dígitos después del guión
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('telefono', form.errors)

    def test_validacion_telefono_con_caracteres_invalidos(self):
        """
        Se prueba que el formulario no sea válido cuando el teléfono no tiene
        dígitos después del guión
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111-?',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('telefono', form.errors)

    def test_validacion_sexo_vacio(self):
        """
        Se prueba que el formulario no sea válido cuando el sexo es vacío
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'sexo': '',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('sexo', form.errors)

    def test_validacion_clave_vacia(self):
        """
        Se prueba que el formulario no sea válido cuando la clave es vacía
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('clave', form.errors)

    def test_validacion_clave2_vacia(self):
        """
        Se prueba que el formulario no sea válido cuando la clave2 es vacía
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('clave2', form.errors)

    def test_validacion_claves_distintas(self):
        """
        Se prueba que el formulario no sea válido cuando la clave y la clave2
        son distintas
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '87654321',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('clave', form.errors)

    def test_validacion_clave_muy_corta(self):
        """
        Se prueba que el formulario no sea válido cuando la clave es de menos de
        6 caracteres
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345',
            'clave2': '12345',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('clave', form.errors)


class PruebasFormRegistroCliente_BaseDeDatos(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='cliente1',
            password=1234567,
            email='mail@ejemplo.com',
            first_name='Ejemplo',
            last_name='Cliente'
        )
        cliente = Cliente(
            usuario=user,
            ci=10000000,
            fecha_nacimiento='1996-10-25',
            sexo='M',
            telefono='1111-1111111'
        )
        user.save()
        cliente.save()


    def test_validacion_username_existente(self):
        """
        Se prueba que el formulario no es válido si el username está usado
        """
        form_data = {
            'username': 'cliente1',
            'ci': '10000001',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_validacion_ci_existente(self):
        """
        Se prueba que el formulario no es válido si hay algún usuario con el
        mismo número de cédula
        """
        form_data = {
            'username': 'cliente2',
            'ci': '10000000',
            'nombre': 'Ejemplo',
            'apellido': 'Cliente',
            'fecha_nacimiento': '10/25/1996',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'sexo': 'M',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroClienteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('ci', form.errors)


class PruebasFormRegistroProveedor(TestCase):
    """
    Pruebas de validación del form de registro de proveedor
    """

    def test_validacion_datos_correctos(self):
        """
        Se prueba que el formulario sea válido si todos los campos cumplen con
        sus requisitos
        """
        form_data = {
            'username': 'cliente1',
            'rif': '123456',
            'nombre': 'Empresa',
            'direccion': 'Dirección para prueba',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroProveedorForm(data=form_data)
        self.assertTrue(form.is_valid())


    def test_validacion_username_vacio(self):
        """
        Se prueba que el formulario no sea válido cuando el username es vacío
        """
        form_data = {
            'username': '',
            'rif': '123456',
            'nombre': 'Empresa Ejemplo',
            'direccion': 'Dirección para prueba',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroProveedorForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


    def test_validacion_rif_vacio(self):
        """
        Se prueba que el formulario no sea válido cuando el rif es vacío
        """
        form_data = {
            'username': 'valen',
            'rif': '',
            'nombre': 'Empresa',
            'direccion': 'Dirección para prueba',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroProveedorForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rif', form.errors)


    def test_validacion_direccion_vacio(self):
        """
        Se prueba que el formulario no sea válido cuando el username es vacío
        """
        form_data = {
            'username': 'proveedor',
            'rif': '123456',
            'nombre': 'Empresa',
            'direccion': '',
            'email': 'mail@ejemplo.com',
            'telefono': '1111-1111111',
            'clave': '12345678',
            'clave2': '12345678',
        }

        form = RegistroProveedorForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('direccion', form.errors)
