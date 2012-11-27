#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from settings import DEFAULT_FORM_KEY
from utils import get_feedback_form

def show_ajax_response(request):
    if request.method == 'POST':
        key = request.POST.get('form_settings_key', DEFAULT_FORM_KEY)
        FormClass = get_feedback_form(key)
        form = FormClass(request.POST)
        if form.is_valid():
            form.mail(request)
            return render_to_response([
                'feedback/%s/thankyou.html' % key,
                'feedback/thankyou.html',
                ], {'form': form}, context_instance=RequestContext(request))
        else:
            return render_to_response([
                'feedback/%s/feedback.html' % key,
                'feedback/feedback.html',
                ], {'form': form}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')
