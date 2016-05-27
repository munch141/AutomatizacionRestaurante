from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^registroCliente/$', views.registroCliente.as_view(), name='registroCliente'),
    url(r'^registroProveedor/$', views.registroProveedor.as_view(), name='registroProveedor'),
    url(r'^registroCliente/exito/$', views.usuarioRegistrado, name='exitoC'),
    url(r'^registroProveedor/exito/$', views.usuarioRegistrado, name='exitoP'),
]
