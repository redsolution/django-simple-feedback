from django import template
from feedback.utils import get_feedback_form

register = template.Library()


@register.inclusion_tag('feedback/feedback.html', takes_context=False)
def show_feedback():
    form = get_feedback_form()()
    return locals()
