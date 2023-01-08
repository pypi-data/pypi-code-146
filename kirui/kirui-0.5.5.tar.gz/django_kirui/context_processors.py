import json

from django.conf import settings
from django.middleware import csrf
from django.urls import reverse
from django.utils.module_loading import import_string


class DjangoSamonBinding:
    def __init__(self, request):
        self.request = request

    def url(self, view_name, *args, **kwargs):
        return reverse(view_name, args=args, kwargs=kwargs)

    def bind_url(self, view_name, *args, **kwargs):
        return "${'" + self.url(view_name, *args, **kwargs) + "'}"

    def bind_dict(self, d):
        return "${" + json.dumps(d) + "}"

    @property
    def csrf_token(self):
        return csrf.get_token(self.request)

    def static(self, path):
        return f'{settings.STATIC_URL}{path}'


def djsamon(request):
    klass = getattr(settings, 'DJANGO_SAMON_BINDING_CLASS', 'django_kirui.context_processors.DjangoSamonBinding')
    klass = import_string(klass)

    return {
        'djsamon': klass(request)
    }
