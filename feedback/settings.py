#-*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

DEFAULT_FORM_KEY = 'default'
DEFAULT_FORM = 'feedback.forms.DefaultFeedbackForm'

FEEDBACK_FORMS = getattr(settings, 'FEEDBACK_FORMS', {})

FEEDBACK_FORMS_NAMES = getattr(settings, 'FEEDBACK_FORMS_NAMES', {})

if not isinstance(FEEDBACK_FORMS, dict):
    raise ImproperlyConfigured(u'FEEDBACK_FORMS property must be a dictionary')

if DEFAULT_FORM_KEY not in FEEDBACK_FORMS.keys():
    FEEDBACK_FORMS[DEFAULT_FORM_KEY] = DEFAULT_FORM

PREFIX_KEY_FIELDS = getattr(settings, 'FEEDBACK_PREFIX_KEY_FIELDS', False)

ANTISPAM = {
    'CHECKING_HIDDEN_FIELD': True,
    'BLOCKING_EXTERNAL_LINKS': True
}

FEEDBACK_ANTISPAM = getattr(settings, 'FEEDBACK_ANTISPAM', ANTISPAM)
ADMIN_EXTRA_CLASS = getattr(settings, 'FEEDBACK_ADMIN_EXTRA_CLASS', {'all': ''})
ADMIN_EXTRA_CSS = getattr(settings, 'FEEDBACK_ADMIN_EXTRA_CSS', {'all': ['']})
