from django.apps import AppConfig

from gdaps.api import require_app


class GrapheneConfig(AppConfig):
    name = "gdaps.graphene"

    def ready(self):
        require_app(self, "graphene_django")
