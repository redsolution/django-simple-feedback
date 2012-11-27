#-*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from settings import FEEDBACK_FORMS

forms = [(key, ' '.join(key.split('_')).capitalize()) for key in FEEDBACK_FORMS.keys()]


class FeedbackEmail(models.Model):
    class Meta:
        verbose_name = _('Email address')
        verbose_name_plural = _('Email addresses')
    
    name = models.CharField(verbose_name=_('Receiver\'s name'),max_length=200,blank=True,null=True)
    email = models.EmailField(verbose_name=_('Email'), max_length=200)
    
    
    def __unicode__(self):
        return '%s:%s' % (self.name,self.email,) if self.name else self.email

class MailingList(models.Model):
    class Meta:
        verbose_name = _('Mailing list')
        verbose_name_plural = _('Mailing lists')
    
    title = models.CharField(verbose_name=_('List title'),max_length=200,null=True)
    emails = models.ManyToManyField(FeedbackEmail, verbose_name=_('List of addresses'), 
        related_name='forms',blank=True)
    form = models.CharField(verbose_name=_('Feedback form'),max_length=100,unique=True,choices=forms)
    default_from = models.EmailField(verbose_name=_('Default sender email'),max_length=200,blank=True,null=True)
    
    def __unicode__(self):
        return self.title 
