# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-26 20:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0008_auto_20160526_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
