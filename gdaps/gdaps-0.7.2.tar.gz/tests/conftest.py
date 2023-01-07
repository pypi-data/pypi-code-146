import django
from pathlib import Path


def pytest_configure(config):
    from django.conf import settings

    BASE_DIR = Path(__file__).resolve().parent

    settings.configure(
        SECRET_KEY="test",
        BASE_DIR=BASE_DIR,
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
        },
        INSTALLED_APPS=["gdaps", "tests.plugins.plugin1"],
        PLUGIN1={"OVERRIDE": 20},
        PROJECT_NAME="foo_bar",
        GDAPS={"FRONTEND_ENGINE": "unknown"},
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [BASE_DIR / "templates"],
                "APP_DIRS": True,
            },
        ],
    )

    django.setup()
