# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from redsolutioncms.models import CMSSettings, BaseSettings, BaseSettingsManager


FIELD_TYPES = (
    ('BooleanField', _('Checkbox')),
    ('CharField', _('Character field')),
    ('Text', _('Text area')),
    ('EmailField', _('Email field')),
)

class FeedbackSettingsManager(BaseSettingsManager):
    def get_settings(self):
        if self.get_query_set().count():
            return self.get_query_set()[0]
        else:
            feedback_settings = self.get_query_set().create()
#            cms_settings = CMSSettings.objects.get_settings()

            return feedback_settings


class FeedbackSettings(BaseSettings):
#    use_direct_view = models.BooleanField(
#        verbose_name=_('Use dedicated view to render feedback page'),
#        default=True
#    )
    # Temporary hadrcoded
    use_direct_view = True
    use_custom_form = models.BooleanField(verbose_name=_('Use custom feedback form'),
        default=False)

    objects = FeedbackSettingsManager()


class FormField(models.Model):
    feedback_settings = models.ForeignKey('FeedbackSettings')
    field_type = models.CharField(verbose_name=_('Type of field'),
        choices=FIELD_TYPES, max_length=255)
    field_name = models.CharField(verbose_name=_('Verbose name of field'),
        max_length=255)
