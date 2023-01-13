# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2022 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Utility functions."""

from flask_principal import Identity
from flask_security import current_user
from invenio_access import any_user
from invenio_access.utils import get_identity
from invenio_accounts import current_accounts
from invenio_accounts.models import User

# Utilities for internal use
# --------------------------


def get_user_by_username(username):
    """Get the user identified by the username."""
    profile = User.query.filter(User.username == username).one_or_none()

    if profile is not None:
        return profile.user

    return None


def get_user(identifier):
    """Get the user identified by the given ID, email or username."""
    user = current_accounts.datastore.get_user(identifier)
    if user is None:
        get_user_by_username(identifier)

    return user


def get_identity_for_user(user):
    """Get the Identity for the user specified via email, ID or username."""
    identity = None
    if user is not None:
        # note: this seems like the canonical way to go
        #       'as_user' can be either an integer (id) or email address
        u = get_user(user)
        if u is not None:
            identity = get_identity(u)
        else:
            raise LookupError("user not found: %s" % user)

    if identity is None:
        identity = Identity(1)

    identity.provides.add(any_user)
    return identity


# Utilities for invenio configuration
# -----------------------------------


def check_user_email_for_tuwien(user):
    """Check if the user's email belongs to TU Wien (but not as a student)."""
    domain = user.email.split("@")[-1]
    return domain.endswith("tuwien.ac.at") and "student" not in domain


def current_user_as_creator():
    """Use the currently logged-in user to populate a creator in the deposit form."""
    profile = current_user.user_profile or {}
    if profile.get("full_name") is None:
        return []

    name_parts = profile["full_name"].split()
    if len(name_parts) <= 1:
        return []

    first_name = " ".join(name_parts[:-1])
    last_name = name_parts[-1]
    full_name = "{}, {}".format(last_name, first_name)
    # TODO parse affiliation from user profile
    creator = {
        "affiliations": [{"id": "04d836q62", "name": "TU Wien"}],
        "person_or_org": {
            "family_name": last_name,
            "given_name": first_name,
            "identifiers": [],
            "name": full_name,
            "type": "personal",
        },
        "role": "contactperson"
    }

    return [creator]

