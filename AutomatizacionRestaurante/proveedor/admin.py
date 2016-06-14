from django.contrib import admin

from .models import Proveedor, Inventario

admin.site.register(Proveedor)
admin.site.register(Inventario)
