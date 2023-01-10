from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Dict, Optional

import httpx
import pydantic
from packaging.version import Version
from pydantic import BaseModel

from classiq.exceptions import ClassiqAPIError

if TYPE_CHECKING:
    from classiq._internals.client import Client

_VERSION_UPDATE_SUGGESTION = 'Please run "pip install -U classiq" to upgrade the classiq SDK to the latest version.'
_logger = logging.getLogger(__name__)


class HostVersions(BaseModel):
    classiq_interface: pydantic.StrictStr = pydantic.Field()


class DeprecationInfo(BaseModel):
    deprecation_date: datetime = pydantic.Field()
    removal_date: datetime = pydantic.Field()


class GlobalVersions(BaseModel):
    deprecated: Dict[str, DeprecationInfo] = pydantic.Field()


class HostChecker:
    _UNKNOWN_VERSION = "0.0.0"

    def __init__(self, client: Client, client_version: str):
        self._client = client
        self._client_version = client_version

    def _get_host_version(self) -> str:
        host = HostVersions.parse_obj(self._client.sync_call_api("get", "/versions"))
        return host.classiq_interface

    def _get_deprecation_info(self) -> Optional[DeprecationInfo]:
        global_versions = GlobalVersions.parse_obj(
            self._client.sync_call_api("get", "/versions", use_versioned_url=False)
        )
        return global_versions.deprecated.get(self._client_version, None)

    @classmethod
    def _check_matching_versions(cls, lhs_version: str, rhs_version: str) -> bool:
        if lhs_version == cls._UNKNOWN_VERSION or rhs_version == cls._UNKNOWN_VERSION:
            # In case one of those versions is unknown, they are considered equal
            _logger.debug(
                "Either {} or {} is an unknown version. Assuming both versions are equal.",
                lhs_version,
                rhs_version,
            )
            return True
        processed_lhs = Version(lhs_version)
        processed_rhs = Version(rhs_version)
        return processed_lhs.release[:2] == processed_rhs.release[:2]

    def check_host_version(self) -> None:
        try:
            raw_host_version = self._get_host_version()
        except httpx.ConnectError:
            _logger.warning(
                "Version check failed - host unavailable.",
            )
        else:
            if not self._check_matching_versions(
                raw_host_version, self._client_version
            ):
                raise ClassiqAPIError(
                    f"Classiq API version mismatch: 'classiq' version is "
                    f"{self._client_version}, backend version is {raw_host_version}. {_VERSION_UPDATE_SUGGESTION}"
                )

    def check_deprecated_version(self) -> None:
        try:
            deprecation_info = self._get_deprecation_info()
        except httpx.ConnectError:
            _logger.warning(
                "Deprecation check failed - host unavailable.",
            )
        else:
            if deprecation_info is None:
                return
            _logger.warning(
                "The current version of 'classiq' has been deprecated, and will not be supported as of %s. %s",
                deprecation_info.removal_date.date(),
                _VERSION_UPDATE_SUGGESTION,
            )
