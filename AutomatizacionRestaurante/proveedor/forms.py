# -*- coding: utf-8 -*-

from django.forms import EmailField, ModelForm, CharField
from django.contrib.auth.models import User
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Field, Layout, MultiWidgetField, Submit

from administrador.models import Ingrediente

from .models import Inventario


class EditarPerfilForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']

    email = EmailField(label='Correo electrónico')

class AgregarIngredienteForm(ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['nombre']

    nombre = CharField(label='Ingrediente')

class CrearInventarioForm(forms.ModelForm):
    ingredientes = forms.ModelMultipleChoiceField(queryset=Ingrediente.objects.all(), widget = forms.CheckboxSelectMultiple(attrs={'id': 'ingredientes'}))

    class Meta:
        model = Inventario
        fields = ['ingredientes']

    def __init__(self, *args, **kwargs):
        super(CrearInventarioForm, self).__init__(*args, **kwargs)

        #self.fields['ingredientes'].id = 'ingredientes'

        self.fields['ingredientes'].label = "Elija los ingredientes para el inventario:"
        self.fields['ingredientes'].required = False

class EditarInventarioForm(forms.ModelForm):
    ingredientes = forms.ModelMultipleChoiceField(
        queryset=Ingrediente.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'id': 'ingredientes'}))

    class Meta:
        model = Inventario
        fields = ['ingredientes']


    def __init__(self, *args, **kwargs):
        super(EditarInventarioForm, self).__init__(*args, **kwargs)

        self.fields['ingredientes'].label = "Elija los ingredientes para el inventario:"
        self.fields['ingredientes'].required = False
        

    

    
