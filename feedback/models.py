#-*- coding: utf-8 -*-

import simplejson as json

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

class ResponseAttachments(models.Model):
    """Model contains attachments for feedback responses"""
    
    file = models.FileField(upload_to='upload/feedback/')
    response = models.ForeignKey('Response')
    
    class Meta:
        verbose_name = _('response attachment')
        verbose_name_plural = _('response attachments')

class Response(models.Model):
    """Model contains responses sent by users"""
    
    send_time = models.DateTimeField(auto_now_add=True,verbose_name=_('Sending time'))
    response = models.TextField(verbose_name=_('Content response'))
    
    def set_response(self, serialize_form):
        setattr(self, 'response', 
                json.dumps(serialize_form.get_dictionary()))
        
    def get_response(self):
        return json.loads(getattr(self, 'response'))
    
    def __unicode__(self):
        sended = self.send_time.strftime('%d.%m.%Y %H:%M')
        return 'Response for %(sended)s' % {'sended': sended}
    
    class Meta:
        verbose_name = _('response')
        verbose_name_plural = _('responses')
    
# probably it isn't a model, but in __init__.py this code breaks setup.py

class BogusSMTPConnection(object):
    """Instead of sending emails, print them to the console."""

    def __init__(self, *args, **kwargs):
        print "Initialized bogus SMTP connection"

    def open(self):
        print "Open bogus SMTP connection"

    def close(self):
        print "Clone bogus SMTP connection"

    def send_messages(self, messages):
        print "Sending through bogus SMTP connection:"
        for message in messages:
            print "From: %s" % message.from_email
            print "To: %s" % (", ".join(message.to))
            print "Subject: %s\n\n" % unicode(message.subject)
            print "%s" % message.body
            print messages
            print "Attachments:"
            for attachment in message.attachments:
                for field in attachment: 
                    print field
                print "----" 
        return len(messages)


if settings.DEBUG:
    from django.core import mail
    mail.SMTPConnection = BogusSMTPConnection


