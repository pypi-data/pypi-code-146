# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 - 2021 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Utility functions for authentication."""


from invenio_oauthclient.contrib.keycloak import KeycloakSettingsHelper


class TUWSSOSettingsHelper(KeycloakSettingsHelper):
    """KeycloakSettingsHelper, adjusted for the needs of TU Data."""

    def get_handlers(self):
        return {
            "authorized_handler": "invenio_config_tuw.auth:authorized_signup_handler",
            "disconnect_handlerdler": (
                "invenio_oauthclient.contrib.keycloak.handlers:disconnect_handler"
            ),
            "signup_handler": {
                "info": "invenio_config_tuw.auth:info_handler",
                "setup": "invenio_oauthclient.contrib.keycloak.handlers:setup_handler",
                "view": "invenio_config_tuw.auth:signup_handler",
            },
        }
