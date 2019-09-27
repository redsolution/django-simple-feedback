# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.mail.message import EmailMessage
from django.forms import models, ChoiceField
from django.template import engines

from .settings import DEFAULT_FORM_KEY, FEEDBACK_FORMS, FEEDBACK_FORMS_NAMES
from .models import MailingList
from .settings import FEEDBACK_ANTISPAM, ADMIN_EXTRA_CLASS
from .utils import get_mailing_list

django_engine = engines['django']


def get_extra_class(field_name):
    return ADMIN_EXTRA_CLASS.get(field_name, ADMIN_EXTRA_CLASS.get('all', ''))


def make_form_choices():

    ''' Creating choices, based on FEEDBACK_FORMS for mailing list admin form '''

    result = []
    for key in FEEDBACK_FORMS.keys():
        form_name = ' '.join(key.split('_')).capitalize()
        if key in FEEDBACK_FORMS_NAMES:
            form_name = FEEDBACK_FORMS_NAMES[key]
        result.append((key, form_name))
    return result


class MailingListAdminForm(models.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MailingListAdminForm, self).__init__(*args, **kwargs)
        self.fields['form'].help_text = _('For each feedback form you can specify only one mailing list!')

    form = ChoiceField(
        label=_('form'), choices=make_form_choices(),
        widget=forms.Select(attrs={'class':  get_extra_class('form')})
    )

    class Meta:
        model = MailingList
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': get_extra_class('title')}),
            'default_from': forms.TextInput(attrs={'class': get_extra_class('default_from')}),
            'form_title': forms.TextInput(attrs={'class': get_extra_class('form_title')}),
            'message_subject': forms.TextInput(attrs={'class': get_extra_class('message_subject')}),
            'message_template': forms.Textarea(attrs={'class': get_extra_class('message_template')}),
        }


class BaseFeedbackForm(forms.Form):
    class Media:
        if hasattr(settings, 'STATIC_URL'):
            js = ((settings.STATIC_URL + 'feedback/js/feedback.js'),)
        else:
            js = ((settings.MEDIA_URL + 'feedback/js/feedback.js'),)

    # Скрытое поле для защиты от спам-ботов
    message_ = forms.CharField(
        label=u'Сообщение', required=False,
        widget=forms.Textarea(attrs={'style': 'display: none;'})
    )

    def get_settings_key(self):

        ''' Finds its own class in settings.FEEDBACK_FORMS dictionary and returns appropriate key '''

        reverse_forms_dict = dict(
            (v.rsplit('.', 1)[1], k) for k, v in FEEDBACK_FORMS.iteritems()
        )
        return reverse_forms_dict.get(self.__class__.__name__, DEFAULT_FORM_KEY)

    def __init__(self, *args, **kwargs):
        super(BaseFeedbackForm, self).__init__(*args, **kwargs)

        self.key = self.get_settings_key()
        self.mailing_list = get_mailing_list(self.key)
        self.sender = settings.DEFAULT_FROM_EMAIL
        self.recipients = [mail[1] for mail in settings.MANAGERS]
        self.subject = settings.EMAIL_SUBJECT_PREFIX

        if self.mailing_list:
            self.title = self.mailing_list.form_title
            self.thankyou = self.mailing_list.form_thankyou

            if self.mailing_list.message_subject:
                self.subject = self.mailing_list.message_subject

            recipiends = self.mailing_list.emails.values_list('email', flat=True)
            if recipiends:
                self.recipients = recipiends

            if self.mailing_list.default_from:
                self.sender = self.mailing_list.default_from

    DEFAULT_EMPTY_VALUE = '-'

    def clean(self):

        """ Check spam in fields """

        if FEEDBACK_ANTISPAM['CHECKING_HIDDEN_FIELD']:
            if len(self.cleaned_data.get('message_', '')):
                self._errors['message_'] = 'unhuman message found'
        if FEEDBACK_ANTISPAM['BLOCKING_EXTERNAL_LINKS']:
            for key, value in self.cleaned_data.iteritems():
                if isinstance(value, unicode) and 'href=' in value:
                    self._errors['message_'] = 'external links found'

        return self.cleaned_data

    def get_field_value(self, field):

        """ Get correct field value for different fields types """

        value = self.DEFAULT_EMPTY_VALUE
        if hasattr(field.form.fields[field.name], 'choices'):
            for choice in field.form.fields[field.name].choices:
                if field.data:
                    if unicode(choice[0]) == unicode(field.data):
                        value = choice[1]
                        break
        elif type(field.form.fields[field.name]) is forms.BooleanField:
            if field.data is not None:
                value = _('Yes') if field.data else _('No')
        elif field.data:
            value = field.data
        return value

    def extra_message_context(self, request):

        """ Override this for extra message context """

        return {}

    def render_message(self, request):
        message_template = self.mailing_list.message_template if self.mailing_list else ''
        context = {
            'referer': request.META['HTTP_REFERER'],
            'subject': self.subject
        }
        context.update(self.extra_message_context(request))
        for field in self:
            context[field.name] = self.get_field_value(field)

        template = django_engine.from_string(message_template)
        return template.render(context, request)

    def after_mail(self, **kwargs):

        """ Override this for additial logic """

        pass

    def mail(self, request):

        message = self.render_message(request)
        headers = {}
        if self.cleaned_data.has_key('email'):
            headers = {'Reply-to': self.cleaned_data.get('email')}

        msg = EmailMessage(self.subject, message, self.sender, self.recipients, headers=headers)
        msg.send()
        self.after_mail(message=message, headers=headers)


class DefaultFeedbackForm(BaseFeedbackForm):
    email = forms.EmailField(label=_('Email'), max_length=200)
    topic = forms.CharField(label=_('Topic'), max_length=200)
    response = forms.CharField(
        label=_('Message text'), max_length=500,
        widget=forms.Textarea(attrs={'cols': '30', 'rows': '5'})
    )
