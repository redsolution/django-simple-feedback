# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from feedback.utils import get_feedback_form
from feedback.models import Response
from django.core import serializers


def show_ajax_response(request, key='default'):
    if request.method == 'POST':
        FormClass = get_feedback_form(request.POST.get('form_settings_key', key))
        form = FormClass(request.POST, request.FILES)
        report = Response()
        if form.is_valid():
            form.mail(request)
            
            report.set_response(form)
            report.save()

            return render_to_response('feedback/thankyou.html', {'form': form},
                context_instance=RequestContext(request))
        else:
            return render_to_response('feedback/feedback.html', {'form': form},
                context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')
