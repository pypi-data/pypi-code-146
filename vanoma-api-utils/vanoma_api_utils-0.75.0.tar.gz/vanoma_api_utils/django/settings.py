import os
import dj_database_url  # type: ignore
from typing import Any, Dict
from ..misc import resolve_environment


def resolve_database() -> Dict[str, str]:
    if resolve_environment() == "testing":
        return {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join("/tmp", "db.sqlite3"),
        }

    return dj_database_url.config(conn_max_age=600)


def resolve_logging() -> Dict[str, Any]:
    if resolve_environment() == "testing":
        return {}

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {  # Needed to prettify logs (especially for mini-huey/background task queue) to match gunicon logs format.
                "style": "{",
                "format": "[{asctime}] [{process}] [{levelname}] {message}",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
    }


def resolve_file_storage() -> str:
    if resolve_environment() == "testing":
        return "inmemorystorage.InMemoryStorage"

    return "storages.backends.s3boto3.S3Boto3Storage"


BASE_INSTALLED_APPS = [
    "rest_framework",
    "corsheaders",
    "django_filters",
]

BASE_MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "vanoma_api_utils.django.middlewares.CamelCaseMiddleWare",
]

BASE_REST_FRAMEWORK = {
    "ORDERING_PARAM": "sort",
    "UNAUTHENTICATED_USER": None,
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "EXCEPTION_HANDLER": "vanoma_api_utils.rest_framework.views.exception_handler",
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "DEFAULT_PAGINATION_CLASS": "vanoma_api_utils.rest_framework.pagination.PageNumberPagination",
}
