# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from settings import DEFAULT_FORM_KEY, FEEDBACK_FORMS
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
from django.forms import models
from models import MailingList, forms as form_list
from .settings import FEEDBACK_ANTISPAM


class MailingListForm(models.ModelForm):
    class Meta:
        model = MailingList
    
    def __init__(self, *args, **kwargs):
        super(MailingListForm, self).__init__(*args, **kwargs)
        self.fields['form'].help_text = _('For each feedback form you can specify only one mailing list!')
        self.fields['form'].choices = form_list


class BaseFeedbackForm(forms.Form):

    class Media:
        if hasattr(settings, 'STATIC_URL'):
            js = ((settings.STATIC_URL + 'feedback/js/feedback.js'),)
        else:
            js = ((settings.MEDIA_URL + 'feedback/js/feedback.js'),)

    # Скрытое поле для защиты от спам-ботов
    message_ = forms.CharField(label=u'Сообщение', required=False, widget=forms.Textarea(attrs={'class': 'important-field'}))

    def clean(self):
        if FEEDBACK_ANTISPAM['CHECKING_HIDDEN_FIELD']:
            if len(self.cleaned_data.get('message_', '')):
                self._errors['message_'] = 'unhuman message found'
        if FEEDBACK_ANTISPAM['BLOCKING_EXTERNAL_LINKS']:
            for key, value in self.cleaned_data.iteritems():
                if 'href=' in value:
                    self._errors['message_'] = 'external links found'

        return self.cleaned_data

    subject = _('message_')

    def mail(self, request):
        from models import MailingList

        key = self.get_settings_key()
        try:
            m = MailingList.objects.get(form__exact=key)
            recipients = m.emails.values_list('email', flat=True)
            sender = m.default_from if m.default_from else settings.DEFAULT_FROM_EMAIL
        except:
            recipients = [mail[1] for mail in settings.MANAGERS]
            sender = settings.DEFAULT_FROM_EMAIL
        
        context = self.get_context_data(request)
        message = render_to_string(self.get_email_template_names(), context)
        headers = {}
        if self.cleaned_data.has_key('email'):
            headers = {'Reply-to': self.cleaned_data.get('email')}
        
        msg = EmailMessage(self.subject, message, sender, recipients, headers=headers)    
        msg.send()
        self._errors['end_date'] = self.error_class([msg])

    def get_context_data(self, request):
        context = {'fields': {}}
        for name, field in self.fields.iteritems():
            context['fields'][name] = self.cleaned_data.get(name, None)
        context['form'] = self
        context['request'] = request
        return context

    def get_settings_key(self):
        '''Finds its own class in settings.FEEDBACK_FORMS dictionary
        and returns appropriate key
        '''
        reverse_forms_dict = dict(
            (v.rsplit('.', 1)[1], k) for k, v in FEEDBACK_FORMS.iteritems()
        )
        return reverse_forms_dict.get(self.__class__.__name__, DEFAULT_FORM_KEY)

    def get_email_template_names(self):
        """
        Returns template names for Email rendering.
        """
        templates = ['feedback/feedback_message.txt',]
        # Insert before default template
        templates[0:0] = ['feedback/%s/email.txt' % self.get_settings_key(),]
        return templates
        
class DefaultFeedbackForm(BaseFeedbackForm):
    email = forms.EmailField(label=_('Email'), max_length=200)
    topic = forms.CharField(label=_('Topic'), max_length=200)
    response = forms.CharField(label=_('Message text'), max_length=500,
        widget=forms.Textarea(attrs={'cols':'30', 'rows':'5'}))
    subject = _('Feedback form')
