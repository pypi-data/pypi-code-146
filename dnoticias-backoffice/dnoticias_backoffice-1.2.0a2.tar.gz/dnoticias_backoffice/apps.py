from django.apps import AppConfig


class DnoticiasBackofficeConfig(AppConfig):
    name = 'dnoticias_backoffice'

    def ready(self):
        from .components import load_backoffice_slippers
        load_backoffice_slippers()
