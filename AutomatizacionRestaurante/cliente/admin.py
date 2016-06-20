from django.contrib import admin

from .models import Billetera, Cliente, Historial

admin.site.register(Cliente)
admin.site.register(Billetera)
admin.site.register(Historial)
