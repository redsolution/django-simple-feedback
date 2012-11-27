#-*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from models import MailingList, FeedbackEmail
from forms import MailingListForm

class FeedbackEmailAdmin(ModelAdmin):
    model = FeedbackEmail

class MailingListAdmin(ModelAdmin):
    form = MailingListForm
    filter_horizontal = ('emails',)

    
admin.site.register(MailingList, MailingListAdmin)
admin.site.register(FeedbackEmail, FeedbackEmailAdmin)
