# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator

from administrador.models import Ingrediente


class Proveedor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rif = models.CharField(max_length=10, primary_key=True)
    telefono = models.CharField(
        validators=[RegexValidator(
            regex='^[0-9]{4}-[0-9]{7}$',
            message='El teléfono debe tener este formato: 0212-1234567',
            code='telefono_invalido')],
        max_length=12)
    direccion = models.CharField(max_length=128)

    def __str__(self):
        return str(self.usuario.username)


class Inventario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'inventario_'+str(self.usuario.username)


class Ingrediente_inventario(models.Model):
    inventario = models.ForeignKey(Inventario, related_name='ingredientes')
    ingrediente = models.ForeignKey(Ingrediente)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.ingrediente)+'_'+str(self.inventario)
