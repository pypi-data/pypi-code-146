# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os
import sys

from contrast.agent.assess.rules.config import (
    DjangoHttpOnlyRule,
    DjangoSecureFlagRule,
    DjangoSessionAgeRule,
)

from contrast.wsgi.middleware import WSGIMiddleware
from contrast.utils.decorators import fail_quietly
from contrast.agent.middlewares.route_coverage.django_routes import DjangoRoutesMixin
from contrast.extern import structlog as logging
from contrast.utils.decorators import cached_property

logger = logging.getLogger("contrast")


class DjangoWSGIMiddleware(DjangoRoutesMixin, WSGIMiddleware):
    """
    A subclass of the WSGI middleware that provides django route coverage and config
    scanning.

    This is not a Django-style middleware - it must wrap django's WSGI_APPLICATION,
    and does not belong in MIDDLEWARE / MIDDLEWARE_CLASSES.
    """

    def __init__(self, wsgi_app):
        self.app_name = self.get_app_name()

        self.config_rules = [
            DjangoSessionAgeRule(),
            DjangoSecureFlagRule(),
            DjangoHttpOnlyRule(),
        ]

        super().__init__(wsgi_app, self.app_name)

    @fail_quietly(
        "Unable to get Django application name", return_value="Django Application"
    )
    def get_app_name(self):
        from django.conf import settings

        wsgi_application = settings.WSGI_APPLICATION

        return wsgi_application.split(".")[0]

    @fail_quietly("Failed to run config scanning rules")
    def _scan_configs(self):
        """
        Run config scanning rules for assess

        Overridden from base class; gets called from base class
        """
        from django.conf import settings as app_settings

        app_config_module_name = os.environ.get("DJANGO_SETTINGS_MODULE")
        if not app_config_module_name:
            logger.warning("Unable to find Django settings for config scanning")
            return

        app_config_module = sys.modules.get(app_config_module_name)
        if not app_config_module:
            logger.warning("Django settings module not loaded; can't scan config")
            return

        for rule in self.config_rules:
            rule.apply(app_settings, app_config_module)

    @cached_property
    def name(self):
        return "django"
