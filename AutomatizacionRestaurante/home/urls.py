from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^perfil/$', views.perfil, name='perfil'),
    url(r'^perfil/actualizar/$', views.actualizar_perfil, name='actualizar_perfil')
]
