from django.conf.urls import patterns, url

urlpatterns = patterns('events.views',
    url(r'^event/list/$', 'event_list', name='event-list'),
    url(r'^event/edit/(\d{1,6})/$', 'event_edit', name='event-edit'),
    url(r'^event/add/(\d{1,6})/$', 'event_add', name='event-add'),
    url(r'^event/attendance/(\d{1,6})/$', 'event_attendance', name='event-attendance'),
    url(r'^event/send-invites/(\d{1,6})/$', 'event_send_invites', name='event-send-invites'),
    url(r'^event/disable/(\d{1,6})/$', 'event_disable', name='event-disable'),
    url(r'^event/delete/(\d{1,6})/$', 'event_delete', name='event-delete'),

    url(r'^dashboard/$', 'event_dashboard', name='event-dashboard'),

    url(r'^member/list/$', 'member_list', name='member-list'),
    url(r'^member/edit/(\d{1,6})/$', 'member_edit', name='member-edit'),
    url(r'^member/delete/(\d{1,6})/$', 'member_delete', name='member-delete'),
    url(r'^member/download-backup$', 'download_backup', name='download-backup'),

    url(r'^email/yes/(.+?)/$', 'email_yes', name='email-yes'),
    url(r'^email/no/(.+?)/$', 'email_no', name='email-no'),
)
