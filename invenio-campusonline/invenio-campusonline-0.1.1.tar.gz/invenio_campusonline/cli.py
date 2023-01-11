# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Command line interface to interact with the CampusOnline-Connector module."""


import click
from click_params import URL
from flask import current_app
from flask.cli import with_appcontext

from .api import fetch_all_ids, import_from_campusonline
from .types import CampusOnlineConfigs


@click.group()
def campusonline():
    """Campusonline CLI."""


@campusonline.command()
@with_appcontext
@click.option("--endpoint", type=URL)
@click.option("--campusonline-id", type=click.STRING)
@click.option("--token", type=click.STRING)
@click.option("--user-email", type=click.STRING, default="cms@tugraz.at")
def import_thesis(endpoint, campusonline_id, token, user_email):
    """Import metadata and file (aka one thesis) from campusonline."""
    import_func = current_app.config["CAMPUSONLINE_IMPORT_FUNC"]
    theses_filters = current_app.config["CAMPUSONLINE_THESES_FILTERS"]
    recipients = current_app.config["CAMPUSONLINE_ERROR_MAIL_RECIPIENTS"]
    sender = current_app.config["CAMPUSONLINE_ERROR_MAIL_SENDER"]

    configs = CampusOnlineConfigs(
        endpoint, token, user_email, theses_filters, recipients, sender
    )
    record = import_from_campusonline(import_func, campusonline_id, configs)

    current_app.logger.info(f"record.id: {record.id}")


@campusonline.command()
@with_appcontext
@click.option("--endpoint", type=URL)
@click.option("--token", type=click.STRING)
def fetch_ids(endpoint, token):
    """Fetch all to import ids."""
    theses_filters = current_app.config["CAMPUSONLINE_THESES_FILTERS"]
    ids = fetch_all_ids(endpoint, token, theses_filters)

    current_app.logger.info(ids)
