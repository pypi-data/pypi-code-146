# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it
# and/or modify it under the terms of the MIT License; see LICENSE
# file for more details.


"""Celery tasks for `invenio-campusonline`."""
from typing import Callable

from celery import shared_task
from flask import current_app
from flask_mail import Message

from .api import fetch_all_ids, import_from_campusonline
from .types import CampusOnlineConfigs


def config_variables() -> tuple[Callable, CampusOnlineConfigs]:
    """Configuration variables."""
    import_func = current_app.config["CAMPUSONLINE_IMPORT_FUNC"]
    endpoint = current_app.config["CAMPUSONLINE_ENDPOINT"]
    token = current_app.config["CAMPUSONLINE_TOKEN"]
    user_email = current_app.config["CAMPUSONLINE_USER_EMAIL"]
    theses_filters = current_app.config["CAMPUSONLINE_THESES_FILTERS"]
    recipients = current_app.config["CAMPUSONLINE_ERROR_MAIL_RECIPIENTS"]
    sender = current_app.config["CAMPUSONLINE_ERROR_MAIL_SENDER"]

    return import_func, CampusOnlineConfigs(
        endpoint, token, user_email, theses_filters, recipients, sender
    )


@shared_task(ignore_result=True)
def import_theses_from_campusonline() -> None:
    """Import theses from campusonline."""
    import_func, configs = config_variables()
    ids = fetch_all_ids(configs.endpoint, configs.token, configs.theses_filters)

    for cms_id, state in ids:
        try:
            import_from_campusonline(import_func, cms_id, configs)
        except RuntimeError:
            msg = Message(
                "ERROR: importing from campusonline",
                sender=configs.sender,
                recipients=configs.recipients,
                body=f"thesis id: {cms_id}",
            )
            current_app.extensions["mail"].send(msg)
