# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .settings import PREFIX_KEY_FIELDS
from .utils import get_feedback_form


def show_ajax_response(request, key):

    if request.method == 'POST':
        form_cls = get_feedback_form(key)
        form = form_cls(request.POST)

        if PREFIX_KEY_FIELDS:
            form.prefix = key

        if form.is_valid():
            form.mail(request)
            templates = ['feedback/%s/thankyou.html' % key, 'feedback/thankyou.html']
        else:
            if 'message_' in form.errors:
                templates = ['feedback/%s/spam.html' % key, 'feedback/spam.html']
            else:
                templates = ['feedback/%s/feedback.html' % key, 'feedback/feedback.html']
        return render(request, templates, {'form': form})
    else:
        return HttpResponseRedirect('/')
