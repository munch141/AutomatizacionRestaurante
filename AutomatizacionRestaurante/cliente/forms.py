# -*- coding: utf-8 -*-

from django.forms import EmailField, ModelForm
from django.contrib.auth.models import User


class EditarPerfilForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']

    email = EmailField(label='Correo electrónico')
