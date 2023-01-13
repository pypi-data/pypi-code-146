# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio-Theme-TUW hacks and overrides to be applied on application startup.

This module provides a blueprint whose sole purpose is to execute some code exactly
once during application startup (via ``bp.record_once()``).
These functions will be executed after the Invenio modules' extensions have been
initialized, and thus we can rely on them being already available.
"""

from logging import ERROR
from logging.handlers import SMTPHandler

from flask import Blueprint

from .formatters import CustomFormatter
from .permissions import TUWCommunitiesPermissionPolicy

blueprint = Blueprint("invenio_config_tuw_hacks", __name__)


@blueprint.record_once
def register_smtp_error_handler(state):
    """Register email error handler to the application."""
    # NOTE: this function is called on blueprint registration rather than in the
    #       InvenioConfigTUW extension, to ensure that all configuration has been
    #       loaded and all relevant extensions (e.g. Invenio-Mail) have been registered
    app = state.app
    handler_name = "invenio-config-tuw-smtp-error-handler"

    # check reasons to skip handler registration
    error_mail_disabled = app.config.get("CONFIG_TUW_DISABLE_ERROR_MAILS", False)
    if app.debug or app.testing or error_mail_disabled:
        # email error handling should occur only in production mode, if not disabled
        return

    elif any([handler.name == handler_name for handler in app.logger.handlers]):
        # we don't want to register duplicate handlers
        return

    elif "invenio-mail" not in app.extensions:
        app.logger.warning(
            (
                "The Invenio-Mail extension is not loaded! "
                "Skipping registration of SMTP error handler."
            )
        )
        return

    # check if mail server and admin email(s) are present in the config
    # if not raise a warning
    if app.config.get("MAIL_SERVER") and app.config.get("MAIL_ADMIN"):
        # configure auth
        username = app.config.get("MAIL_USERNAME")
        password = app.config.get("MAIL_PASSWORD")
        auth = (username, password) if username and password else None

        # configure TLS
        secure = None
        if app.config.get("MAIL_USE_TLS"):
            secure = ()

        # initialize SMTP Handler
        mail_handler = SMTPHandler(
            mailhost=(app.config["MAIL_SERVER"], app.config.get("MAIL_PORT", 25)),
            fromaddr=app.config["SECURITY_EMAIL_SENDER"],
            toaddrs=app.config["MAIL_ADMIN"],
            subject=app.config["THEME_SITENAME"] + " - Failure",
            credentials=auth,
            secure=secure,
        )
        mail_handler.name = handler_name
        mail_handler.setLevel(ERROR)
        mail_handler.setFormatter(CustomFormatter())

        # attach to the application
        app.logger.addHandler(mail_handler)

    else:
        app.logger.warning(
            "Mail configuration missing: SMTP error handler not registered!"
        )


@blueprint.record_once
def override_communities_permissions(state):
    """Override permission policy class for communities."""
    # TODO change this as soon as Invenio-Communities allows to do it via config
    app = state.app
    communities = app.extensions.get("invenio-communities", None)
    assert communities is not None

    # override the permission policy class for all communities services
    svc = communities.service
    svc.config.permission_policy_cls = TUWCommunitiesPermissionPolicy
    svc.files.config.permission_policy_cls = TUWCommunitiesPermissionPolicy
    svc.members.config.permission_policy_cls = TUWCommunitiesPermissionPolicy
