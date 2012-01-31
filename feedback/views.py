# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from feedback.utils import get_feedback_form
from feedback.models import Response, ResponseAttachments

def dump_data_to_database(request, form):
    response = Response()
    response.set_response(form)
    response.save()
    
    for attachment in request.FILES.values():
        response_attach = ResponseAttachments(response=response)
        response_attach.file.save(attachment.name, attachment)
        response_attach.save()

def show_ajax_response(request, key='default'):
    if request.method == 'POST':
        key = request.POST.get('form_settings_key', key)
        FormClass = get_feedback_form(key)
        form = FormClass(request.POST, request.FILES)
        if form.is_valid():
            form.mail(request)
            dump_data_to_database(request, form)
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
