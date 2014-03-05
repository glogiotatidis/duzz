from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

import jingo.monkey

import duzz.base.views

admin.autodiscover()
jingo.monkey.patch()


urlpatterns = patterns(
    '',
    url(r'^$', duzz.base.views.home, name='root'),
    url(r'^profile/$', duzz.base.views.ProfileUpdate.as_view(), name='profile'),
    url(r'^topics/$', duzz.base.views.Topics.as_view(), name='topics'),
    url(r'^topic/add/$',
        duzz.base.views.TopicCreate.as_view(), name='topic_add'),
    url(r'^topic/(?P<topic_id>\d+)/$',
        duzz.base.views.Comments.as_view(), name='topic'),

    url(r'^browserid/', include('django_browserid.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^foundation/', include('foundation.urls')),
)


if settings.DEBUG:
    urlpatterns = (urlpatterns + 
                   static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
