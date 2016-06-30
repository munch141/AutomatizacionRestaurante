from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home_proveedor'),

    url(r'^perfil/$', views.perfil, name='perfil_proveedor'),

    url(r'^perfil/editar/$',
        views.editar_perfil,
        name='editar_perfil_proveedor'),

    url(r'^crear_inventario/ingredientes/$',
        views.crear_inventario_1,
        name='crear_inventario_1'),

    url(r'^crear_inventario/ingredientes/precios_cantidades$',
        views.crear_inventario_2,
        name='crear_inventario_2'),

	url(r'^agregar_ingrediente/$',
        views.agregar_ingrediente,
        name='agregar_ingrediente_proveedor'),	
]
