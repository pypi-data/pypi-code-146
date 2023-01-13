# SPDX-FileCopyrightText: 2023 Gabriele Pongelli
#
# SPDX-License-Identifier: MIT

"""Main module."""
import logging
from typing import List

import requests
from requests_html import HTMLSession


def _fetch_tags(package: str, version: str) -> List:
    """Fetch available docker tags.

    Arguments:
        package: package name to be fetched, default to python
        version: python's version to fetch docker images

    Returns:
        list of docker imaged of package at that version
    """
    _names = []

    _next_page = True
    _page = 1
    while _next_page:
        logging.debug("Fetching docker tags for %s %s , page %s", package, version, _page)
        result = requests.get(
            f"https://registry.hub.docker.com/v2/repositories/library/{package}/tags?" f"name={version}&page={_page}",
            timeout=120,
        )
        _json = result.json()
        if not _json['next']:
            _next_page = False
        _page += 1
        _names.extend([r["name"] for r in _json['results']])

    return _names


def _configure_logger(level):
    """Configure logger facility from server or client in same way, changing only the output file.

    Arguments:
        level: level of logging facility
    """
    # configure logging
    _log_level = logging.INFO
    if level.lower() == 'debug':
        _log_level = logging.DEBUG
    elif level.lower() == 'warning':
        _log_level = logging.WARNING
    elif level.lower() == 'error':
        _log_level = logging.ERROR

    logging.basicConfig(
        level=_log_level,
        format='%(asctime)s [%(levelname)s - %(filename)s:%(lineno)d]    %(message)s',
        handlers=None,
    )


def get_active_python_versions(docker_images=False, log_level='INFO') -> List[dict]:  # pylint: disable=too-many-locals
    """Get active python versions.

    Arguments:
        docker_images: flag to return also available docker images
        log_level: string indicating log level on stdout

    Returns:
        dict containing all information of active python versions.
    """
    _configure_logger(log_level)
    versions = []
    version_table_selector = "#status-of-python-versions table"

    _r = HTMLSession().get("https://devguide.python.org/versions/")
    version_table = _r.html.find(version_table_selector, first=True)

    # match development information with the latest downloadable release
    _py_specific_release = ".download-list-widget li"
    _r = HTMLSession().get("https://www.python.org/downloads/")
    spec_table = _r.html.find(_py_specific_release)
    _downloadable_versions = [li.find('span a', first=True).text.split(' ')[1] for li in spec_table]

    for ver in version_table.find("tbody tr"):
        branch, _, _, first_release, end_of_life, _ = [v.text for v in ver.find("td")]

        logging.debug("Found Python branch: %s", branch)
        _matching_version = list(
            filter(lambda d: d.startswith(branch), _downloadable_versions)  # pylint: disable=cell-var-from-loop
        )
        _latest_sw = branch
        if _matching_version:
            _latest_sw = _matching_version[0]

        _d = {"version": branch, "latest_sw": _latest_sw, "start": first_release, "end": end_of_life}
        if docker_images:
            _d['docker_images'] = _fetch_tags('python', _latest_sw)

        versions.append(_d)

    return versions
