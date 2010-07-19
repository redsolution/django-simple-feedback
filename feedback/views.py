# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from feedback.utils import get_feedback_form


def show_feedback_form(request):
    if request.method == 'POST':
        form = get_feedback_form()(request.POST)
        if form.is_valid():
            form.mail()
            return render_to_response('feedback/thankyou.html', {'form': form})
    else:
        form = get_feedback_form()()
    return render_to_response('feedback/feedback.html', {'form': form})
