# -*- coding: utf-8 -*-

from django import forms
from django.forms import CharField, ChoiceField, DateField, EmailField, Form,\
    IntegerField, RegexField, ValidationError
from django.forms.widgets import EmailInput, PasswordInput, TextInput
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Field, Layout, MultiWidgetField, Submit
from crispy_forms.bootstrap import PrependedText

from cliente.models import Cliente
from proveedor.models import Proveedor

SEXOS = (
    ('', '-'),
    ('M', 'M'),
    ('F', 'F')
)

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].label = "Nombre de usuario:"
        self.fields['password'].label = "Contraseña:"

        #crispy forms
        self.helper = FormHelper(self)
        self.helper.form_id = 'login_form'
        self.helper.layout = Layout(
            Field('username', id='username_field'),
            Field('password', id='password_field'),
            ButtonHolder(
                Submit('login', 'Entrar', css_class='btn-success')
            )
        )


class RegistroClienteForm(Form):
    def __init__(self, *args, **kwargs):
        super(RegistroClienteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'registro_cliente_form'
        self.helper.form_class = 'forms col-md-8'
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Registrarse'))
        self.helper.layout = Layout(
            Field('username', placeholder='username'),
            Field('nombre', placeholder='nombre'),
            Field('apellido', placeholder='apellido'),
            Field('ci', placeholder='cédula'),
            Field('email', placeholder='e.g. ejemplo@mail.com'),
            Field('telefono', placeholder='e.g. 0212-1234567'),
            MultiWidgetField('sexo', attrs=({'style': 'width: auto; display: '
                                                      'inline-block;'})),
            MultiWidgetField(
                'fecha_nacimiento',
                attrs=({'style': 'width: auto; display: inline-block;'})),
            Field('clave', placeholder='contraseña'),
            Field('clave2', placeholder='confirme contraseña'))

    username = RegexField(
        label='Nombre de usuario',
        regex=r'^[a-zA-Z0-9_@+.-]+$',
        error_messages={
            'invalid': 'El nombre de usuario sólo puede tener letras, números,'
                       ' "_", "@", "+", "." y "-".',
            'required': 'Este campo es requerido.'})

    ci = IntegerField(
        label='Cédula',
        widget=TextInput(),
        error_messages={
            'invalid': 'La cédula debe ser un número entero.',
            'required': 'Este campo es requerido.'})

    nombre = RegexField(
        label='Nombre',
        regex=r'^([a-zA-Z]+|[a-zA-Z]+\s[a-zA-Z]+)$',
        error_messages={
            'invalid': 'El nombre no puede contener números ni caracteres '
                       'especiales.',
            'required': 'Este campo es requerido.'})

    apellido = RegexField(
        label='Apellido',
        regex=r'^([a-zA-Z]+|[a-zA-Z]+\s[a-zA-Z]+)$',
        error_messages={
            'invalid': 'El apellido no puede contener números ni caracteres '
                       'especiales.',
            'required': 'Este campo es requerido.'})

    fecha_nacimiento = DateField(
        label='Fecha de nacimiento',
        widget=SelectDateWidget(years=range(1900, 2016)))

    email = EmailField(
        label='Correo electrónico',
        widget=EmailInput(),
        error_messages={'required': 'Este campo es requerido.'})

    telefono = RegexField(
        label='Teléfono',
        regex=r'^[0-9]{4}-[0-9]{7}$',
        error_messages={
            'invalid': 'El teléfono debe tener este formato: 0212-1234567',
            'required': 'Este campo es requerido.'})

    sexo = ChoiceField(
        label='Sexo',
        choices=SEXOS,
        error_messages={'required': 'Este campo es requerido.'})

    clave = CharField(
        label='Contraseña',
        widget=PasswordInput(),
        error_messages={'required': 'Este campo es requerido.'})

    clave2 = CharField(
        label='Confirme Contraseña',
        widget=PasswordInput(attrs={'required': True}),
        error_messages={'required': 'Este campo es requerido.'})


    def clean_username(self):
        try:
            User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError('El nombre de usuario ya existe. Intente de'
                                    ' nuevo.')

    def clean_ci(self):
        cedula = self.cleaned_data['ci']

        try:
            Cliente.objects.get(ci=cedula)
        except Cliente.DoesNotExist:
            if (cedula <= 9999999) or (99999999 < cedula):
                raise ValidationError('La cédula debe ser de 8 dígitos.')
            return cedula
        raise forms.ValidationError('Ya hay un usuario registrado con esa'
                                    ' cédula. Intente de nuevo.')

    def clean_clave(self):
        clave = self.cleaned_data.get('clave')

        if len(clave) < 6:
            raise ValidationError('La clave debe tener al menos 6 caracteres.')
        else:
            return clave

    def clean(self):
        cleaned_data = super(RegistroClienteForm, self).clean()
        clave = cleaned_data.get('clave')
        clave2 = cleaned_data.get('clave2')

        if clave != clave2:
            self.add_error(
                'clave',
                ValidationError('Las contraseñas no concuerdan!'))


class RegistroProveedorForm(Form):
    def __init__(self, *args, **kwargs):
        super(RegistroProveedorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'registro_proveedor_form'
        self.helper.form_class = 'forms col-md-7'
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Registrarse'))
        self.helper.layout = Layout(
            Field('username', placeholder='nombre de usuario'),
            PrependedText('rif', 'J -', placeholder='rif'),
            Field('nombre', placeholder='nombre'),
            Field('direccion', placeholder='dirección'),
            Field('email', placeholder='e.g. ejemplo@mail.com'),
            Field('telefono', placeholder='e.g. 0212-1234567'),
            Field('clave', placeholder='contraseña'),
            Field('clave2', placeholder='confirme contraseña'))

    username = RegexField(
        label='Nombre de usuario',
        regex=r'^[a-zA-Z0-9_@+.-]+$',
        error_messages={
            'invalid': 'El nombre de usuario sólo puede tener letras, números,'
                       ' "_", "@", "+", "." y "-".',
            'required': 'Este campo es requerido.'})

    rif = IntegerField(
        label='RIF',
        widget=TextInput(),
        error_messages={'invalid': 'El RIF debe ser un número entero.',
                        'required': 'Este campo es requerido.'})

    nombre = RegexField(
        label='Nombre',
        regex=r'^([a-zA-Z0-9.]+|[a-zA-Z0-9.]+\s[a-zA-Z0-9.]+)$',
        error_messages={
            'invalid': 'El nombre no puede contener números ni caracteres '
                       'especiales.',
            'required': 'Este campo es requerido.'})

    direccion = CharField(
        label='Dirección',
        error_messages={'required': 'Este campo es requerido.'})

    email = EmailField(
        label='Correo electrónico',
        widget=EmailInput())

    telefono = RegexField(
        label='Teléfono',
        regex=r'^[0-9]{4}-[0-9]{7}$',
        error_messages={
            'invalid': 'El teléfono debe tener este formato: 0212-1234567',
            'required': 'Este campo es requerido.'})

    clave = CharField(
        label='Contraseña',
        widget=PasswordInput(),
        error_messages={'required': 'Este campo es requerido.'})

    clave2 = CharField(
        label='Confirme Contraseña',
        widget=PasswordInput(attrs={'required': True}),
        error_messages={'required': 'Este campo es requerido.'})

    def clean_username(self):
        try:
            User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError('El nombre de usuario ya existe. Intente de'
                                    ' nuevo.')

    def clean_rif(self):
        rif = self.cleaned_data['rif']

        try:
            Proveedor.objects.get(rif=rif)
        except Proveedor.DoesNotExist:
            if (rif <= 99999) or (99999999 < rif):
                raise ValidationError('La cédula debe ser de 8 dígitos.') 
            return self.cleaned_data['rif']
        raise forms.ValidationError('Ya hay un usuario registrado con ese rif.'
                                    'Intente de nuevo.')

    def clean_clave(self):
        clave = self.cleaned_data.get('clave')

        if len(clave) < 6:
            raise ValidationError('La clave debe tener al menos 6 caracteres.')
        else:
            return clave

    def clean(self):
        cleaned_data = super(RegistroProveedorForm, self).clean()
        clave = cleaned_data.get('clave')
        clave2 = cleaned_data.get('clave2')

        if clave != clave2:
            self.add_error(
                'clave',
                ValidationError('Las contraseñas no concuerdan!'))
