import re

import pydantic

from classiq.interface._version import VERSION


def _make_version_regex() -> str:
    """
    This regex should match any version that has the same major and minor parts as the
    current one.
    This is so that the VersionedModel would accept objects created by versions with
    a different patch part.
    """
    match = re.match(r"(\d+)\.(\d+)\.(\d+).*", VERSION)
    if match is None:
        raise RuntimeError(f"Version {VERSION} is invalid")
    major, minor = match.group(1), match.group(2)
    return rf"^{major}\.{minor}\."


class VersionedModel(pydantic.BaseModel, extra=pydantic.Extra.forbid):
    version: str = pydantic.Field(default=VERSION, regex=_make_version_regex())
