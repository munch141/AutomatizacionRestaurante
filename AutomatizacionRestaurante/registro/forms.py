# -*- coding: utf-8 -*-

from django.forms import CharField, ChoiceField, DateField, EmailField,\
    IntegerField, RegexField, ValidationError
from django.forms.widgets import EmailInput, PasswordInput, Select,\
    TextInput
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.models import User
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, MultiWidgetField, Submit
from crispy_forms.bootstrap import PrependedText

from .models import Cliente
from .models import Proveedor

SEXOS = (
    ('', '-'),
    ('M', 'M'),
    ('F', 'F')
)


class RegistroClienteForm(forms.Form):
    username = RegexField(label='Nombre de usuario',
                          regex=r'^\w+$',
                          error_messages={'invalid': 'El nombre de usuario sólo'
                                                     'puede tener letras, númer'
                                                     'os y _.',
                                          'required': 'Este campo es requerido.'})
    ci = IntegerField(label='Cédula',
                      widget=TextInput(),
                      error_messages={'invalid': 'La cédula debe ser un número'
                                                 ' entero.',
                                      'required': 'Este campo es requerido.'})
    nombre = RegexField(label='Nombre',
                        regex=r'^[a-zA-Z]+$',
                        error_messages={'invalid': 'El nombre no puede contener'
                                                   ' números ni caracteres espe'
                                                   'ciales.',
                                        'required': 'Este campo es requerido.'})
    apellido = RegexField(label='Apellido',
                          regex=r'^[a-zA-Z]+$',
                          error_messages={'invalid': 'El apellido no puede cont'
                                                     'ener números ni caracter'
                                                     'es especiales.',
                                          'required': 'Este campo es requerido.'})
    fecha_nacimiento = DateField(label='Fecha de nacimiento',
                                 widget=SelectDateWidget(years=range(1900, 
                                                                     2016)))
    email = EmailField(label='Correo electrónico', widget=EmailInput())
    telefono = RegexField(label='Teléfono',
                          regex=r'^[0-9]{4}-[0-9]{7}$',
                          error_messages={'invalid': 'El teléfono debe tener es'
                                                     'te formato: 1234-1234567',
                                          'required': 'Este campo es requerido.'})
    sexo = ChoiceField(label='Sexo', choices=SEXOS)
    clave = CharField(label='Contraseña',
                      widget=PasswordInput(attrs={'placeholder': 'contraseña',
                                                  'required': True}))
    clave2 = CharField(label='Confirme Contraseña',
                       widget=PasswordInput(attrs={'placeholder': 'confirme '
                                                                  'contraseña',
                                                   'required': True}))
    helper = FormHelper()
    helper.form_class = 'forms'
    helper.form_method = 'post'
    helper.disable_csrf = False
    helper.add_input(Submit('submit', 'Registrarse'))
    helper.layout = Layout(
        Field('username', placeholder='username'),
        Field('nombre', placeholder='nombre'),
        Field('apellido', placeholder='apellido'),
        Field('ci', placeholder='cédula'),
        Field('email', placeholder='e.g. ejemplo@mail.com'),
        Field('telefono', placeholder='e.g. 0212-1234567'),
        MultiWidgetField('sexo', attrs=({'style': 'width: auto; display: inline-block;'})),
        MultiWidgetField(
            'fecha_nacimiento',
            attrs=({'style': 'width: auto; display: inline-block;'})),
        'clave',
        'clave2')

    def clean_username(self):
        try:
            User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError('El nombre de usuario ya existe. Intente de'
                                    ' nuevo.')

    def clean_ci(self):
        try:
            Cliente.objects.get(ci=self.cleaned_data['ci'])
        except Cliente.DoesNotExist:
            return self.cleaned_data['ci']
        raise forms.ValidationError('Ya hay un usuario registrado con esa'
                                    ' cédula. Intente de nuevo.')

    def clean_claves(self):
        clave = self.cleaned_data.get('clave')
        clave2 = self.cleaned_data.get('clave2')

        if clave != clave2:
            raise ValidationError("Las contraseñas no concuerdan!")
        return clave2


class RegistroProveedorForm(forms.Form):
    username = RegexField(label="Nombre de usuario",
                          widget=TextInput(attrs={'placeholder': 'nombre de us'
                                                                 'uario',
                                                  'required': True,
                                                  'max_length': 30}),
                          error_messages={'invalid': 'This value must contain '
                                                     'only letters, numbers an'
                                                     'd underscores.'},
                          regex=r'^\w+$')
    rif = IntegerField(label='RIF',
                       widget=TextInput(),
                       error_messages={'invalid': 'El RIF debe ser un número'
                                                  ' entero.',
                                       'required': 'Este campo es requerido.'})
    nombre = RegexField(label='Nombre',
                        regex=r'^[a-zA-Z]+$',
                        error_messages={'invalid': 'El nombre no puede contener'
                                                   ' números ni caracteres espe'
                                                   'ciales.',
                                        'required': 'Este campo es requerido.'})
    direccion = CharField(label='Dirección', widget=TextInput())
    email = EmailField(label='Correo electrónico',
                       widget=EmailInput(attrs={'placeholder': 'e.g. ejemplo@m'
                                                               'ail.com',
                                                'required': True}))
    telefono = RegexField(label='Teléfono',
                          regex=r'^[0-9]{4}-[0-9]{7}$',
                          error_messages={'invalid': 'El teléfono debe tener es'
                                                     'te formato: 1234-1234567',
                                          'required': 'Este campo es requerido.'})
    clave = CharField(label='Contraseña',
                      widget=PasswordInput(attrs={'placeholder': 'contraseña',
                                                  'required': True}))
    clave2 = CharField(label='Confirme Contraseña',
                       widget=PasswordInput(attrs={'placeholder': 'confirme '
                                                                  'contraseña',
                                                   'required': True}))


    helper = FormHelper()
    helper.form_class = 'forms'
    helper.form_action = '/registro/registroProveedor/'
    helper.form_method = 'post'
    helper.add_input(Submit('submit', 'Registrarse'))
    helper.layout = Layout(
        Field('username', css_class='input-md'),
        PrependedText('rif', 'J -'),
        Field('nombre', placeholder='nombre'),
        Field('direccion', placeholder='dirección'),
        Field('email', placeholder='e.g. ejemplo@mail.com'),
        Field('telefono', placeholder='e.g. 0212-1234567'),
        'clave',
        'clave2')

    def clean_username(self):
        try:
            User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError('El nombre de usuario ya existe. Intente de'
                                    ' nuevo.')

    def clean_rif(self):
        try:
            Proveedor.objects.get(rif=self.cleaned_data['rif'])
        except Proveedor.DoesNotExist:
            return self.cleaned_data['rif']
        raise forms.ValidationError('Ya hay un usuario registrado con ese rif.'
                                    'Intente de nuevo.')

    def clean_claves_iguales(self):
        clave = self.cleaned_data.get('clave')
        clave2 = self.cleaned_data.get('clave2')

        if clave != clave2:
            raise ValidationError("Las contraseñas no concuerdan!")
        return clave2
