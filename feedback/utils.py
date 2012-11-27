#-*- coding: utf-8 -*-
from django.core.exceptions import ImproperlyConfigured
from models import MailingList
from settings import DEFAULT_FORM_KEY

def import_item(path, error_text):
    """Imports a model by given string. In error case raises ImpoprelyConfigured"""
    i = path.rfind('.')
    module, attr = path[:i], path[i + 1:]
    try:
        return getattr(__import__(module, {}, {}, ['']), attr)
    except ImportError, e:
        raise ImproperlyConfigured('Error importing %s %s: "%s"' % (error_text, path, e))

def get_feedback_form(key):
    from settings import FEEDBACK_FORMS
    if key not in FEEDBACK_FORMS:
        raise ImproperlyConfigured('Form %s not registered in FEEDBACK_FORMS' % key)
    return import_item(FEEDBACK_FORMS[key], 'can not import feedback form')

def get_mailing_list(key):
    from settings import FEEDBACK_FORMS
    if key not in FEEDBACK_FORMS:
        raise ImproperlyConfigured('Form %s not registered in FEEDBACK_FORMS' % key)

    try:
        m = MailingList.objects.get(form__exact=key)
    except:
        try:
            m = MailingList.objects.get(form__exact=DEFAULT_FORM_KEY)
        except:
            return None
        
    return m
