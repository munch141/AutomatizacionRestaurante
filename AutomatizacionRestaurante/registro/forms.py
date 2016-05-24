# -*- coding: utf-8 -*-

from django.forms import ModelForm, CharField, ValidationError
from django.forms.widgets import PasswordInput, EmailInput, TextInput, DateInput
from django.forms.extras.widgets import SelectDateWidget

from .models import Cliente

class ClienteForm(ModelForm):
    clave2 = CharField(
                  label='Confirme Contraseña',
                  widget=PasswordInput(attrs={'placeholder': 'confirme '\
                                                             'contraseña',
                                              'required': True})
                  )
    
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
          'ci': TextInput(attrs={'placeholder': 'cédula',
                                 'required': True}),
          'nombre': TextInput(attrs={'placeholder': 'nombre',
                                     'required': True}),
          'apellido': TextInput(attrs={'placeholder': 'apellido',
                                       'required': True}),
          'fecha_nacimiento': SelectDateWidget(years = range(1900,2016)),

          'email': EmailInput(attrs={'placeholder': 'e.g. example@mail.com',
                                     'required': True}),
          'telefono': TextInput(attrs={'placeholder': 'e.g. 0555-1234567',
                                       'pattern': '[0-9]{4}-[0-9]{7}',
                                       'required': True}),
          'clave': PasswordInput(attrs={'placeholder': 'contraseña',
                                        'required': True})
        } 
        labels = {
          'ci': 'Cédula',
          'nombre': 'Nombre',
          'apellido': 'Apellido',
          'fecha_nacimiento': 'Fecha de nacimiento',
          'sexo': 'Sexo',
          'email': 'Correo electrónico',
          'telefono': 'Teléfono',
          'clave': 'Contraseña'
        }

    def clean_clave2(self):
        clave = self.cleaned_data.get('clave')
        clave2 = self.cleaned_data.get('clave2')

        if clave != clave2:
            raise ValidationError("Las contraseñas no concuerdan!")
        return clave2