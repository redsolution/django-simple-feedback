Simple Django feedback application
====================================

.. describe:: Usage

    Insert 
    
        ``{% show_feedback %}``
    
    template tag in your template and include something like
        
        ``(r'^feedback/', include('feedback.urls'))``

    in urlpatterns. That's all!

.. describe:: Templates

    Application uses following templates:

        ``fedback/feedback.html`` - to render feedback form

        ``feedback/thankyou.html`` - to render message after submit

        ``feedback/feedback_message.txt`` - to render message, that will 
        be sent after user posts form

To find out more documentation, run 

    ./doc$ make html

and browse documentation in doc/build/html
