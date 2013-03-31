from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
       url(r'^$', 'blog.views.home', name='index'),
       url(r'^archive/$', 'blog.views.archive', name='archive'),
       url(r'^archive/(\d{4})/$', 'blog.views.archive', name='archive_year'),
       url(r'^archive/(\d{4})/(\d{2})$', 'blog.views.archive', name='archive_month'),
       url(r'^archive/(\d{4})/(\d{2})/(\d{2})$', 'blog.views.archive', name='archive_day'),
       url(r'^admin/entry/(.*)$', 'blog.views.edit_entry', name='edit_entry'),
       url(r'^admin/entry/$', 'blog.views.edit_entry', name='edit_entry'),
       url(r'^entry/(.*)/$', 'blog.views.display_entry', name='display_entry'),
       url(r'^feed.atom/$', 'blog.views.atom', name='atom_feed'),
)
