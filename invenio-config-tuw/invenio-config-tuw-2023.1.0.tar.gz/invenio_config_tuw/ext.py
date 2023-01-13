# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2022 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module containing some customizations and configuration for TU Wien."""

from flask.config import Config
from flask_security.signals import user_registered

from . import config
from .auth.utils import auto_trust_user


class TUWConfig(Config):
    """Override for the Flask config that evaluates the SITE_{API,UI}_URL proxies."""

    @classmethod
    def from_flask_config(cls, config):
        """Create a clone of the given config."""
        return cls(config.root_path, config)

    def __getitem__(self, key):
        value = super().__getitem__(key)

        # give special treatment to the URL configuration items:
        # enforce their evaluation as strings
        if key in ("SITE_UI_URL", "SITE_API_URL"):
            value = str(value)

        return value


@user_registered.connect
def auto_trust_new_user(sender, user, **kwargs):
    # NOTE: 'sender' and 'kwargs' are ignored, but they're required to match the
    #       expected function signature
    # NOTE: this function won't be called when a user is created via the CLI
    #       ('invenio users create'), because it doesn't send the 'user_registered'
    #       signal
    auto_trust_user(user)


class InvenioConfigTUW(object):
    """Invenio-Config-TUW extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions["invenio-config-tuw"] = self

        @app.before_first_request
        def hack_app_config():
            # replace the app's config with our own override that evaluates the
            # LocalProxy objects used for SITE_{API,UI}_URL by casting them into strings
            # (which is their expected type)
            app.config = TUWConfig.from_flask_config(app.config)

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if len(k.replace("_", "")) >= 3 and k.isupper():
                app.config.setdefault(k, getattr(config, k))

        # the datacenter symbol seems to be the username for DataCite Fabrica
        if app.config.get("DATACITE_ENABLED", False):
            key = "DATACITE_DATACENTER_SYMBOL"
            if not app.config.get(key, None):
                app.config[key] = app.config["DATACITE_USERNAME"]
