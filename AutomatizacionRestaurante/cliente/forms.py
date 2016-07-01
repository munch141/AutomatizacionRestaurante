# -*- coding: utf-8 -*-
from django import forms
from django.forms import EmailField, ModelForm, CharField, Form, FloatField, \
RegexField, ValidationError
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, NumberInput, TextInput

from .models import Billetera
from administrador.models import Menu


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


class RecargaBilleteraForm(Form):
    nombre = RegexField(
        label='Nombre en tarjeta:',
        regex=r'^([a-zA-Z]+|[a-zA-Z]+\s[a-zA-Z]+)$',
        widget=TextInput(attrs={'placeholder': 'nombre en tarjeta'}),
        error_messages={
            'invalid': 'El nombre sólo puede tener letras y máximo 2 nombres.',
            'required': 'Este campo es requerido.'})

    numero = RegexField(
        label='Número de tarjeta:',
        regex=r'^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}$',
        widget=TextInput(attrs={'placeholder': 'número de tarjeta'}),
        error_messages={
            'invalid': 'El número de la tarjeta debe tener este formato: '
                       '0000-0000-0000-0000.',
            'required': 'Este campo es requerido.'})

    codigo = RegexField(
        label='Código de seguridad:',
        regex=r'^[0-9]{3}$',
        widget=TextInput(attrs={'placeholder': 'código de seguridad'}),
        error_messages={
            'invalid': 'El código de seguridad tiene que ser de 3 dígitos',
            'required': 'Este campo es requerido.'})

    monto = FloatField(
        label='Monto:',
        widget=NumberInput(attrs={'placeholder': 'monto'}),
        error_messages={'required': 'Este campo es requerido.'})

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto <= 0:
            raise ValidationError('El monto debe ser mayor que 0.')
        return monto

class ElegirPlatosForm(forms.Form):
    try:
        menu = Menu.objects.get(actual=True).incluye
    except:
        menu = Menu.objects.none()
    platos = forms.ModelMultipleChoiceField(
        queryset=menu,
        widget=forms.CheckboxSelectMultiple(),
        required=True,
        label='Elija los platos que desea ordenar:')

    def __init__(self, queryset, *args, **kwargs):
        super(ElegirPlatosForm, self).__init__(*args, **kwargs)
        self.fields['platos'].queryset = queryset

class TarjetaCreditoForm(Form):
    nombre = RegexField(
        label='Nombre en tarjeta:',
        regex=r'^([a-zA-Z]+|[a-zA-Z]+\s[a-zA-Z]+)$',
        widget=TextInput(attrs={'placeholder': 'nombre en tarjeta'}),
        error_messages={
            'invalid': 'El nombre sólo puede tener letras y máximo 2 nombres.',
            'required': 'Este campo es requerido.'})

    numero = RegexField(
        label='Número de tarjeta:',
        regex=r'^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}$',
        widget=TextInput(attrs={'placeholder': 'número de tarjeta'}),
        error_messages={
            'invalid': 'El número de la tarjeta debe tener este formato: '
                       '0000-0000-0000-0000.',
            'required': 'Este campo es requerido.'})

    codigo = RegexField(
        label='Código de seguridad:',
        regex=r'^[0-9]{3}$',
        widget=TextInput(attrs={'placeholder': 'código de seguridad'}),
        error_messages={
            'invalid': 'El código de seguridad tiene que ser de 3 dígitos',
            'required': 'Este campo es requerido.'})


    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto <= 0:
            raise ValidationError('El monto debe ser mayor que 0.')
        return monto
