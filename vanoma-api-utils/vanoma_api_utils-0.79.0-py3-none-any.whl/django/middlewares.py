import re
from typing import Any
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from djangorestframework_camel_case.settings import api_settings  # type: ignore
from djangorestframework_camel_case.util import underscoreize  # type: ignore

CAMECAL_CASE_PATTERN = re.compile(r"(?<!^)(?=[A-Z])")


class CamelCaseMiddleWare:
    """
    Middleware to convert camelCase query params to snake_case. Copied from https://github.com/vbabiy/djangorestframework-camel-case/pull/68
    """

    def __init__(self, get_response: Any) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request.GET = underscoreize(request.GET, **api_settings.JSON_UNDERSCOREIZE)

        # Convert value of "sort" paremeter to snake case since they refer to fields
        if request.GET.get("sort") is not None:
            request.GET["sort"] = CAMECAL_CASE_PATTERN.sub(
                "_", request.GET["sort"]
            ).lower()

        # Convert value of "fields" paremeter to snake case since they refer to fields
        if request.GET.get("fields") is not None:
            request.GET["fields"] = CAMECAL_CASE_PATTERN.sub(
                "_", request.GET["fields"]
            ).lower()

        return self.get_response(request)
