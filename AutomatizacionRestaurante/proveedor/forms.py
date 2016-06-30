# -*- coding: utf-8 -*-

from django.forms import EmailField, ModelForm, CharField,ValidationError
from django.contrib.auth.models import User
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Field, Layout, MultiWidgetField,\
                                Div, Submit

from administrador.models import Ingrediente

from .models import Ingrediente_inventario, Inventario


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

class CrearInventarioForm1(forms.Form):
    ingredientes = forms.ModelMultipleChoiceField(
        queryset=Ingrediente.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label='Elija los ingredientes del inventario:')


class IngredienteInventarioFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(IngredienteInventarioFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'POST'
        self.form_tag = False
        self
        self.layout = Layout(
            Div(
                Div('ingrediente',css_class='col-md-3',),
                Div('cantidad',css_class='col-md-2',),
                Div('precio',css_class='col-md-2',),
                css_class='row'))

class IngredienteInventarioForm(forms.ModelForm):
    class Meta:
        model = Ingrediente_inventario
        fields = ['ingrediente', 'cantidad', 'precio']

    ingrediente = CharField(disabled=True)

    def clean_precio(self):
        if precio < 0:
            raise ValidationError('El precio debe ser mayor que 0!')
