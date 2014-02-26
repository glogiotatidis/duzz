from django.conf.urls import patterns, include, url
from django.contrib import admin

import jingo.monkey

import duzz.base.views

admin.autodiscover()
jingo.monkey.patch()


urlpatterns = patterns(
    '',
    url(r'^$', duzz.base.views.home, name='home'),
    url(r'^profile/$', duzz.base.views.ProfileUpdate.as_view(), name='profile'),
    url(r'^topic/$', duzz.base.views.Topics.as_view(), name='topics'),
    url(r'^topic/add/$',
        duzz.base.views.CommentCreate.as_view(), name='topic_add'),
    url(r'^topic/(?P<topic_id>\d+)/$',
        duzz.base.views.Comments.as_view(), name='comments'),
    url(r'^topic/(?P<topic_id>\d+)/add/$',
        duzz.base.views.CommentCreate.as_view(), name='comment_add'),

    (r'^browserid/', include('django_browserid.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
