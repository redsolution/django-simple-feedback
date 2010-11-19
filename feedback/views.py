# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from feedback.utils import get_feedback_form


def show_ajax_response(request, key='default'):
    if request.method == 'POST':
        FormClass = get_feedback_form(request.POST.get('form_settings_key', key))
        form = FormClass(request.POST)
        if form.is_valid():
            form.mail()
            return render_to_response('feedback/thankyou.html', {'form': form},
                context_instance=RequestContext(request))
        else:
            return render_to_response('feedback/feedback.html', {'form': form},
                context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')
