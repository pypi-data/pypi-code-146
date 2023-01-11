# pylint: disable=missing-module-docstring
from collections import namedtuple

Version = namedtuple(
    "Version",
    [
        "url",
        "version_id",
        "valid_from",
        "valid_to",
        "last_modified",
    ],
)

Correspondence = namedtuple(
    "Correspondence",
    [
        "url",
        "correspondence_id",
        "source_version_id",
        "target_version_id",
        "last_modified",
    ],
)
