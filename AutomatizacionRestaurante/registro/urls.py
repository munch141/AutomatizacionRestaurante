from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^registro_cliente/$',
        views.registro_cliente,
        name='registro_cliente'),

    url(r'^registro_proveedor/$',
        views.registro_proveedor,
        name='registro_proveedor'),

    url(r'^exito/$', views.usuario_registrado, name='exito'),
]
