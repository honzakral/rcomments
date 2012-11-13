from django.conf.urls.defaults import patterns, url

from rcomments.views import comment_list

urlpatterns = patterns('',
    url(r'^(?P<ct_id>\d+)/(?P<object_pk>.+)/$', comment_list, name='comment-list'),
)
