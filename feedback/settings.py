from django.conf import settings

DEFAULT_FORM = 'feedback.forms.FeedbackForm'

FEEDBACK_FORM = getattr(settings, 'FEEDBACK_FORM', DEFAULT_FORM)

DIRECT_TO_TEMPLATE = getattr(settings, 'DIRECT_TO_TEMPLATE', True)
