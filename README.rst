====================================
Simple Django feedback application
====================================

Quick start
```````````

In code
-------

Add ``feedback`` to INSTALLED_APPS ::
    
    INSTALLED_APPS = [
        ...
        'feedback',
        ...
    ]

Example urlpatterns:

    ``(r'^feedback', include('feedback.urls'))``

Synchronize your database models run ``django syncdb``

In templates
------------
Load tags library:

    ``{% load feedback_tags %}``

Insert template tag in your template

    ``{% show_feedback [key] %}``,

where ``key`` is feedback form key. Default key value is ``default``.


Requriments
```````````

Note that feedback uses ajax form based on jQuery, so you need to include jQuery
in your page. You can install it from Google hosting:

	``<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js"></script>``


Settings
````````

**DIRECT_TO_TEMPLATE**
  When ``True``, application will show **default** feedback form 
  with template ``feedback/feedback_page.html`` where feedback urls were included. 
  If you set this setting to ``False`` you should display feedback form manually, 
  by including ``{% show_feedback [key] %}`` tag into template. 

**FEEDBACK_FILE_SIZE**
   This parameter sets attachments maximum file size in megabytes.
   Default value is 2 MB.

**FEEDBACK_FORMS**
   Registry for custom feedback forms. See Customize section.

Customize
`````````

If you want to customize default feedback form, or add your own, you have to 
create an application with your forms. All feedback forms should be subclasses of
``feedback.forms.BaseFeedbackForm``. Here is an example of custom feedback class: ::   

    from django import forms
    from feedback.forms import BaseFeedbackForm
    
    
    class OrderForm(BaseFeedbackForm):
        name = forms.CharField(label=u'Your name', max_length=200)
        email = forms.EmailField(label=u'Your Email', max_length=200)
        phone = forms.CharField(label=u'Phone', max_length=200)
        address = forms.CharField(label=u'Your address', max_length=200)
        date = forms.CharField(label=u'Date and time', max_length=200)
        file = forms.FileField(label=u'Attach the file')
    
        response = forms.CharField(label=u'Comment', max_length=500,
            widget=forms.Textarea(attrs={'cols':'30', 'rows':'5'}))
        subject = u'Custom order form'
        
        serialized_fields = ('name', 'phone', 'address', 'response')

``subject`` attribute appears in email subject.

``serialized_fields`` attribute contains names of fields, those will be stored in DB. 

Than, you need to put feedback forms in your settings.py:

``FEEDBACK_FORMS`` - dictionary object, describes feedback forms on your
site. Every key-value pair stands for feedback form object. For example: ::

    FEEDBACK_FORMS = {
        'default': 'feedback.forms.FeedbackForm',
        'order': 'mysite.custom_feedback.forms.OrderForm',
    }


Now we can include ``{% show_feedback order %}`` in  template and get overriden form.


Custom templates
-----------------

You can create custom templates if you have custom form class. Application search them by first. Template names are:

**feedback/FORM_KEY/feedback.html**, **feedback/feedback.html**
  for rendering form itself
**feedback/FORM_KEY/thankyou.html**, **feedback/thankyou.html**
  for rendering success response
**feedback/FORM_KEY/email.txt**, **feedback/feedback_messages.txt**
  for rendering email text




What's new
``````````

0.3.0 - Model for storing attachments in database added. Now attachments available in admin interface.

0.3.1 - Feedback Emails are 'marked safe'

0.3.2 - Added Reply-to header if email form has ``email`` key

0.3.3 - Fixed javascript URL in order to work with staticfiles

0.3.4 - Added customizable templates

Redsolution CMS classifiers:
````````````````````````````

`Content plugins`_

.. _`Content plugins`: http://www.redsolutioncms.org/classifiers/content
