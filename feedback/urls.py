# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('feedback.views',
    url(r'^$', 'show_feedback_form', name='feedback'),
)
