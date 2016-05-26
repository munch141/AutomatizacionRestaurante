from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^registroCliente/$', views.registroCliente.as_view(), name='registroCliente'),
    url(r'^registroCliente/clienteRegistrado/$', views.clienteRegistrado, name='clienteRegistrado'),
    url(r'^registroProveedor/proveedorRegistrado/$', views.proveedorRegistrado, name='proveedorRegistrado'),
    url(r'^registroProveedor/$', views.registroProveedor.as_view(), name='registroProveedor')
	

]
