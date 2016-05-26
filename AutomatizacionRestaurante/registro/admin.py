from django.contrib import admin

from .models import Cliente
from .models import Proveedor

admin.site.register(Cliente)
admin.site.register(Proveedor)
