import re
from urllib.parse import urlparse

from cerberus import Validator

from powerstrip.utils import SemVer


class CustomValidator(Validator):
    """
    custom validator with extended checks
    """
    def _check_with_is_semver(self, field: str, value: str):
        """
        checks if value is a valid SemVer

        => see https://semver.org
        """
        try:
            SemVer.create_from_str(value)

        except TypeError as e:
            self._error(field, f"{e}")

    def _check_with_is_url(self, field: str, value: str):
        """
        checks if value is a valid URL
        """
        if not value.endswith("/"):
            # ensure that URL ends with a path, i.e., if not
            # existing simply add it
            value += "/"

        res = urlparse(value)
        if not all([res.scheme, res.netloc, res.path]):
            # URL parts are missing
            self._error(field, f"Invalid URL '{value}'!")

    def _check_with_is_alphanumeric(self, field: str, value: str):
        """
        checks if value is a alphanumeric value or includes one of: _, -, .
        """
        res = re.compile(r"^[A-Za-z0-9._-]+$").match(value)
        if not res:
            self._error(field, f"Invalid alphanumeric string '{value}'!")

    def _check_with_is_hex(self, field: str, value: str):
        """
        checks if value is a hex value
        """
        res = re.compile(r"^[A-Fa-f0-9]+$").match(value)
        if not res:
            self._error(field, f"Invalid hex string '{value}'!")

    def _check_with_is_author(self, field: str, value: str):
        """
        checks if value is a author value of the format
        Firstname Lastname <email@example.com>
        """
        res = re.compile(r'^(?:"?([^"]*)"?\s)?(?:<?(.+@[^>]+)>?)$').match(value)
        if not res:
            self._error(field, f"Invalid author '{value}'!")

    def _check_with_is_list(self, field: str, value: str):
        """
        checks if value is a  valid list
        """
        if value in ("", None):
            # ignore not set list
            return

        li = value.split(",")
        if not all(li):
            self._error(field, f"Invalid list '{value}'!")
