# -*- coding: utf-8 -*-

import sys
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator

from administrador.models import Ingrediente


SEXOS = (
    ('M', 'Masculino'),
    ('F', 'Femenino')
)


class Historial(models.Model):
    total = models.FloatField()
        
    def agregarTransaccion(self, t):
        self.trans.add(t)
        self.total += t.monto
        self.save()

    def __str__(self):
        try:
            self.debitos
            return str(self.debitos)+'_debitos'
        except:
            return str(self.creditos)+'_creditos'


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
    debitos = models.OneToOneField(
        Historial, on_delete=models.CASCADE, related_name='debitos')
    creditos = models.OneToOneField(
        Historial, on_delete=models.CASCADE, related_name='creditos')

    def __str__(self):
        return str(self.usuario.username)

    def save(self, *args, **kwargs):
        self.debitos = Historial.objects.create(total=0)
        self.creditos = Historial.objects.create(total=0)
        super(Billetera, self).save(*args, **kwargs)

    def saldo(self):
        return self.creditos.total - self.debitos.total
    
    def recargar(self, monto):
        print(monto)
        self.creditos.agregarTransaccion(
                Transaccion.objects.create(
                    monto=monto, fecha=datetime.now(), historial=self.creditos))
        
    def consumir(self, monto):
        if self.saldo() < monto:
            return False
        else:
            self.debitos.agregarTransaccion(
                Transaccion.objects.create(
                    monto=monto, fecha=datetime.now(), historial=self.debitos))
            return True


class Transaccion(models.Model):
    monto = models.FloatField()
    fecha = models.DateTimeField()
    historial = models.ForeignKey(
        'Historial', on_delete=models.CASCADE, related_name='trans')
