from django.conf.urls import url
from . import views

from home.views import editarPerfilView


urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^perfil/$', views.perfil, name='perfil'),
	url(r'^$', views.home, name='home'),
	url(r'^editarPerfil/$', editarPerfilView.as_view(), name='editarPerfil'),
	url(r'^perfilAct/$', views.perfilAct, name='perfilAct'),
]
