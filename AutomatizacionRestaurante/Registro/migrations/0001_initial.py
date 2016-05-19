# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-19 20:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('ci', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=60)),
                ('apellido', models.CharField(max_length=60)),
                ('fecha_nacimiento', models.DateTimeField(verbose_name='fecha de nacimiento')),
                ('telefono', models.IntegerField()),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femanino')], max_length=1)),
                ('clave', models.CharField(max_length=10)),
            ],
        ),
    ]
