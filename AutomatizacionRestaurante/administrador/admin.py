from django.contrib import admin

from .models import Administrador, Ingrediente, Ingrediente_inventario, Menu, Plato

admin.site.register(Administrador)
admin.site.register(Ingrediente)
admin.site.register(Menu)
admin.site.register(Plato)
admin.site.register(Ingrediente_inventario)
