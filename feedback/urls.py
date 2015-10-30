#-*- coding: utf-8 -*-
from django.conf.urls import url, patterns

urlpatterns = patterns('feedback.views',
    url(r'ajax/(?P<key>\w+)/$', 'show_ajax_response', name='ajax_feedback'),
)
