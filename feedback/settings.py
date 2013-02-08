# -*- coding: utf-8 -*-
from django.conf import settings

DEFAULT_FORM = 'feedback.forms.FeedbackForm'

DEFAULT_FORM_KEY = getattr(settings, 'DEFAULT_FORM_KEY', 'default')

FEEDBACK_FORM = getattr(settings, 'FEEDBACK_FORM', DEFAULT_FORM)

DIRECT_TO_TEMPLATE = getattr(settings, 'DIRECT_TO_TEMPLATE', True)

FEEDBACK_FORMS = getattr(settings, 'FEEDBACK_FORMS', {
    DEFAULT_FORM_KEY: FEEDBACK_FORM,
})

FEEDBACK_ATTACHMENT_SIZE = getattr(settings, 'FEEDBACK_ATTACHMENT_SIZE', 2)

FEEDBACK_RECIPIENTS_EXCLUDED = getattr(settings, 'FEEDBACK_RECIPIENTS_EXCLUDED', {})