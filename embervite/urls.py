from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'embervite.views.index', name='index'),
    url(r'^login/$', 'embervite.views.login', name='login'),
    url(r'^logout/$', 'embervite.views.logout', name='logout'),
    url(r'^ev/', include('events.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
