# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it
# and/or modify it under the terms of the MIT License; see LICENSE
# file for more details.

"""API functions of the campusonline connector."""
from typing import Callable
from xml.etree.ElementTree import fromstring

from requests import post

from .types import (
    URL,
    CampusOnlineConfigs,
    CampusOnlineID,
    CampusOnlineToken,
    ThesesFilter,
    ThesesState,
)
from .utils import (
    create_request_body_ids,
    create_request_header,
    download_file,
    get_metadata,
)


def import_from_campusonline(
    import_func: Callable, cms_id: CampusOnlineID, configs: CampusOnlineConfigs
):
    """Import record from campusonline."""
    return import_func(cms_id, configs, get_metadata, download_file)


def fetch_all_ids(
    endpoint: URL, token: CampusOnlineToken, theses_filters: ThesesFilter = None
) -> list[tuple[CampusOnlineID, ThesesState]]:
    """Fetch to import ids."""
    ids = []
    for theses_filter, state in theses_filters:
        body = create_request_body_ids(token, theses_filter)

        headers = create_request_header("getAllThesesMetadataRequest")
        response = post(endpoint, data=body, headers=headers)

        root = fromstring(response.text)
        xpath = "{http://www.campusonline.at/thesisservice/basetypes}ID"
        ids += [(CampusOnlineID(node.text), state) for node in root.iter(xpath)]
    return ids
