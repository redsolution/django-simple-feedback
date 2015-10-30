from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class FeedbackAppConfig(AppConfig):
    name = 'feedback'
    verbose_name = _('Feedback')

    class Meta:
        app_label = 'feedback'