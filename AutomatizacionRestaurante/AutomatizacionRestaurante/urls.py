from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^registro/', include('registro.urls')),
    url(r'^home/', include('home.urls')),
    url(r'^admin/', admin.site.urls),
]
