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
from .options.ScopedValueOptions import ScopedValueOptions
from .enum.ScopedValueResetType import ScopedValueResetType


class ScopedValue:
    reset_type: ScopedValueResetType
    value: int
    updated_at: int
    next_reset_at: Optional[int] = None

    def __init__(
        self,
        reset_type: ScopedValueResetType,
        value: int,
        updated_at: int,
        options: Optional[ScopedValueOptions] = ScopedValueOptions(),
    ):
        self.reset_type = reset_type
        self.value = value
        self.updated_at = updated_at
        self.next_reset_at = options.next_reset_at if options.next_reset_at else None

    def properties(
        self,
    ) -> Dict[str, Any]:
        properties: Dict[str, Any] = {}

        if self.reset_type is not None:
            properties["resetType"] = self.reset_type.value
        if self.value is not None:
            properties["value"] = self.value
        if self.next_reset_at is not None:
            properties["nextResetAt"] = self.next_reset_at
        if self.updated_at is not None:
            properties["updatedAt"] = self.updated_at

        return properties
