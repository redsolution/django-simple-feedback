# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from feedback.utils import render_to_string
from django.shortcuts import render_to_response

from forms import FeedbackForm

def show_feedback_form(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.mail()
            return render_to_response('feedback/thankyou.html', {'form': form})
    else:
        form = FeedbackForm()
    return render_to_response('feedback/feedback.html', {'form': form})
