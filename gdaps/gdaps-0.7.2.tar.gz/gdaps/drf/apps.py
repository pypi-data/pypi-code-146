from django.apps import AppConfig

from gdaps.api import require_app


class DrfConfig(AppConfig):
    name = "gdaps.drf"

    def ready(self):
        require_app(self, "rest_framework")
