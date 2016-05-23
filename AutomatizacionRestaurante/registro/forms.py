from django.forms import ModelForm,  CharField
from .models import Cliente
from django.forms.widgets import PasswordInput, EmailInput, TextInput, DateInput
from django.forms.fields import RegexField

class ClienteForm(ModelForm):
    clave2 = CharField(label='Repita Contraseña',
                       widget=PasswordInput(
                                    attrs={'placeholder': 'Confirme contraseña',
                                           'required': True})
                       )
    telefono = RegexField(error_messages={'invalid':'El formato del teléfono'\
                                          ' debe ser XXXX-XXXXXXX'},
                          widget=TextInput(attrs={'placeholder': 'Teléfono',
                                                  'required': True}),
                          regex='[0-9]{3}-[0-9]{7}',
                          )
    
    class Meta:
        model = Cliente
        exclude = ['telefono']
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
            'clave': PasswordInput(attrs={'placeholder': 'Contraseña',
                                       'required': True}),
            }
        
        labels = {
            'ci': 'Cédula',
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
            'sexo': 'Sexo',
            'clave': 'Contraseña'
            }