# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.asgi.middleware import ASGIMiddleware
from contrast.agent.middlewares.route_coverage.django_routes import DjangoRoutesMixin
from contrast.utils.decorators import fail_quietly

from contrast.agent.assess.rules.config import (
    DjangoHttpOnlyRule,
    DjangoSecureFlagRule,
    DjangoSessionAgeRule,
)

from contrast.extern import structlog as logging
from contrast.utils.decorators import cached_property

# pylint: disable=dangerous-framework-import
from django.http import HttpResponse
from contrast.utils.exceptions.security_exception import SecurityException

logger = logging.getLogger("contrast")


class DjangoASGIMiddleware(DjangoRoutesMixin, ASGIMiddleware):
    def __init__(self, asgi_app):
        self.app_name = self.get_app_name()

        self.config_rules = [
            DjangoSessionAgeRule(),
            DjangoSecureFlagRule(),
            DjangoHttpOnlyRule(),
        ]

        super().__init__(asgi_app, self.app_name)

    @fail_quietly(
        "Unable to get Django application name", return_value="Django Application"
    )
    def get_app_name(self):
        from django.conf import settings

        asgi_application = settings.ASGI_APPLICATION

        return asgi_application.split(".")[0]

    @cached_property
    def name(self):
        return "django"

    def generate_security_exception_response(self):
        return HttpResponse(
            self.OVERRIDE_MESSAGE,
            status=SecurityException.STATUS_CODE,
            content_type="text/html",
        )
