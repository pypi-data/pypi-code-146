from aleksis.core.util.apps import AppConfig


class DefaultConfig(AppConfig):
    name = "aleksis.apps.paweljong"
    verbose_name = "AlekSIS — Paweljong (Camp/Event management)"
    dist_name = "AlekSIS-App-Paweljong"

    urls = {
        "Repository": "https://edugit.org/Teckids/hacknfun/AlekSIS-App-Paweljong",
    }
    licence = "EUPL-1.2+"
    copyright_info = (
        ([2018, 2021, 2022], "Dominik George", "dominik.george@teckids.org"),
        ([2019, 2022], "Tom Teichler", "tom.teichler@teckids.org"),
    )
