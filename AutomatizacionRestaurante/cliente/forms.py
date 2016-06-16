# -*- coding: utf-8 -*-

from django.forms import EmailField, ModelForm, CharField, Form, FloatField, \
RegexField
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, NumberInput

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field


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


class RecargaBilleteraForm(Form):
    def __init__(self, *args, **kwargs):
        super(RecargaBilleteraForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'recargar_biletera_form'
        self.helper.form_class = 'forms col-md-8'
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Recargar', css_class='btn-success'))
        self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn btn-default'))
        self.helper.layout = Layout(
            Field('numero', placeholder='e.g. 0000-0000-0000-0000'),
            Field('nombre', placeholder='Nombre'),
            Field('codigo', placeholder='Codigo'),
            Field('monto', placeholder='Monto'))
        
    monto = FloatField(
        label='monto',
        widget=NumberInput(attrs={ 'min': '0'}),
        error_messages={'required':'Este campo es requerido.'})

    nombre = RegexField(
        label='Nombre en Tarjeta',
        regex=r'^([a-zA-Z]+|[a-zA-Z]+\s[a-zA-Z]+)$',
        error_messages={
            'invalid': 'El nombre de usuario sólo puede tener letras',
            'required': 'Este campo es requerido.'})

    numero = RegexField(
        label='Numero Tarjeta',
        regex=r'^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}$',
        error_messages={
            'invalid': 'El número de la tarjeta debe tener este formato: 0000-0000-0000-0000',
            'required': 'Este campo es requerido.'})

    codigo = RegexField(
        label='Codigo de Seguridad',
        regex=r'^[0-9]{3}$',
        error_messages={
            'invalid': 'El código de seguridad tiene que ser de 3 dígitos',
            'required': 'Este campo es requerido.'})
