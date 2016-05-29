from django.contrib.auth.models import User
from django.db import models

SEXOS = (
    ('M', 'Masculino'),
    ('F', 'Femenino')
)


class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    ci = models.PositiveIntegerField(primary_key=True)
    fecha_nacimiento = models.DateField('fecha de nacimiento')
    sexo = models.CharField(max_length=1, choices=SEXOS)
    telefono = models.CharField(max_length=12)

    def __str__(self):
        return str(self.usuario.username)


class Proveedor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rif = models.PositiveIntegerField(primary_key=True)
    telefono = models.CharField(max_length=12)
    direccion = models.CharField(max_length=128)

    def __str__(self):
        return str(self.usuario.username)
