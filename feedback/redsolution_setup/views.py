from feedback.redsolution_setup.admin import FeedbackSettingsAdmin

def index(request):
    admin_instance = FeedbackSettingsAdmin()
    return admin_instance.change_view(request)
