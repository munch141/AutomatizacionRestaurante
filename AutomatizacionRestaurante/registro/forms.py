# -*- coding: utf-8 -*-

from django.forms import CharField, ChoiceField, DateField, EmailField, ModelForm, Form,\
    IntegerField, RegexField, ValidationError
from django.forms.widgets import EmailInput, PasswordInput, TextInput
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.models import User

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


class RegistroClienteForm(Form):
    def __init__(self, *args, **kwargs):
        super(RegistroClienteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'forms col-md-8'
        self.helper.form_method = 'post'
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
        regex=r'^[a-zA-Z]+$',
        error_messages={
            'invalid': 'El nombre no puede contener números ni caracteres '
                       'especiales.',
            'required': 'Este campo es requerido.'})

    apellido = RegexField(
        label='Apellido',
        regex=r'^[a-zA-Z]+$',
        error_messages={
            'invalid': 'El apellido no puede contener números ni caracteres '
                       'especiales.',
            'required': 'Este campo es requerido.'})

    fecha_nacimiento = DateField(
        label='Fecha de nacimiento',
        widget=SelectDateWidget(years=range(1900, 2016)))

    email = EmailField(
        label='Correo electrónico',
        widget=EmailInput())

    telefono = RegexField(
        label='Teléfono',
        regex=r'^[0-9]{4}-[0-9]{7}$',
        error_messages={
            'required': 'Este campo es requerido.',
            'invalid': 'El teléfono debe tener este formato: 0212-1234567'})

    sexo = ChoiceField(
        label='Sexo',
        choices=SEXOS)

    clave = CharField(
        label='Contraseña',
        widget=PasswordInput())

    clave2 = CharField(
        label='Confirme Contraseña',
        widget=PasswordInput(
            attrs={'required': True}))


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


class RegistroProveedorForm(Form):
    def __init__(self, *args, **kwargs):
        super(RegistroProveedorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'forms col-md-7'
        self.helper.form_method = 'post'
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
        regex=r'^[a-zA-Z]+$',
        error_messages={
            'invalid': 'El nombre no puede contener números ni caracteres '
                       'especiales.',
            'required': 'Este campo es requerido.'})

    direccion = CharField(
        label='Dirección')

    email = EmailField(
        label='Correo electrónico',
        widget=EmailInput())

    telefono = RegexField(
        label='Teléfono',
        regex=r'^[0-9]{4}-[0-9]{7}$',
        error_messages={
            'required': 'Este campo es requerido.',
            'invalid': 'El teléfono debe tener este formato: 0212-1234567'})

    clave = CharField(
        label='Contraseña',
        widget=PasswordInput())

    clave2 = CharField(
        label='Confirme Contraseña',
        widget=PasswordInput(attrs={'required': True}))

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
