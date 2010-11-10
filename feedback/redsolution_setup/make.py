from redsolutioncms.make import BaseMake
from redsolutioncms.models import CMSSettings
from feedback.redsolution_setup.models import FeedbackSettings
from os.path import dirname, join
import shutil

class Make(BaseMake):

    def make(self):
        super(Make, self).make()
        cms_settings = CMSSettings.objects.get_settings()
        feedback_settings = FeedbackSettings.objects.get_settings()

        cms_settings.render_to('settings.py', 'feedback/redsolutioncms/settings.pyt', {
            'feedback_settings': feedback_settings,
        })
        cms_settings.render_to('urls.py', 'feedback/redsolutioncms/urls.pyt', {
            'feedback_settings': feedback_settings,
        })


    def postmake(self):
        super(Make, self).postmake()
        cms_settings = CMSSettings.objects.get_settings()
        feedback_settings = FeedbackSettings.objects.get_settings()
        
        feedback_media_dir = join(dirname(dirname(__file__)), 'media')
        project_media_dir = join(cms_settings.project_dir, 'media')

#       WARNING! Silently delete media dirs
        try:
            shutil.rmtree(join(project_media_dir, 'feedback'))
#            no such directory
        except OSError:
            pass

        if 'redsolutioncms.django-server-config' not in cms_settings.installed_packages:
#           copy files to media directory
            shutil.copytree(
                join(feedback_media_dir, 'feedback'),
                join(project_media_dir, 'feedback'),
            )

make = Make()
