"""Provide login CLI command."""

import argparse
import os
from getpass import getpass
from pathlib import Path

from spotter.api import ApiClient
from spotter.storage import Storage


def add_parser(subparsers: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
    """
    Add a new parser for login command to subparsers.

    :param subparsers: Subparsers action
    """
    parser = subparsers.add_parser(
        "login", help="Log in to Steampunk Spotter user account"
    )
    parser.add_argument(
        "--username", "-u", type=str, help="Steampunk Spotter username"
    )
    parser.add_argument(
        "--password", "-p", type=str, help="Steampunk Spotter password"
    )
    parser.set_defaults(func=_parser_callback)


def _parser_callback(args: argparse.Namespace) -> None:
    """
    Execute callback for login command.

    :param args: Argparse arguments
    """
    api_endpoint = os.environ.get("SPOTTER_ENDPOINT", "")
    storage_path = args.storage_path or Storage.DEFAULT_PATH
    username = args.username or os.environ.get("SPOTTER_USERNAME") or input("Username: ")
    password = args.password or os.environ.get("SPOTTER_PASSWORD") or getpass()

    login(api_endpoint, storage_path, username, password)
    print("Login successful!")


def login(api_endpoint: str, storage_path: Path, username: str, password: str) -> None:
    """
    Do user login.

    :param api_endpoint: Steampunk Spotter API endpoint
    :param storage_path: Path to storage
    :param username: Steampunk Spotter username
    :param password: Steampunk Spotter password
    """
    storage = Storage(storage_path)

    # TODO: extract this to a separate configuration component along with other configuration file options
    if not api_endpoint:
        if storage.exists("spotter.json"):
            storage_configuration_json = storage.read_json("spotter.json")
            api_endpoint = storage_configuration_json.get("endpoint", ApiClient.DEFAULT_ENDPOINT)
        else:
            api_endpoint = ApiClient.DEFAULT_ENDPOINT

    api_client = ApiClient(api_endpoint, storage, username, password)
    api_client.login()
