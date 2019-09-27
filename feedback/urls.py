# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import show_ajax_response


urlpatterns = [
    url(r'ajax/(?P<key>\w+)/$', show_ajax_response, name='ajax_feedback'),
]
