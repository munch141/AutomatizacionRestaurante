# -*- coding: utf-8 -*-

from django.forms import EmailField, ModelForm
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Layout, Submit
from django.contrib.auth.models import User


class EditarPerfilClienteForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']

    email = EmailField(label='Correo electrónico')

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        #crispy forms
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
