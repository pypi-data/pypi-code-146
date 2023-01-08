from django.apps import AppConfig


class FinfloConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'finflo'

    def ready(self):
        import finflo.signals
