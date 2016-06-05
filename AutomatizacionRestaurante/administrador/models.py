from django.db import models

from . import fields

class Ingrediente(models.Model):
    nombre = models.CharField(max_length=30, primary_key=True)


class Plato(models.Model):
    nombre = models.CharField(max_length=30, primary_key=True)
    descripcion = models.TextField(max_length=30)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    ingredientes = models.ManyToManyField(Ingrediente)


class Menu(models.Model):
    nombre = models.CharField(max_length=30, primary_key=True)
    actual = fields.OneTrueBooleanField(default=False)
    platos = models.ManyToManyField(Plato)
