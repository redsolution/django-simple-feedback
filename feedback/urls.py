# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from feedback import settings

if settings.DIRECT_TO_TEMPLATE:
    urlpatterns = patterns('django.views.generic.simple',
        url(r'^', 'direct_to_template', {'template': ''}, name='feedback_main')
    )
else:
    urlpatterns = patterns('')

urlpatterns += patterns('feedback.views',
    url(r'^ajax$', 'show_feedback_form', name='ajax_feedback'),
)
