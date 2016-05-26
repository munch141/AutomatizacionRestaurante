# -*- coding: utf-8 -*-

from django import forms
from django.forms import RegexField, CharField, ValidationError                      
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.models import User

class LogInForm(forms.Form):
    username = RegexField(
                  label = "Nombre de usuario", 
                  widget = TextInput(attrs={'placeholder':'nombre de usuario',\
                                           'required':True, 'max_length':30}),
                  error_messages={
                        'invalid': 'This value must contain only letters, '\
                                     'numbers and underscores.'},
                  regex=r'^\w+$'
    )
    
    clave = CharField(
            label = 'Contraseña',
            widget = PasswordInput(attrs={'placeholder': 'contraseña', 'required': True}),
    )

    def clean_username(self):
        usuario = User.objects.get(username=self.cleaned_data['username'])
        if usuario == None:
            raise ValidationError("Nombre de usuario no existente")
        return usuario	   	 
