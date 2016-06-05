from django.conf.urls import include, url
from django.contrib import admin
from cuentas.views import LoginView

from cuentas.views import home

urlpatterns = [
    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^home/$', home, name='home'),
    url(r'^cuentas/', include('cuentas.urls')),
    url(r'^cliente/', include('cliente.urls')),
    url(r'^proveedor/', include('proveedor.urls')),
    url(r'^admin/', admin.site.urls),
]
