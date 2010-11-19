from django.db import models

from django.conf import settings

# probably it isn't a model, but in __init__.py this code breaks setup.py

class BogusSMTPConnection(object):
    """Instead of sending emails, print them to the console."""

    def __init__(*args, **kwargs):
        print "Initialized bogus SMTP connection"

    def open(self):
        print "Open bogus SMTP connection"

    def close(self):
        print "Clone bogus SMTP connection"

    def send_messages(self, messages):
        print "Sending through bogus SMTP connection:"
        for message in messages:
            print "From: %s" % message.from_email
            print "To: %s" % (", ".join(message.to))
            print "Subject: %s\n\n" % message.subject
            print "%s" % message.body
            print messages
        return len(messages)


if settings.DEBUG:
    from django.core import mail
    mail.SMTPConnection = BogusSMTPConnection


