# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.asgi.middleware import ASGIMiddleware
from contrast.agent.middlewares.app_finder import get_original_app_or_fail
from contrast.utils.decorators import cached_property
from contrast.agent.middlewares.route_coverage.falcon_routes import FalconRoutesMixin

# pylint: disable=dangerous-framework-import
import falcon


class FalconAsyncMiddleware(FalconRoutesMixin, ASGIMiddleware):
    def __init__(self, app, orig_falcon_api_instance=None):
        falcon_app = falcon.asgi.app.App

        _app = (
            orig_falcon_api_instance
            if orig_falcon_api_instance is not None
            and isinstance(orig_falcon_api_instance, falcon_app)
            else get_original_app_or_fail(app, falcon_app)
        )
        self.falcon_app = _app
        # used for route coverage only for falcon middleware
        self.endpoint_cls = None

        super().__init__(_app, app_name="Falcon Application")

    @cached_property
    def name(self):
        return "falcon"
