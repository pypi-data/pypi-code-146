#!/usr/bin/env python3

""" Module for implementation of simplehash canonicalization"""

import argparse
from hashlib import sha256
import sys
from urllib.parse import urlparse, urlunparse

from bencodepy import encode as binary_encode

from requests import RequestException
from requests import get as requests_get
from requests import post as requests_post

DEFAULT_PAGE_SIZE = 10
TIMEOUT = 30

V1_FIELDS = {
    "identity",
    "asset_identity",
    "event_attributes",
    "asset_attributes",
    "operation",
    "behaviour",
    "timestamp_declared",
    "timestamp_accepted",
    "timestamp_committed",
    "principal_accepted",
    "principal_declared",
    "confirmation_status",
    "from",
    "tenant_identity",
}


class SimpleHashError(Exception):
    """Base exception"""


class SimpleHashClientAuthError(SimpleHashError):
    """If either client id or secret, or both are missing"""


class SimpleHashRequestsError(SimpleHashError):
    """HTTP error from requests module"""


class SimpleHashFieldError(SimpleHashError):
    """Incorrect field name in list() method"""


class SimpleHashPendingEventFound(SimpleHashError):
    """If PENDING event found"""


class SimpleHashFieldMissing(SimpleHashError):
    """If essential field is missing"""


def simplehash_exception_handler(
    dummy_type, value, dummy_traceback
):  # pylint: disable=unused-argument # pragma: no cover
    """Suppress traceback"""
    print(value)


sys.excepthook = simplehash_exception_handler


def __check_event(event):
    """Raise exception if any PENDING events found or
    if required keys are missing"""

    missing = V1_FIELDS.difference(event)
    if missing:
        raise SimpleHashFieldMissing(
            f"Event Identity {event['identity']} has missing field(s) {missing}"
        )
    if event["confirmation_status"] not in ("FAILED", "CONFIRMED"):
        raise SimpleHashPendingEventFound(
            f"Event Identity {event['identity']} has illegal "
            f"confirmation status {event['confirmation_status']}"
        )


def redact_event(event):
    """Form an event only containing necessary fields"""
    return {k: event[k] for k in V1_FIELDS}


def __list_events(api_query, auth_token, page_size):
    """GET method (REST) with params string
    Lists events that match the params dictionary.
    If page size is specified return the list of records in batches of page_size
    until next_page_token in response is null.
    If page size is unspecified return up to the internal limit of records.
    (different for each endpoint)
    Args:
        api_query (string): The api_query as returned from the simplehashed event response.
        auth_token (string): authorization token to be able to call the list events api
        page_size (int): page_size
    Returns:
        iterable that lists events
    Raises:
        SimpleHashFieldError: field has incorrect value.
    """

    headers = {
        "Content-Type": "application/json",
    }
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
    api_query += f"&page_size={page_size}"

    params = None
    while True:
        response = requests_get(
            api_query, headers=headers, params=params, timeout=TIMEOUT
        )
        try:
            response.raise_for_status()
        except RequestException as ex:
            raise SimpleHashRequestsError(
                f"Error from upstream getting events {response.text}"
            ) from ex

        data = response.json()

        try:
            events = data["events"]
        except KeyError as ex:
            raise SimpleHashFieldError("No events found") from ex

        for event in events:
            yield event

        page_token = data.get("next_page_token")
        if not page_token:
            break

        params = {"page_token": page_token}


def anchor_events(api_query, auth_token=None, page_size=DEFAULT_PAGE_SIZE):
    """Generate Simplehash for a given set of events canonicalizing then hashing"""

    hasher = sha256()

    # for each event
    for event in __list_events(api_query, auth_token, page_size):

        __check_event(event)

        # only accept the correct fields on the event
        redacted_event = redact_event(event)

        # bencode the event, this orders dictionary keys
        bencoded_event = binary_encode(redacted_event)

        # add the event to the sha256 hash
        hasher.update(bencoded_event)

    # return the complete hash
    return hasher.hexdigest()


def get_auth_token(api_query, client_id, client_secret):
    """
    get_auth_token gets an auth token from an app registration, given its client id and secret
    """

    fqdn = urlparse(api_query)
    url = urlunparse(
        (fqdn.scheme, fqdn.netloc, "archivist/iam/v1/appidp/token", "", "", "")
    )
    params = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    timeout = 10  # seconds
    response = requests_post(url, data=params, timeout=timeout)
    try:
        response.raise_for_status()
    except RequestException as ex:
        raise SimpleHashRequestsError(
            f"Error from upstream getting events {response.text}"
        ) from ex

    data = response.json()

    auth_token = data["access_token"]
    return auth_token


def main():  # pragma: no cover
    """Creates an anchor given the start time, end time and auth token"""

    parser = argparse.ArgumentParser(description="Create simple hash anchor.")

    # auth
    parser.add_argument(
        "--auth-token-file",
        type=str,
        help="filepath to the stored auth token within a file",
    )

    # client id + secret auth
    parser.add_argument(
        "--client-id",
        type=str,
        help="client id for an app registration to gain auth, ignored if --auth-token-file is set",
    )
    parser.add_argument(
        "--client-secret-file",
        type=str,
        help=(
            "filepath to the stored client secret for an app registration to gain auth, ignored "
            "if --auth-token-file is set"
        ),
    )

    parser.add_argument(
        "api_query",
        type=str,
        help=("the api query string in the asset event response."),
    )

    args = parser.parse_args()

    # get auth token
    auth_token = None
    if args.auth_token_file:
        with open(args.auth_token_file, encoding="utf-8") as fd:
            auth_token = str(fd.read()).strip("\n")

    elif args.client_id and args.client_secret_file:
        # we don't have the auth token file, but we have a client id and secret
        # so attempt to get the auth token via client id and secret
        with open(args.client_secret_file, encoding="utf-8") as fd:
            client_secret = str(fd.read()).strip("\n")
            auth_token = get_auth_token(args.api_query, args.client_id, client_secret)

    # auth_token may be None here and this will only work with the publicassets endpoint
    anchor = anchor_events(args.api_query, auth_token=auth_token)
    print(anchor)


if __name__ == "__main__":  # pragma: no cover
    main()
