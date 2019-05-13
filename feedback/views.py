#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from settings import PREFIX_KEY_FIELDS
from utils import get_feedback_form

def show_ajax_response(request, key):
    if request.method == 'POST':
        FormClass = get_feedback_form(key)
        form = FormClass(request.POST)

        if PREFIX_KEY_FIELDS:
            form.prefix = key

        if form.is_valid():
            form.mail(request)
            return render_to_response([
                'feedback/%s/thankyou.html' % key,
                'feedback/thankyou.html',
                ], {'form': form}, context_instance=RequestContext(request))
        else:
            if 'message_' in form.errors:
                return render_to_response([
                    'feedback/%s/spam.html' % key,
                    'feedback/spam.html',
                ], {'form': form}, context_instance=RequestContext(request))
            return render_to_response([
                'feedback/%s/feedback.html' % key,
                'feedback/feedback.html',
                ], {'form': form}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')
