from django.forms import ModelForm,  CharField
from .models import Cliente
from django.forms.widgets import PasswordInput, EmailInput, TextInput, DateInput
from django.forms.fields import RegexField

class ClienteForm(ModelForm):
    telefono = RegexField(label = 'Teléfono',
                          error_messages={'invalid':'El formato del teléfono'\
                                          ' debe ser XXXX-XXXXXXX'},
                          widget=TextInput(attrs={'placeholder': 'Teléfono',
                                                  'required': True}),
                          regex='[0-9]{3}-[0-9]{7}'
                          )
    clave = CharField(label='Contraseña',
                       widget=PasswordInput(
                                    attrs={'placeholder': 'Contraseña',
                                           'required': True})
                       )
    clave2 = CharField(label='Confirme Contraseña',
                       widget=PasswordInput(
                                    attrs={'placeholder': 'Confirme contraseña',
                                           'required': True})
                       )
    
    class Meta:
        model = Cliente
        exclude = ['telefono', 'clave']
        widgets = {
            'ci': TextInput(attrs={'placeholder': 'Cédula',
                                   'required': True}),
            'nombre': TextInput(attrs={'placeholder': 'Nombre',
                                       'required': True}),
            'apellido': TextInput(attrs={'placeholder': 'Apellido',
                                         'required': True}),
            'fecha_nacimiento': DateInput(attrs={'placeholder': 'Fecha de Nacimiento',
                                                 'required': True}),
            'email': EmailInput(attrs={'placeholder': 'Email',
                                       'required': True}),
            }
        
        labels = {
            'ci': 'Cédula',
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'sexo': 'Sexo',
            'email': 'Correo electrónico',
            }