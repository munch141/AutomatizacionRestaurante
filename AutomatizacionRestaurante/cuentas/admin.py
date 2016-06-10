from django.contrib import admin

from .models import Cliente
from .models import Proveedor, Inventario

admin.site.register(Cliente)
admin.site.register(Proveedor)
admin.site.register(Inventario)
