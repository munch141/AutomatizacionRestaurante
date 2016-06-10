from django.db import models
from django.contrib.auth.models import User

from . import fields


class Administrador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.usuario.username)


class Ingrediente(models.Model):
    nombre = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return str(self.nombre)


class Plato(models.Model):
    nombre = models.CharField(max_length=30, primary_key=True)
    descripcion = models.TextField(max_length=30)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    ingredientes = models.ManyToManyField(Ingrediente)

    def __str__(self):
        return str(self.nombre)


class Menu(models.Model):
    nombre = models.CharField(max_length=30, primary_key=True)
    actual = fields.OneTrueBooleanField(default=False)
    platos = models.ManyToManyField(Plato)

    def __str__(self):
        return str(self.nombre)
