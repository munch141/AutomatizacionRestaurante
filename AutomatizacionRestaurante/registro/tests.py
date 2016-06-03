# -*- coding: utf-8 -*-

import unittest
from django.test import Client, TestCase
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

    def test_validacion_username_vacia(self):
        """
        Se prueba que el formulario sea inválido si la cédula es vacía
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

    def test_validacion_cedula_vacia(self):
        """
        Se prueba que el formulario sea inválido si la cédula es vacía
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
