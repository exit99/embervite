from django.conf.urls import patterns, url

urlpatterns = patterns('events.views',
    url(r'^event/edit/(\d{1,6})/$', 'event_edit', name='event-edit'),
    url(r'^event/list/$', 'event_list', name='event-list'),
    url(r'^member/edit/(\d{1,6})/$', 'member_edit', name='member-edit'),
)
