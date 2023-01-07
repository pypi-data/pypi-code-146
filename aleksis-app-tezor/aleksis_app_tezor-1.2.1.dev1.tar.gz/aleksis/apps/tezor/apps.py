from aleksis.core.util.apps import AppConfig


class DefaultConfig(AppConfig):
    name = "aleksis.apps.tezor"
    verbose_name = "AlekSIS — Tezor"
    dist_name = "AlekSIS-App-Tezor"

    urls = {
        "Repository": "https://edugit.org/AlekSIS/onboarding//AlekSIS-App-Tezor",
    }
    licence = "EUPL-1.2+"
    copyright_info = (
        ([2022], "Dominik George", "dominik.george@teckids.org"),
        ([2022], "Tom Teichler", "tom.teichler@teckids.org"),
    )

    def ready(self):
        from .signals import update_on_person_change  # noqa
