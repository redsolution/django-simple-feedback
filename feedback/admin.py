# -*- coding: utf-8 -*-

import os

from django.contrib import admin
from feedback.models import Response, ResponseAttachments

class ResponseAdmin(admin.ModelAdmin):
    list_display = ('send_time',)
    
    change_form_template = 'admin/change_form_template.html'
    change_list_template = 'admin/change_list_template.html'
    
    def change_view(self, request, object_id, extra_context=None):
        extra_context = {
            'form': Response.objects.get(id=object_id).get_response(),
            'attachments': ResponseAttachments.objects.filter(response=object_id)}
        return super(ResponseAdmin, self).change_view(request, object_id, extra_context)

admin.site.register(Response, ResponseAdmin)
    