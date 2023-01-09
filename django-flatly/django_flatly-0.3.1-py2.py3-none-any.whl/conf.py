from django.conf import settings

TEMPLATE_ROOT = getattr(settings, 'FLATLY_TEMPLATE_ROOT', 'flatly')
ENGINE = getattr(settings, 'FLATLY_ENGINE', None)
EXTENSIONS = getattr(settings, 'FLATLY_EXTENSIONS', ['html'])
CACHE_ENABLED = getattr(settings, 'FLATLY_CACHE_ENABLED', not settings.DEBUG)
