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

from ...core.func import GetAttr, Join
from .MissionGroupModelRef import MissionGroupModelRef
from .CounterModelRef import CounterModelRef
from ..stamp_sheet.IncreaseCounterByUserId import IncreaseCounterByUserId
from ..stamp_sheet.ReceiveByUserId import ReceiveByUserId


class NamespaceRef:
    namespace_name: str

    def __init__(
        self,
        namespace_name: str,
    ):
        self.namespace_name = namespace_name

    def mission_group_model(
        self,
        mission_group_name: str,
    ) -> MissionGroupModelRef:
        return MissionGroupModelRef(
            self.namespace_name,
            mission_group_name,
        )

    def counter_model(
        self,
        counter_name: str,
    ) -> CounterModelRef:
        return CounterModelRef(
            self.namespace_name,
            counter_name,
        )

    def increase_counter(
        self,
        counter_name: str,
        value: int,
        user_id: Optional[str] = "#{userId}",
    ) -> IncreaseCounterByUserId:
        return IncreaseCounterByUserId(
            self.namespace_name,
            counter_name,
            value,
            user_id,
        )

    def receive(
        self,
        mission_group_name: str,
        mission_task_name: str,
        user_id: Optional[str] = "#{userId}",
    ) -> ReceiveByUserId:
        return ReceiveByUserId(
            self.namespace_name,
            mission_group_name,
            mission_task_name,
            user_id,
        )

    def grn(
        self,
    ) -> str:
        return Join(
            ":",
            [
                "grn",
                "gs2",
                GetAttr.region(
                ).str(
                ),
                GetAttr.owner_id(
                ).str(
                ),
                "mission",
                self.namespace_name,
            ],
        ).str(
        )
