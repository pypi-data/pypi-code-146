from django.apps import AppConfig


class BaseSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base_system'
