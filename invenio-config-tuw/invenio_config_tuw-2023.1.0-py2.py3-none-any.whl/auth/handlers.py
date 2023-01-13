# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2022 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Custom handlers for the Keycloak integration."""


from flask import current_app, redirect, render_template, request, session, url_for
from flask_login import current_user
from invenio_db import db
from invenio_oauthclient.contrib.keycloak.helpers import get_user_info
from invenio_oauthclient.errors import (
    OAuthClientMustRedirectSignup,
    OAuthClientUnAuthorized,
)
from invenio_oauthclient.handlers.base import base_signup_handler
from invenio_oauthclient.handlers.ui import (
    oauth_remote_error_handler,
    oauth_resp_remote_error_handler,
)
from invenio_oauthclient.handlers.utils import (
    get_session_next_url,
    response_token_setter,
    token_getter,
    token_session_key,
)
from invenio_oauthclient.proxies import current_oauthclient
from invenio_oauthclient.signals import (
    account_info_received,
    account_setup_committed,
    account_setup_received,
)
from invenio_oauthclient.utils import (
    create_csrf_disabled_registrationform,
    create_registrationform,
    fill_form,
    oauth_authenticate,
    oauth_get_user,
    oauth_register,
)

from .utils import auto_trust_user, create_username_from_info, get_user_by_username


def info_handler(remote, resp):
    """Retrieve remote account information for finding matching local users."""
    # NOTE: for lookup of local users, only the 'external_id' and 'user.email' are used
    #       => calculation of the 'user.user_profile.username'
    #          here should actually be safe
    user_info = get_user_info(remote, resp)

    # fill out the information required by 'invenio-accounts'.
    #
    # note: "external_id": `preferred_username` should also work,
    #       as it is seemingly not editable in Keycloak
    result = {
        "user": {
            "active": True,
            "email": user_info["email"],
            "username": user_info.get("preferred_username"),
            "user_profile": {
                "full_name": user_info.get("name"),
            },
        },
        "external_id": user_info["sub"],
        "external_method": remote.name,
    }

    return result


@oauth_remote_error_handler
def signup_handler(remote, *args, **kwargs):
    """Handle extra signup information.

    :param remote: The remote application.
    :returns: Redirect response or the template rendered.
    """
    try:
        form = create_registrationform(request.form)
        next_url = base_signup_handler(remote, form, *args, **kwargs)
        if form.is_submitted():
            if next_url:
                return redirect(next_url)
            else:
                return redirect("/")

        return render_template(
            current_app.config["OAUTHCLIENT_SIGNUP_TEMPLATE"],
            form=form,
            remote=remote,
            app_title=current_app.config["OAUTHCLIENT_REMOTE_APPS"][remote.name].get(
                "title", ""
            ),
            app_description=current_app.config["OAUTHCLIENT_REMOTE_APPS"][
                remote.name
            ].get("description", ""),
            app_icon=current_app.config["OAUTHCLIENT_REMOTE_APPS"][remote.name].get(
                "icon", None
            ),
        )
    except OAuthClientUnAuthorized:
        # Redirect the user after registration (which doesn't include the
        # activation), waiting for user to confirm his email.
        return redirect(url_for("security.login"))


@oauth_resp_remote_error_handler
def authorized_signup_handler(resp, remote, *args, **kwargs):
    """Handle sign-in/up functionality.

    :param remote: The remote application.
    :param resp: The response.
    :returns: Redirect response.
    """
    next_url = base_authorized_signup_handler(resp, remote, *args, **kwargs)
    # Redirect to next
    if next_url:
        return redirect(next_url)

    return redirect(url_for("invenio_oauthclient_settings.index"))


def base_authorized_signup_handler(resp, remote, *args, **kwargs):
    """Handle sign-in/up functionality.

    :param remote: The remote application.
    :param resp: The response.
    :returns: Redirect response.
    """
    # Remove any previously stored auto register session key
    session.pop(token_session_key(remote.name) + "_autoregister", None)

    # Store token in session
    # ----------------------
    # Set token in session - token object only returned if
    # current_user.is_autenticated().
    token = response_token_setter(remote, resp)
    handlers = current_oauthclient.signup_handlers[remote.name]

    # Sign-in/up user
    # ---------------
    if not current_user.is_authenticated:
        account_info = handlers["info"](resp)
        account_info_received.send(
            remote, token=token, response=resp, account_info=account_info
        )

        user = oauth_get_user(
            remote.consumer_key,
            account_info=account_info,
            access_token=token_getter(remote)[0],
        )
        user_found = user is not None

        if not user_found:
            # Auto sign-up if user not found
            user_info = account_info["user"]
            username = user_info["username"]
            form = create_csrf_disabled_registrationform(remote)

            form = fill_form(form, account_info["user"])
            if not form.validate() or get_user_by_username(username) is not None:
                # if the 'preferred_username' wasn't valid or already taken,
                # try to auto-generate a valid and unique username
                account_info["user"]["username"] = create_username_from_info(user_info)
                form = fill_form(form, account_info["user"])

            remote_apps = current_app.config["OAUTHCLIENT_REMOTE_APPS"]
            precedence_mask = remote_apps[remote.name].get("precedence_mask")
            user = oauth_register(form, account_info["user"], precedence_mask)

            # if registration fails ...
            if user is None:
                # requires extra information
                session[token_session_key(remote.name) + "_autoregister"] = True
                session[token_session_key(remote.name) + "_account_info"] = account_info
                session[token_session_key(remote.name) + "_response"] = resp
                db.session.commit()
                raise OAuthClientMustRedirectSignup()

            else:
                # auto-trust new users, if they meet the configured criteria
                # NOTE: this was moved here from ext.py (as a handler for the
                # flask_security.signals.user_registered signal), because that
                # didn't quite work with a containerized setup...
                auto_trust_user(user)

        # Authenticate user
        if not oauth_authenticate(
            remote.consumer_key, user, require_existing_link=False
        ):
            raise OAuthClientUnAuthorized()

        if user_found:
            # the user already exists: update their details!
            user_info = account_info.get("user", {})
            new_email = user_info.get("email", user.email)
            new_profile = user_info.get("user_profile", {})
            new_full_name = new_profile.get("full_name")

            if user.email != new_email:
                user.email = new_email

                # our usernames are based on the users' email addresses;
                # thus, we need to update the username if the email address changes
                user.username = create_username_from_info(user_info)

            # update the full name if it has changed
            old_profile = user.user_profile or {}
            if new_full_name and new_full_name != user.user_profile["full_name"]:
                user.user_profile = {"full_name": new_full_name, **old_profile}

        # Link account
        # ------------
        # Need to store token in database instead of only the session when
        # called first time.
        token = response_token_setter(remote, resp)

    # Setup account
    # -------------
    if not token.remote_account.extra_data:
        account_setup = handlers["setup"](token, resp)
        account_setup_received.send(
            remote, token=token, response=resp, account_setup=account_setup
        )
        db.session.commit()
        account_setup_committed.send(remote, token=token)
    else:
        db.session.commit()

    # Redirect to next
    next_url = get_session_next_url(remote.name)
    if next_url:
        return next_url
