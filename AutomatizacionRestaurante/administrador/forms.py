# -*- coding: utf-8 -*-

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Field, Layout, MultiWidgetField, Submit

from .models import Menu, Plato, Ingrediente


class CrearMenuForm(forms.ModelForm):
    incluye = forms.ModelMultipleChoiceField(
        queryset=Plato.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'id': 'incluye'}))
    
    class Meta:
        model = Menu
        fields = ['nombre', 'incluye', 'actual']
        widgets  = {
            'nombre': forms.TextInput(attrs={'id': 'nombre'}),
            'actual': forms.CheckboxInput(attrs={'id': 'actual'})
        }

    def __init__(self, *args, **kwargs):
        super(CrearMenuForm, self).__init__(*args, **kwargs)

        self.fields['incluye'].label = "Elija los platos del menú:"
        self.fields['incluye'].required = False
        self.fields['actual'].label = "¿Desea que este sea el menú actual?"


class CrearPlatoForm(forms.ModelForm):
    contiene = forms.ModelMultipleChoiceField(
        queryset=Ingrediente.objects.all(),
        widget=forms.CheckboxSelectMultiple())
    
    class Meta:
        model = Plato
        fields = ['nombre', 'descripcion', 'precio', 'contiene']

    def __init__(self, *args, **kwargs):
        super(CrearPlatoForm, self).__init__(*args, **kwargs)

        self.fields['contiene'].label = "Elija los ingredientes del plato:"

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')

        if precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor que 0.')
        else:
            return precio


class AgregarIngredienteForm(forms.ModelForm):    
    class Meta:
        model = Ingrediente
        fields = ['nombre']
