from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home_cliente'),

    url(r'^perfil/$', views.perfil, name='perfil_cliente'),

    url(r'^perfil/editar/$',
        views.editar_perfil,
        name='editar_perfil_cliente'),
]
