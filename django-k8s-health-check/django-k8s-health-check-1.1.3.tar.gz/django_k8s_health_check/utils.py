from django.conf import settings
from django.core.cache import caches
from django.db import connections


class HealthCheck:

    @staticmethod
    def test_databases():
        checks, has_error = {}, False
        for key in settings.DATABASES.keys():
            try:
                if not settings.DATABASES.get(key, {}).get('ENGINE') == 'django.db.backends.dummy':
                    connections[key].cursor()
                checks[key] = True
            except Exception:
                checks[key] = False
                has_error = True

        return has_error, checks

    @staticmethod
    def test_caches():
        checks, has_error = {}, False
        for key in settings.CACHES.keys():
            try:
                caches[key].get('invalid_key', None)
                checks[key] = True
            except Exception:
                checks[key] = False
                has_error = True

        return has_error, checks
