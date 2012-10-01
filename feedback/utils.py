# -*- coding: utf-8 -*-
from django.core.mail import send_mail, EmailMessage
from django.template import loader
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.utils.translation import string_concat

def import_item(path, error_text):
    """Imports a model by given string. In error case raises ImpoprelyConfigured"""
    i = path.rfind('.')
    module, attr = path[:i], path[i + 1:]
    try:
        return getattr(__import__(module, {}, {}, ['']), attr)
    except ImportError, e:
        raise ImproperlyConfigured('Error importing %s %s: "%s"' % (error_text, path, e))

def get_feedback_form(key):
    from feedback.settings import FEEDBACK_FORMS
    if key not in FEEDBACK_FORMS:
        raise ImproperlyConfigured('Form %s not registered in FEEDBACK_FORMS' % key)
    return import_item(FEEDBACK_FORMS[key], 'can not import feedback form')

def mail_admins(subject, message, fail_silently):
    '''Repalcement for standard Django function.
    It uses ``DEFAULT_FROM_EMAIL`` setting instead ``SERVR_FROM_EMAIL``
    '''
    if not settings.ADMINS:
        return
    EmailMessage(string_concat(settings.EMAIL_SUBJECT_PREFIX, subject), message,
                 settings.DEFAULT_FROM_EMAIL, [a[1] for a in settings.ADMINS],
                 connection=connection).send(fail_silently=fail_silently)

def mail_managers(subject, message, attachments = None, fail_silently=False, connection=None, headers=None, exclude_list=[]):
    """Sends a message to the managers, as defined by the ``MANAGERS`` setting and ``exclude_list`` parameter.
    It uses ``DEFAULT_FROM_EMAIL`` setting instead ``SERVR_FROM_EMAIL``
    """
    if not settings.MANAGERS:
        return
    recipients = [a[1] for a in settings.MANAGERS if a[1] not in exclude_list]
    email = EmailMessage(string_concat(settings.EMAIL_SUBJECT_PREFIX, subject), message,
                 settings.DEFAULT_FROM_EMAIL, recipients,
                 connection=connection,
                 headers=headers)
    if attachments != None:
        for file in attachments.values():
            email.attach(file.name, file.read(), file.content_type)
    email.send(fail_silently=fail_silently)
