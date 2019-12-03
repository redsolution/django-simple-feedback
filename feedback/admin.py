# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.utils.translation import ugettext_lazy as _
from .models import MailingList, FeedbackEmail
from .forms import MailingListAdminForm
from .settings import ADMIN_EXTRA_CSS


@admin.register(FeedbackEmail)
class FeedbackEmailAdmin(ModelAdmin):
    model = FeedbackEmail


@admin.register(MailingList)
class MailingListAdmin(ModelAdmin):

    @property
    def media(self):
        media = super(MailingListAdmin, self).media
        media.add_css(ADMIN_EXTRA_CSS)
        return media

    form = MailingListAdminForm
    filter_horizontal = ['emails']
    fieldsets = (
        (None, {'fields': ('title', 'emails', 'default_from')}),
        (_('form'), {'fields': ('form_title', 'form', 'form_thankyou')}),
        (_('email message'), {'fields': ('message_subject', 'message_template',)}),
    )