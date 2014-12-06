from django.conf.urls import patterns, url

urlpatterns = patterns('events.views',
    url(r'^event/list/$', 'event_list', name='event-list'),
    url(r'^event/edit/(\d{1,6})/$', 'event_edit', name='event-edit'),
    url(r'^event/add/(\d{1,6})/$', 'event_add', name='event-add'),

    url(r'^member/list/$', 'member_list', name='member-list'),
    url(r'^member/edit/(\d{1,6})/$', 'member_edit', name='member-edit'),
    url(r'^member/download-backup$', 'download_backup', name='download-backup'),

    url(r'^email/yes/(.+?)/$', 'email_yes', name='email-yes'),
    url(r'^email/no/(.+?)/$', 'email_no', name='email-no'),
)
