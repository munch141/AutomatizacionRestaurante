# -*- coding: utf-8 -*-

from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Field, Layout, Submit

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
