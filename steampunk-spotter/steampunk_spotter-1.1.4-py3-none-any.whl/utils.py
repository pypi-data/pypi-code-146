"""Provide utility functions that can be used as helpers throughout the code."""

import sys
from typing import Tuple

import pkg_resources


def get_current_cli_version() -> str:
    """
    Retrieve current version of Steampunk Spotter CLI (steampunk-spotter Python package).

    :return: Version string
    """
    try:
        return pkg_resources.get_distribution("steampunk-spotter").version
    except pkg_resources.DistributionNotFound as e:
        print(f"Error when retrieving current steampunk-spotter version: {e}")
        sys.exit(1)


def prompt_yes_no_question(yes_responses: Tuple[str, ...] = ("y", "yes"), no_responses: Tuple[str, ...] = ("n", "no"),
                           case_sensitive: bool = False, default_yes_response: bool = True) -> bool:
    """
    Prompt yes/no dialog and wait for the user to type in the response.

    :param yes_responses: Valid yes responses
    :param no_responses: Valid no responses
    :param case_sensitive: Indicates whether responses are case-sensitive
    :param default_yes_response: Indicates whether the default response is yes or no
    :return: True if users types in yes, False if no
    """
    prompt_message = "Do you want to continue? (Y/n): "
    if not default_yes_response:
        prompt_message = "Do you want to continue? (y/N): "

    check = str(input(prompt_message)).strip()
    if not case_sensitive:
        check = check.lower()

    try:
        if check == "":
            return default_yes_response
        if check in yes_responses:
            return True
        if check in no_responses:
            return False

        print("Invalid input. Please try again.")
        return prompt_yes_no_question(yes_responses, no_responses, case_sensitive, default_yes_response)
    except EOFError as e:
        print(f"Exception occurred: {e}. Please enter valid inputs.")
        return prompt_yes_no_question(yes_responses, no_responses, case_sensitive, default_yes_response)
