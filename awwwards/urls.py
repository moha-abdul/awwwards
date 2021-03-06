from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns=[

    url(r'^$',views.home,name = 'home'),
    url(r'signup/', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^profile/',views.profile,name='profile'),
    url(r'^edit_profile/', views.edit_profile, name = 'edit_profile'),
    url(r'^add_project/', views.add_project, name = 'add_project'),
    url(r'^single_project/(\d+)', views.single_project, name = 'single_project'),
    url(r'^search_project/', views.search_project, name ='search_project'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)