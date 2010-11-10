from django.contrib import admin
from feedback.redsolution_setup.models import FeedbackSettings, FormField
from redsolutioncms.admin import CMSBaseAdmin


class FormFieldInline(admin.TabularInline):
    model = FormField

class FeedbackSettingsAdmin(CMSBaseAdmin):
    model = FeedbackSettings
    inlines = [FormFieldInline,]
