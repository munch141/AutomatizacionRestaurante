from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.administrador, name='administrador'),

	url(r'^Nuevo_menu/$',
        views.nuevo_menu,
        name='nuevo_menu'),

    url(r'^Nuevo_plato/$',
        views.nuevo_plato,
        name='nuevo_plato'),
]
