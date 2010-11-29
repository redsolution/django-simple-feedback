# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string, TemplateDoesNotExist
from feedback.settings import FEEDBACK_FORMS


class BaseFeedbackForm(forms.Form):

    class Media:
        js = ((settings.MEDIA_URL + 'feedback/js/feedback.js'),)

    def __init__(self, *args, **kwds):
        '''Overriden: Creates additional form key hidden field'''
        super(BaseFeedbackForm, self).__init__(*args, **kwds)
        self.fields['form_settings_key'] = forms.CharField(
            label=_('Form type'),
            widget=forms.HiddenInput(),
            max_length=100,
            initial=self.get_settings_key,
        )

    def mail(self):
        # prepare context for message
        context = {'fields': {}}
        for name, field in self.fields.iteritems():
            context['fields'][name] = self.cleaned_data.get(name, None)
            # leaved for compatibility. Wil be removed in feedback v 1.2
            context[name] = self.cleaned_data.get(name, None)
        context['form'] = self
        message = render_to_string(self.get_template(), context)

        # generate subject considering settings variable EMAIL_SUBJECT_PREFIX
        subject = settings.EMAIL_SUBJECT_PREFIX + u'feedback'

        # Email backends appears only in Django 1.2
        import django
        if django.VERSION < (1, 2):
            from feedback.utils import email_backend
            if not settings.MANAGERS:
                return
            email_backend([a[1] for a in settings.MANAGERS],
                message, subject=self.subject % context)
        else:
            from django.core.mail import mail_managers
            mail_managers(subject, message, fail_silently=False)

    def get_settings_key(self):
        '''Finds self class in settings.FEEDBACK_FORMS dictionary
        and returns appropriate key
        '''
        reverse_forms_dict = dict(
            (v.rsplit('.', 1)[1], k) for k, v in FEEDBACK_FORMS.iteritems()
        )
        return reverse_forms_dict.get(self.__class__.__name__, 'default')

    def get_template_name(self):
        '''returns template for rendering email message
        Returns string in format 'feedback/<settings_key>.txt'
        So, if form registered in FEEDBACK_FORMS with key 'myform',
        it will be rendered to feedback/myform.txt
        '''
        if hasattr(self, 'template'):
            return self.template
        else:
            reverse_forms_dict = dict(
                (v.rsplit('.', 1)[1], k) for k, v in FEEDBACK_FORMS.iteritems()
            )
            form_settings_key = self.get_settings_key()
            return 'feedback/' + form_settings_key + '.txt'

    def get_template(self):
        '''If template, returned by ``get_template_name`` exists,
        returns ``get_template_name`` result. Otherwise returns default
        template name used in older versions ``feedback/feedback_message.txt``
        '''
        import django
        template_name = self.get_template_name()
        try:
            if django.VERSION < (1, 2):
                from django.template.loader import find_template_source
                find_template_source(template_name)
            else:
                from django.template.loader import find_template
                find_template(template_name)
            return template_name
        except TemplateDoesNotExist:
            return 'feedback/feedback_message.txt'


class FeedbackForm(BaseFeedbackForm):
    email = forms.EmailField(label=_('Email'), max_length=200)
    topic = forms.CharField(label=_('Topic'), max_length=200)
    response = forms.CharField(label=_('Message text'), max_length=500,
        widget=forms.Textarea(attrs={'cols':'30', 'rows':'5'}))
    subject = _('Feedback form')
