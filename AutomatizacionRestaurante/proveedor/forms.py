# -*- coding: utf-8 -*-

from django.forms import EmailField, ModelForm, CharField, ValidationError
from django.contrib.auth.models import User
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Field, Layout, MultiWidgetField,\
                                Div, Submit

from administrador.models import Ingrediente, Ingrediente_inventario

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


class ElegirIngredientesForm(forms.Form):
    ingredientes = forms.ModelMultipleChoiceField(
        queryset=Ingrediente.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True,
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
                Div('precio',css_class='col-md-2',),
                css_class='row'))


class DetallesIngredienteInventarioForm(forms.ModelForm):
    class Meta:
        model = Ingrediente_inventario
        fields = ['ingrediente', 'precio']

    ingrediente = CharField(disabled=True, required=False)


class EliminarIngredientesForm(forms.Form):
    ingredientes = forms.ModelMultipleChoiceField(
        queryset= Ingrediente.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        required=True,
        label='Elija los ingredientes que desea eliminar:')

    def __init__(self, queryset, *args, **kwargs):
        super(EliminarIngredientesForm, self).__init__(*args, **kwargs)
        self.fields['ingredientes'].queryset = queryset
