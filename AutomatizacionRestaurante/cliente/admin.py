from django.contrib import admin

from .models import BilleteraElectronica, Cliente

admin.site.register(Cliente)
admin.site.register(BilleteraElectronica)
