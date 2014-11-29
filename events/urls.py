from django.conf.urls import patterns, url

urlpatterns = patterns('events.views',
    url(r'^event/edit/(?P<pk>\d*>)/$', 'event_edit', name='event-edit'),
    url(r'^member/edit/(?P<pk>\d*>)/$', 'member_edit', name='member-edit'),
)
