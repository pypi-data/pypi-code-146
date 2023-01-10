import json
from functools import update_wrapper

from django.urls import reverse

from .views import OmniSearchModelView


class OmniSearchAdminSite:
    def get_omnisearch_model(self, app, model):
        return {
            'app': {
                'name': str(app['name']),
                'label': str(app['app_label']),
                'url': str(app['app_url']),
            },
            'addUrl': str(model['add_url']),
            'adminUrl': str(model['admin_url']),
            'ident': str(model['model']._meta.model_name),
            'name': str(model['name']),
            'objectName': str(model['object_name']),
        }

    def get_omnisearch_context(self, ctx):
        items = []
        for app in ctx['available_apps']:
            for model in app['models']:
                items.append(self.get_omnisearch_model(app, model))
        if len(items) == 0:
            return None
        return {
            'models': items,
            'placeholder': str(ctx['site_header']),
            'searchUrl': reverse("admin:omnisearch"),
        }

    def omnisearch_view(self, request):
        return OmniSearchModelView.as_view(admin_site=self)(request)

    def each_context(self, request):
        ctx = super().each_context(request)
        ctx['omni_search'] = json.dumps(self.get_omnisearch_context(ctx))
        return ctx

    def get_urls(self):
        from django.urls import path

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)
            wrapper.admin_site = self
            return update_wrapper(wrapper, view)
        return [
            path("omnisearch/", self.omnisearch_view, name="omnisearch"),
        ] + super().get_urls()
