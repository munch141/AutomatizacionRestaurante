from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home_cliente'),

    url(r'^perfil/$', views.perfil, name='perfil_cliente'),

    url(r'^perfil/editar/$',
        views.editar_perfil,
        name='editar_perfil_cliente'),

    url(r'^crear_billetera/$', views.crear_billetera, name='crear_billetera'),

    url(r'^consultar_saldo/$', views.consultar_saldo, name='consultar_saldo'),

    url(r'^recargar_saldo/$', views.recargar_saldo, name='recargar_saldo'),

    url(r'^ver_menu/$', views.ver_plato, name='ver_menu'),

    url(r'^detalles_plato/(?P<nombre>.+)$', views.detalle_plato, name='detalles_plato'),

    url(r'^elegir_platos/$', views.elegir_platos, name='elegir_platos'),

    url(r'^pagar_pedido/$', views.pagar_pedido, name='pagar_pedido'),

    url(r'^tarjeta_credito/([0-9]+.[0-9]+)$', views.tarjeta_credito, name='tarjeta_credito'),

    url(r'^billetera/([0-9]+.[0-9]+)$', views.billetera, name='billetera'),

]
