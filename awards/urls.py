from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'', include('awwwards.urls')),
    url(r'^logout/$', views.logout, {"next_page": '/'}),
]
