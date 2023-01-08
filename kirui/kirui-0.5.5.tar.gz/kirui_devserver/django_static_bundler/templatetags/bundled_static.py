from django import template
from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse

register = template.Library()


@register.simple_tag
def bundled_static(path):
    if settings.DEBUG:
        return reverse('django_static_bundler:bundle-static-file', args=(path,))

    return static(path)
