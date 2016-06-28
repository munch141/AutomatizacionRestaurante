from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home_proveedor'),

    url(r'^perfil/$', views.perfil, name='perfil_proveedor'),

    url(r'^perfil/editar/$',
        views.editar_perfil,
        name='editar_perfil_proveedor'),

    url(r'^crear_inventario/$' , views.crear_inventario, name='crear_inventario'),

	url(r'^agregar_ingrediente/$' , views.agregar_ingrediente, name='agregar_ingrediente_proveedor'),

	url(r'^editar_inventario/$' , views.editar_inventario, name='editar_inventario'),

	url(r'^detalles_inventario/$' , views.detalles_inventario, name='detalles_inventario'),	
]
