# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string, TemplateDoesNotExist
from feedback.settings import FEEDBACK_FORMS
from feedback.utils import mail_managers
from feedback.settings import FEEDBACK_ATTACHMENT_SIZE

class BaseFeedbackForm(forms.Form):

    class Media:
        if hasattr(settings, 'STATIC_URL'):
            js = ((settings.STATIC_URL + 'feedback/js/feedback.js'),)
        else:
            js = ((settings.MEDIA_URL + 'feedback/js/feedback.js'),)


    subject = _('feedback')
    
    serialized_fields = ()
    
    def __init__(self, *args, **kwds):
        '''Overriden: Creates additional form key hidden field'''
        super(BaseFeedbackForm, self).__init__(*args, **kwds)
        self.fields['form_settings_key'] = forms.CharField(
            label=_('Form type'),
            widget=forms.HiddenInput(),
            max_length=100,
            initial=self.get_settings_key,
        )

    def mail(self, request):
        # prepare context for message
        context = self.get_context_data(request)
        message = render_to_string(self.get_email_template_names(), context)
        headers = {}
        if self.cleaned_data.has_key('email'):
            headers = {'Reply-to': self.cleaned_data.get('email')}
        mail_managers(self.subject, 
                      message, 
                      attachments=request.FILES, 
                      fail_silently=False,
                      headers=headers)
        
    def clean(self):
        size = FEEDBACK_ATTACHMENT_SIZE*1024*1024
        cleaned = self.cleaned_data.copy()
        
        for field_name in cleaned:
            field = self[field_name].field
            data = self[field_name].data
            
            if field.__class__.__name__ == 'FileField' and data.size > size:
                msg = 'Maximum file size is %s MB' % FEEDBACK_ATTACHMENT_SIZE
                self._errors[field_name] = self.error_class([msg])
                
                del self.cleaned_data[field_name]
                
            if field.__class__.__name__ == 'CharField':
                self.cleaned_data[field_name] = mark_safe(self.cleaned_data[field_name])
                
        return self.cleaned_data

    def get_context_data(self, request):
        context = {'fields': {}}
        for name, field in self.fields.iteritems():
            context['fields'][name] = self.cleaned_data.get(name, None)
            # leaved for compatibility. Will be removed in feedback v 1.2
            context[name] = self.cleaned_data.get(name, None)
        context['form'] = self
        context['request'] = request
        return context

    def get_settings_key(self):
        '''Finds its own class in settings.FEEDBACK_FORMS dictionary
        and returns appropriate key
        '''
        reverse_forms_dict = dict(
            (v.rsplit('.', 1)[1], k) for k, v in FEEDBACK_FORMS.iteritems()
        )
        return reverse_forms_dict.get(self.__class__.__name__, 'default')

    def get_template_name(self):
        import django
        import warnings
        warnings.warn("Deprecated method. Use ``get_email_template_names`` instead.", DeprecationWarning)
        return self.get_email_template_names()

    def get_email_template_names(self):
        """
        Returns template names for Email rendering.
        """
        templates = ['feedback/feedback_message.txt',]
        # Insert before default template
        templates[0:0] = ['feedback/%s/email.txt' % self.get_settings_key(),]
        print 'Email templates:', templates
        return templates

    def get_template(self):
        """Deprecated method. Set class property ``template_names``"""
        import django
        import warnings
        warnings.warn("Deprecated method. Set ``template_names`` class attribute instead.", DeprecationWarning)
        if django.VERSION < (1, 2):
            from django.template.loader import find_template_source as find_template
        else:
            from django.template.loader import find_template

        for template in self.get_email_template_names():
            try:
                _, filename = find_template(template)
                return filename
            except TemplateDoesNotExist:
                continue
        return 'feedback/feedback_message.txt'
        
    def get_dictionary(self):
        
        if (self.is_valid()):
            field_dictionary = {'subject': unicode(self.subject)}
            
            counter = 0
            for field in self.serialized_fields:
                field_dictionary[str(counter)] = {
                    'key':unicode(self[field].label),
                    'value':unicode(self.cleaned_data[field])}
                counter += 1
                
            return field_dictionary


class FeedbackForm(BaseFeedbackForm):
    email = forms.EmailField(label=_('Email'), max_length=200)
    topic = forms.CharField(label=_('Topic'), max_length=200)
    response = forms.CharField(label=_('Message text'), max_length=500,
        widget=forms.Textarea(attrs={'cols':'30', 'rows':'5'}))
    subject = _('Feedback form')
    
    serialized_fields = ('email', 'topic', 'response',)
