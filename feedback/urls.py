# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from feedback.settings import DIRECT_TO_TEMPLATE

if DIRECT_TO_TEMPLATE:
    urlpatterns = patterns('django.views.generic.simple',
        url(r'^$', 'direct_to_template',
            {'template': 'feedback/feedback_page.html'}, name='feedback_page')
    )
else:
    urlpatterns = patterns('')

urlpatterns += patterns('feedback.views',
    url(r'ajax/$', 'show_ajax_response', name='ajax_feedback'),
)
