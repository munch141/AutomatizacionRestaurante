# -*- coding: utf-8 -*-

from django import forms
from django.forms import RegexField, CharField, DateField, ValidationError, EmailField, MultipleChoiceField, IntegerField
from django.forms.widgets import PasswordInput, EmailInput, TextInput, DateInput, Select
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.models import User

from .models import Cliente
from .models import Proveedor

SEXOS = (
     ('M','Masculino'),
     ('F','Femenino')    
)

class RegistroClienteForm(forms.Form):
    username = RegexField(
                  label = "Nombre de usuario", 
                  widget = TextInput(attrs={'placeholder':'nombre de usuario',\
                                           'required':True, 'max_length':30}),
                  error_messages={
                        'invalid': 'This value must contain only letters, '\
                                     'numbers and underscores.'},
                  regex=r'^\w+$'
    )
    
    ci = IntegerField(
            label = 'Cédula',
            widget = TextInput(attrs={'placeholder': 'cédula', 'required': True}),
    )

    nombre = CharField(
            label = 'Nombre',
            widget = TextInput(attrs={'placeholder': 'nombre', 'required': True}),
    )

    apellido = CharField(
            label = 'Apellido',
            widget = TextInput(attrs={'placeholder': 'apellido', 'required': True}),
    )

    fecha_nacimiento = DateField(
            label = 'Fecha de nacimiento',
            widget = SelectDateWidget(years = range(1900,2016)),
    )

    email = EmailField(
            label = 'Correo electrónico',
            widget = EmailInput(attrs={'placeholder': 'e.g. example@mail.com',\
                                       'required': True}),
    )

    telefono = CharField(
            label = 'Teléfono',
            widget = TextInput(attrs={'placeholder': 'e.g. 0555-1234567',\
                                      'pattern': '[0-9]{4}-[0-9]{7}',\
                                      'required': True}),
    )

    sexo = MultipleChoiceField(required = False,
              label = 'Sexo',
              widget = Select(choices = SEXOS)
    )

    clave = CharField(
                  label='Contraseña',
                  widget=PasswordInput(attrs={'placeholder': 'contraseña',
                                              'required': True})
    )

    clave2 = CharField(
                  label='Confirme Contraseña',
                  widget=PasswordInput(attrs={'placeholder': 'confirme '\
                                                             'contraseña',
                                              'required': True})
    )

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError('El nombre de usuario ya existe. Intente de'\
                                    ' nuevo.')

    def clean_ci(self):
        try:
            cliente = Cliente.objects.get(ci=self.cleaned_data['ci'])
        except Cliente.DoesNotExist:
            return self.cleaned_data['ci']
        raise forms.ValidationError('Ya hay un usuario registrado con esa'\
                                    ' cédula. Intente de nuevo.')

    def clean_clave2(self):
        clave = self.cleaned_data.get('clave')
        clave2 = self.cleaned_data.get('clave2')

        if clave != clave2:
            raise ValidationError("Las contraseñas no concuerdan!")
        return clave2

class RegistroProveedorForm(forms.Form):
    username = RegexField(
                  label = "Nombre de usuario", 
                  widget = TextInput(attrs={'placeholder':'nombre de usuario',\
                                           'required':True, 'max_length':30}),
                  error_messages={
                        'invalid': 'This value must contain only letters, '\
                                     'numbers and underscores.'},
                  regex=r'^\w+$'
    )
    
    rif = IntegerField(
            label = 'Rif',
            widget = TextInput(attrs={'placeholder': 'rif', 'required': True}),
    )

    nombre = CharField(
            label = 'Nombre Proveedor',
            widget = TextInput(attrs={'placeholder': 'nombre', 'required': True}),
    )


    direccion = CharField(
            label = 'Dirección',
            widget = TextInput(attrs={'placeholder': 'direccion', 'required': True}),
    )

    email = EmailField(
            label = 'Correo electrónico',
            widget = EmailInput(attrs={'placeholder': 'e.g. example@mail.com',\
                                       'required': True}),
    )

    telefono = CharField(
            label = 'Teléfono',
            widget = TextInput(attrs={'placeholder': 'e.g. 0555-1234567',\
                                      'pattern': '[0-9]{4}-[0-9]{7}',\
                                      'required': True}),
    )

    clave = CharField(
                  label='Contraseña',
                  widget=PasswordInput(attrs={'placeholder': 'contraseña',
                                              'required': True})
    )

    clave2 = CharField(
                  label='Confirme Contraseña',
                  widget=PasswordInput(attrs={'placeholder': 'confirme '\
                                                             'contraseña',
                                              'required': True})
    )

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError('El nombre de usuario ya existe. Intente de'\
                                    ' nuevo.')

    def clean_rif(self):
        try:
            proveedor = Proveedor.objects.get(rif=self.cleaned_data['rif'])
        except Proveedor.DoesNotExist:
            return self.cleaned_data['rif']
        raise forms.ValidationError('Ya hay un usuario registrado con ese rif.'\
                                    'Intente de nuevo.')

    def clean_clave2(self):
        clave = self.cleaned_data.get('clave')
        clave2 = self.cleaned_data.get('clave2')

        if clave != clave2:
            raise ValidationError("Las contraseñas no concuerdan!")
        return clave2