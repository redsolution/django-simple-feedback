#-*- coding: utf-8 -*-
from classytags.arguments import Argument
from classytags.core import Tag, Options
from django import template
from django.template.loader import render_to_string
from django.template.context import RequestContext
from django.utils.translation import gettext_lazy as _
from feedback.utils import get_feedback_form
from feedback.settings import DEFAULT_FORM_KEY
from django.forms.fields import BooleanField


register = template.Library()


class ShowFeedback(Tag):
    name = 'show_feedback'
    
    options = Options(Argument('form_key', required=False, resolve=False))
    
    def render_tag(self, context, form_key):
        form_key = form_key if form_key else DEFAULT_FORM_KEY
        form = get_feedback_form(form_key)()
        
        return render_to_string([
            'feedback/%s/feedback.html' % form_key,
            'feedback/feedback.html',
            ], {'form':form}, context_instance=RequestContext(context['request']))

register.tag(ShowFeedback)


@register.filter
def get_choice_value(bound_field):
    '''Returns verbose name of choice value'''
    value = None

    if hasattr(bound_field.form.fields[bound_field.name], 'choices'):
        for choice in bound_field.form.fields[bound_field.name].choices:
            if bound_field.data:
                if choice[0] == int(bound_field.data):
                    value = choice[1]
                    break;
            else:
                value = _('None')
    if value is None:
        if type(bound_field.form.fields[bound_field.name]) is BooleanField:
            if bound_field.data is None:
                return _('None')
            elif bound_field.data:
                return _('Yes')
            else:
                return _('No')
        else:
            return bound_field.data
    else:
        return value
