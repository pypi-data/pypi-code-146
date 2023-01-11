# Copyright 2016- Game Server Services, Inc. or its affiliates. All Rights
# Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.
from __future__ import annotations
from typing import *
from .Version import Version
from .options.VersionModelOptions import VersionModelOptions
from .options.VersionModelScopeIsPassiveOptions import VersionModelScopeIsPassiveOptions
from .options.VersionModelScopeIsActiveOptions import VersionModelScopeIsActiveOptions
from .enum.VersionModelScope import VersionModelScope


class VersionModel:
    name: str
    warning_version: Version
    error_version: Version
    scope: VersionModelScope
    metadata: Optional[str] = None
    current_version: Optional[Version] = None
    need_signature: Optional[bool] = None
    signature_key_id: Optional[str] = None

    def __init__(
        self,
        name: str,
        warning_version: Version,
        error_version: Version,
        scope: VersionModelScope,
        options: Optional[VersionModelOptions] = VersionModelOptions(),
    ):
        self.name = name
        self.warning_version = warning_version
        self.error_version = error_version
        self.scope = scope
        self.metadata = options.metadata if options.metadata else None
        self.current_version = options.current_version if options.current_version else None
        self.need_signature = options.need_signature if options.need_signature else None
        self.signature_key_id = options.signature_key_id if options.signature_key_id else None

    @staticmethod
    def scope_is_passive(
        name: str,
        warning_version: Version,
        error_version: Version,
        need_signature: bool,
        options: Optional[VersionModelScopeIsPassiveOptions] = VersionModelScopeIsPassiveOptions(),
    ) -> VersionModel:
        return VersionModel(
            name,
            warning_version,
            error_version,
            VersionModelScope.PASSIVE,
            VersionModelOptions(
                need_signature,
                options.metadata,
            ),
        )

    @staticmethod
    def scope_is_active(
        name: str,
        warning_version: Version,
        error_version: Version,
        current_version: Version,
        options: Optional[VersionModelScopeIsActiveOptions] = VersionModelScopeIsActiveOptions(),
    ) -> VersionModel:
        return VersionModel(
            name,
            warning_version,
            error_version,
            VersionModelScope.ACTIVE,
            VersionModelOptions(
                current_version,
                options.metadata,
            ),
        )

    def properties(
        self,
    ) -> Dict[str, Any]:
        properties: Dict[str, Any] = {}

        if self.name is not None:
            properties["name"] = self.name
        if self.metadata is not None:
            properties["metadata"] = self.metadata
        if self.warning_version is not None:
            properties["warningVersion"] = self.warning_version.properties(
            )
        if self.error_version is not None:
            properties["errorVersion"] = self.error_version.properties(
            )
        if self.scope is not None:
            properties["scope"] = self.scope.value
        if self.current_version is not None:
            properties["currentVersion"] = self.current_version.properties(
            )
        if self.need_signature is not None:
            properties["needSignature"] = self.need_signature
        if self.signature_key_id is not None:
            properties["signatureKeyId"] = self.signature_key_id

        return properties
