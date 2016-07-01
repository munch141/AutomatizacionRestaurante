# -*- coding: utf-8 -*-

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Field, Layout, MultiWidgetField, Submit, Div

from .models import Menu, Plato, Ingrediente, Tiene


class CrearMenuForm(forms.ModelForm):
    incluye = forms.ModelMultipleChoiceField(
        queryset=Plato.objects.all(),
        widget=forms.CheckboxSelectMultiple())
    
    class Meta:
        model = Menu
        fields = ['nombre', 'incluye', 'actual']
        widgets  = {
            'nombre': forms.TextInput(attrs={'id': 'nombre'}),
            'actual': forms.CheckboxInput(attrs={'id': 'actual'})
        }

    def __init__(self, *args, **kwargs):
        super(CrearMenuForm, self).__init__(*args, **kwargs)

        self.fields['incluye'].field = forms.ModelMultipleChoiceField(
            queryset=Plato.objects.all())
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

        self.fields['contiene'].field = forms.ModelMultipleChoiceField(
            queryset=Ingrediente.objects.all())
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


class EditarMenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['nombre', 'actual']
        widgets  = {
            'nombre': forms.TextInput(attrs={'id': 'nombre'}),
            'actual': forms.CheckboxInput(attrs={'id': 'actual'})
        }

    def __init__(self, *args, **kwargs):
        super(EditarMenuForm, self).__init__(*args, **kwargs)
        self.fields['actual'].label = "¿Desea que este sea el menú actual?"


class IngredientePlatoFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(IngredientePlatoFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'POST'
        self.form_tag = False
        self
        self.layout = Layout(
            Div(
                Div('ingrediente',css_class='col-md-3',),
                Div('requiere',css_class='col-md-2',),
                css_class='row'))


class DetallesIngredientePlatoForm(forms.ModelForm):
    class Meta:
        model = Tiene
        fields = ['ingrediente', 'requiere']

    ingrediente = forms.CharField(disabled=True, required=False)

    def clean_requiere(self):
        requiere = self.cleaned_data['requiere']
        if requiere <= 0:
            raise forms.ValidationError(
                'La cantidad del ingrediente debe ser mayor a 0.')
        return requiere
