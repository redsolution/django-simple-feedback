# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
try:
    from tinymce.models import HTMLField
except ImportError:
    from django.db.models.fields import TextField as HTMLField


class FeedbackEmail(models.Model):
    class Meta:
        verbose_name = _('Email address')
        verbose_name_plural = _('Email addresses')

    name = models.CharField(
        verbose_name=_('Receiver\'s name'),
        max_length=200, blank=True, null=True
    )
    email = models.EmailField(
        verbose_name=_('Email'), max_length=200
    )

    def __unicode__(self):
        return '%s: %s' % (self.name, self.email,) if self.name else self.email


class MailingList(models.Model):
    class Meta:
        verbose_name = _('Mailing list')
        verbose_name_plural = _('Mailing lists')

    title = models.CharField(
        verbose_name=_('List title'),
        max_length=200, null=True
    )

    emails = models.ManyToManyField(
        FeedbackEmail,
        verbose_name=_('List of addresses'),
        related_name='forms', blank=True
    )

    default_from = models.EmailField(
        verbose_name=_('Default sender email'),
        max_length=200, blank=True, null=True
    )

    form = models.CharField(
        verbose_name=_('form'),
        max_length=100, unique=True
    )

    form_title = models.CharField(
        verbose_name=_('form title'),
        max_length=255, default='', blank=True
    )

    form_thankyou = HTMLField(verbose_name=_('Success message'), default='', blank=True)

    message_subject = models.CharField(
        verbose_name=_('Message subject'),
        max_length=255, default='', blank=True
    )

    message_template = models.TextField(
        verbose_name=_('Message template'),
        default='', blank=True
    )

    def __unicode__(self):
        return self.title 
