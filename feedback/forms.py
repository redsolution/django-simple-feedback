# -*- coding: utf-8 -*-
from django import forms
from feedback.utils import email_backend, render_to_string
from django.conf import settings


class FeedbackWidget(forms.Textarea):

    class Media:
        js = ((settings.MEDIA_URL + 'feedback/js/feedback.js'),)


class FeedbackForm(forms.Form):
    email = forms.CharField(label=u'Email', max_length=200)
    topic = forms.CharField(label=u'Тема', max_length=200)
    response = forms.CharField(label=u'Текст сообщения', max_length=500,
                               widget=FeedbackWidget(attrs={'rows': 5, 'cols': 30}))

    def mail(self):
        response = self.cleaned_data.get('response', None)
        topic = self.cleaned_data.get('topic', None)
        email = self.cleaned_data.get('email', None)

        to = [email_tuple[1] for email_tuple in settings.MANAGERS]

        message = render_to_string('feedback/feedback_message.txt', {'email': email, 'topic': topic, 'response': response})

        email_backend(to, message, subject=u'Обратная связь: %s' % topic)

