from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^perfil/$', views.perfil, name='perfil'),

    url(r'^perfil/editar/$',
        views.editar_perfil,
        name='editar_perfil')
]
