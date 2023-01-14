""" 
Author:		 Muhammad Tahir Rafique
Date:		 2022-11-29 15:59:16
Project:	 Django-File-Explorer
Description: Provide about view.
"""

from django import http
from django.views.generic.base import TemplateView
from django.urls import reverse

class About(TemplateView):
    template_name = 'explorer/about.html'
    http_method_names = ['get']
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return http.HttpResponseRedirect(f'/admin/login/?next={reverse("explorer-about")}')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # GETTING CONTEXT
        context = self.get_context_data()
        return self.render_to_response(context)