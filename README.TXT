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
        
        ``(r'^feedback/', include('feedback.urls'))``

    in urlpatterns. That's all!

.. describe:: Requriments

   Note that feedback uses ajax form based on jQuery, so you need to include jQuery
   in your page. You can install it from Google hosting. Just include 

        ``<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>``

    in <head> element.

To find out more documentation, run in doc folder

    ./doc$ make html

and browse documentation in doc/build/html
