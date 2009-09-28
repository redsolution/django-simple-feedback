from django.conf import settings

DEFAULT_FORM = 'feedback.forms.FeedbackForm'

FEEDBACK_FORM = getattr(settings, 'FEEDBACK_FORM', DEFAULT_FORM)