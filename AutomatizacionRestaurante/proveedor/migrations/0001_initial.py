# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-16 18:42
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administrador', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredientes', models.ManyToManyField(to='administrador.Ingrediente')),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('rif', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('telefono', models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(code='telefono_invalido', message='El teléfono debe tener este formato: 0212-1234567', regex='^[0-9]{4}-[0-9]{7}$')])),
                ('direccion', models.CharField(max_length=128)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='inventario',
            name='rif_proveedor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='proveedor.Proveedor'),
        ),
    ]
