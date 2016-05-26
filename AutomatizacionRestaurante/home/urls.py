from django.conf.urls import url
from . import views

urlpatterns = [ url(r'^$', views.LogIn, name='LogIn'),
				url(r'^perfil/$', views.perfil, name='perfil'),]
