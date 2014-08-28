from django.conf.urls import patterns, include, url
from single_cinema import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'single_cinema.views.home', name='home'),
    # url(r'^single_cinema/', include('single_cinema.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index),
    url(r'^index$', views.index, name='index'),
    url(r'^home$', views.index, name='home'),
    url(r'^busy$', views.busy, name='busy'),
    url(r'^video$', views.video, name='video'),
    url(r'^stop/(?P<key>-?\d+)$', views.stop, name='stop'),
)
