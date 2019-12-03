# -*- coding: utf-8 -*-

from classytags.arguments import Argument
from classytags.core import Tag, Options
from django import template
from django.template.loader import render_to_string
from feedback.utils import get_feedback_form
from feedback.settings import DEFAULT_FORM_KEY, PREFIX_KEY_FIELDS

register = template.Library()


@register.tag
class ShowFeedback(Tag):

    name = 'show_feedback'
    options = Options(Argument('form_key', required=False, resolve=False))

    def render_tag(self, context, form_key):
        form_key = form_key or DEFAULT_FORM_KEY
        form = get_feedback_form(form_key)()
        if PREFIX_KEY_FIELDS:
            form.prefix = form_key
        templates = ['feedback/%s/feedback.html' % form_key, 'feedback/feedback.html']
        return render_to_string(templates, {'form': form}, context['request'])


@register.tag
class ShowField(Tag):

    """ Отображение поля с проверкой на принадлежность к набору формы """

    name = 'show_field'
    options = Options(
        Argument('field'),
        'set',
        Argument('form_set', required=False, resolve=False, default=False)
    )

    def render_tag(self, context, **kwargs):
        field = kwargs.get('field')
        form_set = kwargs.get('form_set')
        attrs = field.field.widget.attrs
        field_set = str(attrs.get('data-set', 0))
        extra_context = {
            'attrs': attrs,
            'field': field,
            'input_type': getattr(field.field.widget, 'input_type', 'textarea')
        }
        if form_set and form_set != field_set:
            return ''
        return render_to_string('feedback/field.html', extra_context, context['request'])
