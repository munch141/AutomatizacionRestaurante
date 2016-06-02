# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Field, Layout, Submit
from django.forms import CharField, EmailField, RegexField
from django.forms.widgets import EmailInput


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].label = "Nombre de usuario:"
        self.fields['password'].label = "Contraseña:"

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            ButtonHolder(
                Submit('login', 'Entrar', css_class='btn-success')
            )
        )

class editarPerfilForm(forms.Form):
    email = EmailField(label='Correo electrónico', widget=EmailInput())
    telefono = RegexField(label='Teléfono',
                          regex=r'^[0-9]{4}-[0-9]{7}$',
                          error_messages={'invalid': 'El teléfono debe tener es'
                                                     'te formato: 1234-1234567',
                                          'required': 'Este campo es requerido.'})
