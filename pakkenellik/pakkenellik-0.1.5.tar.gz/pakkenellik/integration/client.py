import io
import json
import os
import re
import sys
from typing import Dict, List, Optional, Union

import requests
from requests.auth import HTTPBasicAuth

# append the path of the
# parent directory
sys.path.append("..")

from ..datawrapper.client import Datawrapper  # type: ignore [attr-defined] # noqa: E402


def read_integrations() -> Dict[str, Dict[str, str]]:
    """Reads integration.json, if the file not exists it will be created

    Return
        (dict): [integration_id] => {
                        "author": Who created the integration
                        "title": Title
                        "url": The url to use in CMS
                        "external_id": id in Multimedia tool
                         extra_meta: different key/vals that is handy to have
                        }
    """
    if os.path.isfile("integrations.json") and os.access("integrations.json", os.R_OK):
        with io.open("integrations.json") as json_file:
            data = json.load(json_file)

    else:
        print("Either file is missing or is not readable, creating file...")
        with io.open("integrations.json", "w") as json_file:
            json_file.write(json.dumps({}))
        data = {}

    return data


def exists_on_server(integration_id: str) -> bool:
    """Checks if the integration exists in integration.json

    integration_id (string): Integration id used

    Return
        (bool): True if id exists in integration.json
    """
    integrations = read_integrations()
    return (
        integration_id in integrations
        and "url" in integrations[integration_id]
        and "external_id" in integrations[integration_id]
    )


def get_request_verb_and_url(integration_id: str) -> List[Union[str, bytes]]:
    """Checks if the integration should be updated or created

    integration_id (string): Integration id used

    Return
        (array): verb and url for updating/creating integration
    """
    integrations = read_integrations()

    if base_url := os.getenv("MM_API_BASE_URL"):
        return (
            [
                "PUT",
                f'{base_url}/{integrations[integration_id]["external_id"]}',
            ]
            if integration_id in integrations
            and "external_id" in integrations[integration_id]
            else ["POST", base_url]
        )
    else:
        raise Exception("MM_API_BASE_URL is not set")


def get_mm_data(integration_id: str) -> Union[Dict[str, str], None]:
    """Get the url and external id for the integration in MM-tools

    integration_id (string): Integration id used

    Return
        (dict): external_id: id in Multimedia tool
                external_url: URL to use in the CMS
    """
    integrations = read_integrations()

    if integration_id in integrations:
        return {
            "url": integrations[integration_id]["url"],
            "external_id": integrations[integration_id]["external_id"],
        }

    return None


def get_integration_id(search_key: str, search_value: str) -> Union[str, None]:
    """Get the integration_id base on key/value pair

    search_key (string): the key to search for
    search_value (string): the value to search for

    Return
        (string): the integration id, None if not found
    """
    integrations = read_integrations()

    return next(
        (
            key
            for key, val in integrations.items()
            if search_key in val and val[search_key] == search_value
        ),
        None,
    )


def save_integration_meta(
    integration_id: str,
    title: str,
    author: str,
    external_url: str,
    external_id: str,
    extra_meta: Dict[str, str],
) -> bool:
    """Save the new integration in itegation.json

    integration_id (str): Integration id used
    title (str): title
    author (str): Who created this masterpiece?
    external_url (str): URL returned from MM-tools
    extra_meta (dict): extra meta information that is nice to have
    """
    integrations = read_integrations()

    meta = {
        "author": author,
        "title": title,
        "url": external_url,
        "external_id": external_id,
    }

    for key, val in extra_meta.items():
        meta[key] = val

    integrations[integration_id] = meta

    try:
        with io.open("integrations.json", "w") as json_file:
            json_file.write(json.dumps(integrations))
    except Exception as ex:
        raise Exception(f"Could not write file, due to: {ex}") from ex

    return True


def create_integration(
    integration_id: str,
    title: str,
    author: str,
    body: str,
    extra_meta: Dict[str, str] = {},
) -> Union[Dict[str, str], None]:
    """Create a new integration in MM-tools

    integration_id (string): Integration id used
    title: title
    author: Who created this masterpiece?
    body: HTML

    Return
        (dict): external_id: id in Multimedia tool
                external_url: URL to use in the CMS
    """

    if os.getenv("INTEGRATIONS_ENABLED", "False") == "False":
        raise Exception(
            """Integrations disabled in env file.
            Set INTEGRATIONS_ENABLED=True and restart Jupyter
            """
        )

    re_http = re.compile(r"^http:")

    username = os.getenv("MM_API_PROD_USERNAME")
    password = os.getenv("MM_API_PROD_PASSWORD")

    if not username or not password:
        raise Exception("Missing username or password")

    response = requests.request(
        *get_request_verb_and_url(integration_id),
        auth=HTTPBasicAuth(username, password),
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": username,
        },
        data=json.dumps(
            {
                "title": title or "",
                "author": author or "Bord4",
                "body": body or "",
            }
        ),
    )

    if not (200 <= response.status_code <= 201):
        raise Exception(f"Unexpected status code: {response.status_code}")

    # If this was just an update, there's nothing left for us to do
    # and the API won't give us any interesting information anyway.
    if exists_on_server(integration_id):
        return get_mm_data(integration_id)

    result = response.json()["body"]
    if not result["id"] or not result["url"]:
        raise Exception("Did not receive ID and URL from Multimedia API")

    external_id = result["id"]
    # The URLs returned by the API will be HTTP, which causes problems in
    # production where articles are served over HTTPS.
    # It seems that these used to be rewritten at run-time, but apparently
    # this is no longer the case.
    external_url = re_http.sub("https:", result["url"])

    saved = save_integration_meta(
        integration_id, title, author, external_url, external_id, extra_meta
    )
    if not saved:
        return None

    print(integration_id, external_url)

    return {"url": external_url, "external_id": external_id}


def create_dw_integration(  # type: ignore[no-any-unimported]
    dw: Datawrapper, integration_id: str, chart_id: str
) -> bool:
    """Creates an MM integration for Datawrapper

    dw: (Datawrapper class): An instance of the Datawrapper class
    integration_id (str): id to the integration
    chart_id (str): id for Datawrapper chart

    Return:
        (bool): Success
    """
    chart_props = dw.chart_properties(chart_id)

    if not chart_props:
        raise Exception("Did not receive chart props code from Datawrapper API")

    title = chart_props["title"] or ""

    try:
        byline = chart_props["metadata"]["describe"]["byline"]
    except KeyError:
        byline = ""

    try:
        iframe_code = chart_props["metadata"]["publish"]["embed-codes"][
            "embed-method-responsive"
        ]
        iframe_code = iframe_code.replace('height="undefined"', 'height="400"')
    except TypeError:
        raise Exception("Did not receive iframe code from Datawrapper API")

    if iframe_code:
        created = create_integration(
            integration_id, title, byline, iframe_code, {"chart_id": chart_id}
        )
        if not created:
            raise Exception("Could not create integration")

    return True


def get_or_create_chart(  # type: ignore[no-any-unimported]
    dw: Datawrapper,
    key: str,
    title: str = "Ny grafikk",
    chart_type: str = "d3-maps-choropleth",
    folder_id: Optional[int] = None,
    copy_from: Optional[str] = None,
) -> str:

    """
    Searches integrations.json for given key and if it exists, returns the chart_id.
    If not, it will create a new chart and return the id or create
    a new based on an existing chart.

        dw: (Datawrapper class): An instance of the Datawrapper class
        key: string: The integration key to search for
        title: string: Title of new chart if created
        chart_type: string: Chart type of new chart. Defaults to d3-maps-choropleth
        folder_id: int: ID number of DW folder to place chart in
        copy_from: string: If given will copy another graf as template and return the
        new id, instead of creating a new from scratch. Chart type and folder
        will be the same.
    Returns:
        str: Chart id
    """

    chart_id = ""
    integrations = read_integrations()

    if key in integrations:
        chart_id = integrations[key]["chart_id"]
        print(f"Chart and integration exists with DW id: {chart_id}")
    elif copy_from:
        chart_id = dw.copy_chart(copy_from)

    else:
        chart = dw.create_chart(title=title, chart_type=chart_type, folder_id=folder_id)
        chart_id = chart["id"]
        print(f"Chart and integration does not exist. Creating with DW id: {chart_id}")
    return chart_id
