# -*- coding: utf-8 -*-
from django import forms
from feedback.utils import email_backend
from django.conf import settings
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
        context = {}
        to = [email_tuple[1] for email_tuple in settings.MANAGERS]
        for name, field in self.fields.iteritems():
            context[name] = self.cleaned_data.get(name, None)
        message = render_to_string('feedback/feedback_message.txt', context)
        email_backend(to, message, subject=self.subject % context)


class FeedbackForm(BaseFeedbackForm):
    email = forms.CharField(label=u'Email', max_length=200)
    topic = forms.CharField(label=u'Тема', max_length=200)
    response = forms.CharField(label=u'Текст сообщения', max_length=500,
                               widget=FeedbackWidget(attrs={'rows': 5, 'cols': 30}))
