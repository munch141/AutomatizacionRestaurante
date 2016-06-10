# -*- coding: utf-8 -*-

from django.forms import EmailField, ModelForm, CharField
from django.contrib.auth.models import User

from .models import BilleteraElectronica


class EditarPerfilForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']

    email = EmailField(label='Correo electrónico')

class CrearBilleteraForm(ModelForm):
	class Meta:
		model = BilleteraElectronica
		fields = ['pin']

	pin = CharField(label='Pin')
