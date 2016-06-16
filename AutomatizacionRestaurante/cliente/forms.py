# -*- coding: utf-8 -*-

from django.forms import EmailField, ModelForm, CharField, Form
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput

from .models import Billetera


class EditarPerfilForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']

    email = EmailField(label='Correo electrónico')


class CrearBilleteraForm(ModelForm):
    class Meta:
        model = Billetera
        fields = ['pin']

    pin = CharField(
        label='Pin',
        widget=PasswordInput(),
        error_messages={'required': 'Este campo es requerido.'})

    pin2 = CharField(
        label='Confirme Pin',
        widget=PasswordInput(attrs={'required': True}),
        error_messages={'required': 'Este campo es requerido.'})

    def clean_pin(self):
        pin = self.cleaned_data.get('pin')

        if len(pin) < 6:
            raise ValidationError('El pin debe tener al menos 6 caracteres.')
        else:
            return pin

    def clean(self):
        cleaned_data = super(CrearBilleteraForm, self).clean()
        pin = cleaned_data.get('pin')
        pin2 = cleaned_data.get('pin2')

        if pin != pin2:
            self.add_error(
                'pin',
                ValidationError('Las claves no concuerdan!'))


class ClaveBilleteraForm(Form):
    pin = CharField(
        label='Pin',
        widget=PasswordInput(attrs={'required': True}),
        error_messages={'required': 'Este campo es requerido.'})
