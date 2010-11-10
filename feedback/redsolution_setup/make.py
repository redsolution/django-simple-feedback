from grandma.make import BaseMake
from grandma.models import GrandmaSettings
from django.template.loader import render_to_string
import os
import shutil

class Make(BaseMake):
    def make(self):
        super(Make, self).make()
        grandma_settings = GrandmaSettings.objects.get_settings()
        grandma_settings.render_to('settings.py', 'feedback/grandma/settings.py')
        grandma_settings.render_to('urls.py', 'feedback/grandma/urls.py')

    def postmake(self):
        super(Make, self).postmake()
        grandma_settings = GrandmaSettings.objects.get_settings()
        if not grandma_settings.package_was_installed('grandma.django-server-config'):
            feedback_dir = os.path.dirname(os.path.dirname(__file__))
#           try delete dir before copy. be carefull!!!
            try:
                shutil.rmtree(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(feedback_dir))), 'media/feedback/'),)
#            no such directory
            except OSError:
                pass
#            copy media to cms media directory
            shutil.copytree(
                os.path.join(feedback_dir, 'media/feedback/'),
                os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(feedback_dir))), 'media/feedback/'),
                )
        if grandma_settings.package_was_installed('grandma.django-menu-proxy'):
            grandma_settings.render_to('settings.py', 'feedback/grandma/settings_menu.py')
