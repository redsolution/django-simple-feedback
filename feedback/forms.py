# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string


class FeedbackWidget(forms.Textarea):

    class Media:
        js = ((settings.MEDIA_URL + 'feedback/js/feedback.js'),)


class BaseFeedbackForm(forms.Form):
    # TODO:
#    def _get_media(self):
#        media = media + FeedbackWidget.media
#        return media

    def mail(self):
        # prepare context for message
        context = {'fields': {}}
        for name, field in self.fields.iteritems():
            context['fields'][name] = self.cleaned_data.get(name, None)
            # leaved for compatibility. Wil be removed in feedback v 1.2
            context[name] = self.cleaned_data.get(name, None)

        message = render_to_string('feedback/feedback_message.txt', context)

        # generate subject considering settings variable EMAIL_SUBJECT_PREFIX
        subject = settings.EMAIL_SUBJECT_PREFIX + u'feedback'

        # Email backends appears only in Django 1.2
        import django
        if django.VERSION < (1, 2):
            from feedback.utils import email_backend
            email_backend(to, message, subject=self.subject % context)
        else:
            from django.core.mail import mail_managers
            mail_managers(subject, message, fail_silently=False)


class FeedbackForm(BaseFeedbackForm):
    email = forms.EmailField(label=_('Email'), max_length=200)
    topic = forms.CharField(label=_('Topic'), max_length=200)
    response = forms.CharField(label=_('Message text'), max_length=500,
                               widget=FeedbackWidget(attrs={'rows': 5, 'cols': 30}))
    subject = _('Feedback form')
