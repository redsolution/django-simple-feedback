# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from feedback.redsolution_setup.admin import FeedbackSettingsAdmin
admin_instance = FeedbackSettingsAdmin()

urlpatterns = patterns('',
    url(r'^$', admin_instance.change_view, name='feedback_index'),
)