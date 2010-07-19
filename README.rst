Simple Django feedback application
====================================

.. describe:: Usage

    Add ``feedback`` to INSTALLED_APPS
        
        INSTALLED_APPS = [
            ...
            'feedback',
            ...
        ]

    Load feedback template tags:
    

        ``{% load feedback_tags %}``

    Insert template tag in your template
    
        ``{% show_feedback %}``
    
    Include something like
        
        ``(r'^feedback', include('feedback.urls'))``

    in urlpatterns. That's all!
    
.. describe:: Requriments

   Note that feedback uses ajax form based on jQuery, so you need to include jQuery
   in your page. You can install it from Google hosting. Just include 

        ``<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>``

    in <head> element.

.. describe:: Customize

	You can customize these settings in your settings.py:
	

		``FEEDBACK_FORM`` - form, that will be displayed to user. 
		By default form contains email, topic and response fields
		
		``DIRECT_TO_TEMPLATE`` - Should application render feedback form 
		direct to template ``fedback/feedback_page.html``, or you prefer to use
		template tag in other templates.

To find out more documentation, run in doc folder

    ./doc$ make html

and browse documentation in doc/build/html
