# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module containing some customizations and configuration for TU Wien."""

from datetime import datetime

from flask_babelex import gettext as _
from invenio_oauthclient.views.client import auto_redirect_login

from .auth import TUWSSOSettingsHelper
from .forms import tuw_registration_form
from .permissions import TUWRecordPermissionPolicy, TUWRequestsPermissionPolicy
from .utils import check_user_email_for_tuwien, current_user_as_creator

# Invenio-Config-TUW
# ==================

CONFIG_TUW_AUTO_TRUST_USERS = True
"""Whether or not to auto-assign the 'trusted-user' role to new users."""

CONFIG_TUW_AUTO_TRUST_CONDITION = check_user_email_for_tuwien
"""Function for checking if the user is eligible for auto-trust.

This must be a function that accepts a 'user' argument and returns a boolean value.
Alternatively, it can be set to None. This is the same as ``lambda u: True``.
"""

CONFIG_TUW_AUTO_ALLOW_PUBLISH = True
"""Whether or not to auto-assign the 'trusted-publisher' role to new users.

Note: This setting will only come into play if AUTO_TURST_USERS is enabled.
"""

CONFIG_TUW_AUTO_ALLOW_PUBLISH_CONDITION = check_user_email_for_tuwien
"""Similar to AUTO_TRUST_CONDITION, but for the 'trusted-publisher' role."""

CONFIG_TUW_READ_ONLY_MODE = False
"""Disallow insert and update operations in the repository."""

CONFIG_TUW_DISABLE_ERROR_MAILS = False
"""Disable registration of the SMTP mail handler to suppress warnings."""


# Invenio-Mail
# ============
# See https://invenio-mail.readthedocs.io/en/latest/configuration.html

MAIL_SERVER = "localhost"
"""Domain ip where mail server is running."""

SECURITY_EMAIL_SENDER = "no-reply@researchdata.tuwien.ac.at"
"""Email address used as sender of account registration emails."""

SECURITY_EMAIL_SUBJECT_REGISTER = _("Welcome to TU Data!")
"""Email subject for account registration emails."""

MAIL_SUPPRESS_SEND = True
"""Disable email sending by default."""


# Invenio-Previewer
# =================

PREVIEWER_MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

PREVIEWER_MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


# Authentication
# ==============

SECURITY_CHANGEABLE = False
"""Allow password change by users."""

SECURITY_RECOVERABLE = False
"""Allow password recovery by users."""

SECURITY_REGISTERABLE = False
""""Allow users to register."""

SECURITY_CONFIRMABLE = False
"""Allow user to confirm their email address."""

ACCOUNTS = True
"""Tells if the templates should use the accounts module."""

ACCOUNTS_LOCAL_LOGIN_ENABLED = False
"""Disable local login (rely only on OAuth)."""

USERPROFILES_READ_ONLY = True
"""Prevent users from updating their profiles."""


# Invenio-OAuthClient
# ===================

ACCOUNTS_LOGIN_VIEW_FUNCTION = auto_redirect_login

OAUTHCLIENT_SIGNUP_FORM = tuw_registration_form

OAUTHCLIENT_AUTO_REDIRECT_TO_EXTERNAL_LOGIN = True

helper = TUWSSOSettingsHelper(
    title="TU Wien SSO",
    description="TU Wien Single Sign-On",
    base_url="https://s194.dl.hpc.tuwien.ac.at",
    realm="tu-data-test",
)

OAUTHCLIENT_KEYCLOAK_REALM_URL = helper.realm_url
OAUTHCLIENT_KEYCLOAK_USER_INFO_URL = helper.user_info_url
OAUTHCLIENT_KEYCLOAK_AUD = "tu-data-test"
OAUTHCLIENT_KEYCLOAK_VERIFY_AUD = True

keycloak_remote_app = helper.remote_app
keycloak_remote_app["precedence_mask"] = {
    "email": True,
    "username": True,
    "user_profile": {"full_name": True, "affiliations": True},
}

OAUTHCLIENT_REMOTE_APPS = {
    "keycloak": keycloak_remote_app,
}


# Invenio-App-RDM
# ================

APP_RDM_DEPOSIT_FORM_DEFAULTS = {
    "publication_date": lambda: datetime.now().strftime("%Y-%m-%d"),
    "creators": current_user_as_creator,
    "rights": [
        {
            "id": "cc-by-4.0",
            "title": "Creative Commons Attribution 4.0 International",
            "description": (
                "The Creative Commons Attribution license allows "
                "re-distribution and re-use of a licensed work "
                "on the condition that the creator is "
                "appropriately credited."
            ),
            "link": "https://creativecommons.org/licenses/by/4.0/legalcode",
        }
    ],
    "publisher": "TU Wien",
    "resource_type": {
        "id": "dataset",
    },
    "version": "1.0.0",
}

RDM_CITATION_STYLES = [
    ("apa", _("APA")),
    ("bibtex", _("BibTeX")),
    ("ieee", _("IEEE")),
]

RDM_PERMISSION_POLICY = TUWRecordPermissionPolicy

OAISERVER_METADATA_FORMATS = {
    "oai_dc": {
        "serializer": "invenio_rdm_records.oai:dublincore_etree",
        "schema": "http://www.openarchives.org/OAI/2.0/oai_dc.xsd",
        "namespace": "http://www.openarchives.org/OAI/2.0/oai_dc/",
    },
    "datacite": {
        "serializer": "invenio_rdm_records.oai:datacite_etree",
        "schema": "http://schema.datacite.org/meta/nonexistant/nonexistant.xsd",
        "namespace": "http://datacite.org/schema/nonexistant",
    },
    "oai_datacite": {
        "serializer": "invenio_rdm_records.oai:oai_datacite_etree",
        "schema": "http://schema.datacite.org/oai/oai-1.1/oai.xsd",
        "namespace": "http://schema.datacite.org/oai/oai-1.1/",
    },
}


# Invenio-Requests
# ================

REQUESTS_PERMISSION_POLICY = TUWRequestsPermissionPolicy


# Limitations
# ===========

RATELIMIT_ENABLED = True

RATELIMIT_AUTHENTICATED_USER = "30000 per hour;3000 per minute"

RATELIMIT_GUEST_USER = "6000 per hour;600 per minute"

# Default file size limits for deposits: 75 GB
max_file_size = 75 * (1024**3)

# ... per file
FILES_REST_DEFAULT_MAX_FILE_SIZE = max_file_size

# ... for the entire bucket
FILES_REST_DEFAULT_QUOTA_SIZE = max_file_size

# ... and on the deposit form UI
APP_RDM_DEPOSIT_FORM_QUOTA = {
    "maxFiles": 100,
    "maxStorage": max_file_size,
}

# show the display in powers of 2 (KiB, MiB, GiB, ...) rather than 10 (KB, MB, GB, ...)
APP_RDM_DISPLAY_DECIMAL_FILE_SIZES = False

# for multipart form uploads, we'll use a max. content length of 100 MB
# (e.g. community logo upload, but not record/draft file deposits)
MAX_CONTENT_LENGTH = 100 * (1024**2)


# Misc. Configuration
# ===================

# Default locale (language)
BABEL_DEFAULT_LOCALE = "en"

# Default time zone
BABEL_DEFAULT_TIMEZONE = "Europe/Vienna"

# Recaptcha public key (change to enable).
RECAPTCHA_PUBLIC_KEY = None

# Recaptcha private key (change to enable).
RECAPTCHA_PRIVATE_KEY = None

# Preferred URL scheme to use
PREFERRED_URL_SCHEME = "https"
