from django import template
from feedback.forms import FeedbackForm

register = template.Library()


@register.inclusion_tag('feedback/feedback.html', takes_context=False)
def show_feedback():
    form = FeedbackForm()
    return locals()
