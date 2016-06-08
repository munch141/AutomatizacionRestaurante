from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home_administrador'),
    url(r'^ver_clientes/$', views.ver_clientes, name='ver_clientes'),
]
