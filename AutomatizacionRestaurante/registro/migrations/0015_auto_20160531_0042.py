# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 00:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0014_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='rif',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
