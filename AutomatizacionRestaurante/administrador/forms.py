# -*- coding: utf-8 -*-

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Field, Layout, MultiWidgetField, Submit

from .models import Menu, Plato

class CrearMenuForm(forms.ModelForm):
    incluye = forms.ModelMultipleChoiceField(
        queryset=Plato.objects.all(), widget=forms.CheckboxSelectMultiple())
    
    class Meta:
        model = Menu
        fields = ['nombre', 'incluye', 'actual']

    def __init__(self, *args, **kwargs):
        super(CrearMenuForm, self).__init__(*args, **kwargs)

        self.fields['nombre'].id = 'nombre'
        self.fields['actual'].id = 'actual'
        self.fields['incluye'].id = 'incluye'

        self.fields['incluye'].label = "Elija los platos del menú:"
        self.fields['incluye'].required = False
        self.fields['actual'].label = "¿Desea que este sea el menú actual?"
