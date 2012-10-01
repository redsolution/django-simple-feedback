# -*- coding: utf-8 -*-

from django import template
from django.forms import BooleanField
from django.utils.translation import ugettext_lazy as _
from django.template import loader
from django.template.context import RequestContext

from feedback.utils import get_feedback_form

register = template.Library()


@register.simple_tag(takes_context=True)
def show_feedback(context, key='default'):
    form = get_feedback_form(key)()
    t = loader.select_template([
        'feedback/%s/feedback.html' % key,
        'feedback/feedback.html',
    ])
    request_context = RequestContext(context['request'], locals())
    output = t.render(request_context)
    return output


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
