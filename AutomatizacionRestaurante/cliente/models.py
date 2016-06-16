# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator

from administrador.models import Ingrediente

from cliente.utils import Historial

SEXOS = (
    ('M', 'Masculino'),
    ('F', 'Femenino')
)


class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    ci = models.PositiveIntegerField(primary_key=True)
    fecha_nacimiento = models.DateField('fecha de nacimiento')
    sexo = models.CharField(max_length=1, choices=SEXOS)
    telefono = models.CharField(
        validators=[RegexValidator(
            regex='^[0-9]{4}-[0-9]{7}$',
            message='El teléfono debe tener este formato: 0212-1234567',
            code='telefono_invalido')],
        max_length=12)

    def __str__(self):
        return str(self.usuario.username)


class Billetera(models.Model):
    usuario = models.OneToOneField(
        User, on_delete = models.CASCADE, primary_key=True,)
    pin = models.CharField(max_length=100)
    debitos = Historial()
    creditos = Historial()

    def __str__(self):
        return str(self.usuario.username)

    def saldo(self):
        if (self.creditos.total - self.debitos.total < 0) \
           or (self.debitos.total < 0):
            return -1 # saldo negativo
        return self.creditos.total - self.debitos.total
    
    def recargar(self, monto, id_rest):
        if not isinstance(monto, float) and not isinstance(monto, int):
            return -1 # tipo incorrecto
        else:
            self.creditos.agregarTransaccion(Transaccion(monto))
        
    def consumir(self, monto, pin):
        if not isinstance(monto, float) and not isinstance(monto, int):
            return -3 # tipo incorrecto
        else:
            if pin == self.pin and monto <= self.saldo():
                self.debitos.agregarTransaccion(Transaccion(monto))
            elif pin != self.pin:
                return -2 # pin incorrecto
            elif self.saldo() < monto:
                return -1 # saldo insuficiente
