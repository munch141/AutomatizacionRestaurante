from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^registroCliente/$', views.registroCliente, name='registroCliente')
]