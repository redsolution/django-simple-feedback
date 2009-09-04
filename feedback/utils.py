# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader


def email_backend(recipient_list, message, subject='Feedback'):
    subject = settings.EMAIL_SUBJECT_PREFIX + subject
    if type(recipient_list) is not list:
        recipient_list = [recipient_list, ]

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
              recipient_list, fail_silently=False)

def render_to_string(*args, **kwargs):
    return loader.render_to_string(*args, **kwargs)
