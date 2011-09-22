from django.conf import settings

DEFAULT_FORM = 'feedback.forms.FeedbackForm'

FEEDBACK_FORM = getattr(settings, 'FEEDBACK_FORM', DEFAULT_FORM)

DIRECT_TO_TEMPLATE = getattr(settings, 'DIRECT_TO_TEMPLATE', True)

# new in 0.1.1
FEEDBACK_FORMS = getattr(settings, 'FEEDBACK_FORMS', {
    'default': FEEDBACK_FORM,
})

FEEDBACK_ATTACHMENT_SIZE = getattr(settings, 'FEEDBACK_ATTACHMENT_SIZE', 2)
