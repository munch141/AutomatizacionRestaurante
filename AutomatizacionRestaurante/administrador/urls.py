from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home_administrador'),

    url(r'^ver_clientes/$', views.ver_clientes, name='ver_clientes'),

    url(r'^ver_clientes/([a-zA-Z0-9_@+.-]+)$',
        views.detalles_cliente,
        name='detalles_cliente'),

    url(r'^crear_menu/$', views.crear_menu, name='crear_menu'),

    url(r'^crear_plato/$', views.crear_plato, name='crear_plato'),

    url(r'^crear_plato/detalles_ingredientes$',
        views.detalles_ingredientes_plato,
        name='detalles_ingredientes_plato'),

    url(r'^agregar_ingrediente/$', views.agregar_ingrediente, name='agregar_ingrediente'),

    url(r'^ver_menus/$', views.ver_menus, name='ver_menus'),

    url(r'^ver_menu/(?P<nombre>.+)$',
        views.detalles_menu,
        name='detalles_menu'),

    url(r'^editar_menu/(?P<nombre>.+)$',
        views.editar_menu,
        name='editar_menu'),

    url(r'^ver_proveedores/$', views.ver_proveedores, name='ver_proveedores'),

    url(r'^ver_proveedores/([a-zA-Z0-9_@+.-]+)$',
        views.detalles_proveedor,
        name='detalles_proveedor'),

    url(r'^ver_platos/$', views.ver_platos, name='ver_platos'),

    url(r'^ver_platos/(?P<nombre>.+)$',
        views.detalles_plato,
        name='detalles_plato1'),

    url(r'^ver_ingredientes/$', views.ver_ingredientes, name='ver_ingredientes'),

    url(r'^ver_inventario/$', views.ver_inventario, name='ver_inventario'),
]
