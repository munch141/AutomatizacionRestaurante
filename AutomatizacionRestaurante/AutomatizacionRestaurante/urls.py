from django.conf.urls import include, url
from django.contrib import admin

from home.views import LoginView, logout_view

urlpatterns = [
    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^registro/', include('registro.urls')),
    url(r'^home/', include('home.urls')),
    url(r'^admin/', admin.site.urls),
]
