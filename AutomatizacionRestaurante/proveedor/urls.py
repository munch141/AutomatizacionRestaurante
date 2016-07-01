from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home_proveedor'),

    url(r'^perfil/$', views.perfil, name='perfil_proveedor'),

    url(r'^perfil/editar/$',
        views.editar_perfil,
        name='editar_perfil_proveedor'),

    url(r'^editar_inventario$',
        views.editar_inventario,
        name='editar_inventario'),

    url(r'^editar_inventario/elegir_ingredientes$',
        views.elegir_ingredientes_inventario,
        name='elegir_ingredientes_inventario'),

    url(r'^editar_inventario/elegir_ingredientes/agregar_nuevo$',
        views.agregar_ingrediente,
        name='agregar_ingrediente_p'),

    url(r'^editar_inventario/elegir_ingredientes/detalles$',
        views.detalles_ingredientes_inventario,
        name='detalles_ingredientes_inventario'),
]
