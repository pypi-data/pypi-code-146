import posixpath

import django
from django.template.exceptions import TemplateDoesNotExist
from django.urls import Resolver404, ResolverMatch, URLPattern
from django.urls.resolvers import RegexPattern

from . import conf
from .helpers import get_template_by_name, safe_join
from .views import serve

if django.VERSION >= (4, 1):  # noqa
    class FlatlyURLPattern(URLPattern):
        def resolve(self, path):
            match = self.pattern.match(path)
            if match:
                new_path, args, captured_kwargs = match
                # Pass any default args as **kwargs.
                kwargs = {**captured_kwargs, **self.default_args}

                path = kwargs.get('path')
                path = posixpath.normpath(path).lstrip('/')
                path = path.replace('-', '_')

                if conf.TEMPLATE_ROOT:
                    template_name = safe_join(path, conf.TEMPLATE_ROOT)
                else:
                    template_name = path

                try:
                    template = get_template_by_name(template_name)
                except TemplateDoesNotExist:
                    raise Resolver404({})

                return ResolverMatch(
                    self.callback,
                    (template,),
                    {},
                    route=str(self.pattern),
                    captured_kwargs=captured_kwargs,
                    extra_kwargs=self.default_args,
                )

else:
    class FlatlyURLPattern(URLPattern):
        def resolve(self, path):
            match = self.pattern.match(path)
            if match:
                new_path, args, kwargs = match

                path = kwargs.get('path')
                path = posixpath.normpath(path).lstrip('/')
                path = path.replace('-', '_')

                if conf.TEMPLATE_ROOT:
                    template_name = safe_join(path, conf.TEMPLATE_ROOT)
                else:
                    template_name = path

                try:
                    template = get_template_by_name(template_name)
                except TemplateDoesNotExist:
                    raise Resolver404({})

                if django.VERSION >= (2, 2):
                    return ResolverMatch(
                        self.callback, (template,), {}, route=str(self.pattern)
                    )
                else:
                    return ResolverMatch(self.callback, (template,), {})


def flatly_path(route, view):
    pattern = RegexPattern(route, name=None, is_endpoint=True)
    return FlatlyURLPattern(pattern, view, None, None)


app_name = 'flatly'
urlpatterns = [
    flatly_path(r'^(?P<path>.*/|)$', serve)
]
