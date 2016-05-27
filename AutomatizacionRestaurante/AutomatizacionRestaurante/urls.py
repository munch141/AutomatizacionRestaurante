from django.conf.urls import include, url
from django.contrib.auth.views import login
from django.contrib import admin

from home.views import logout_view

urlpatterns = [
	url(r'^$', login),
	url(r'^logout/$', logout_view),
    url(r'^registro/', include('registro.urls')),
    url(r'^home/', include('home.urls')),
    url(r'^admin/', admin.site.urls),
]