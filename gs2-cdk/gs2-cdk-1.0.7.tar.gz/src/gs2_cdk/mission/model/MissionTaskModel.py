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
from ...core.model import AcquireAction
from .options.MissionTaskModelOptions import MissionTaskModelOptions


class MissionTaskModel:
    name: str
    counter_name: str
    target_value: int
    metadata: Optional[str] = None
    complete_acquire_actions: Optional[List[AcquireAction]] = None
    challenge_period_event_id: Optional[str] = None
    premise_mission_task_name: Optional[str] = None

    def __init__(
        self,
        name: str,
        counter_name: str,
        target_value: int,
        options: Optional[MissionTaskModelOptions] = MissionTaskModelOptions(),
    ):
        self.name = name
        self.counter_name = counter_name
        self.target_value = target_value
        self.metadata = options.metadata if options.metadata else None
        self.complete_acquire_actions = options.complete_acquire_actions if options.complete_acquire_actions else None
        self.challenge_period_event_id = options.challenge_period_event_id if options.challenge_period_event_id else None
        self.premise_mission_task_name = options.premise_mission_task_name if options.premise_mission_task_name else None

    def properties(
        self,
    ) -> Dict[str, Any]:
        properties: Dict[str, Any] = {}

        if self.name is not None:
            properties["name"] = self.name
        if self.metadata is not None:
            properties["metadata"] = self.metadata
        if self.counter_name is not None:
            properties["counterName"] = self.counter_name
        if self.target_value is not None:
            properties["targetValue"] = self.target_value
        if self.complete_acquire_actions is not None:
            properties["completeAcquireActions"] = [
                v.properties(
                )
                for v in self.complete_acquire_actions
            ]
        if self.challenge_period_event_id is not None:
            properties["challengePeriodEventId"] = self.challenge_period_event_id
        if self.premise_mission_task_name is not None:
            properties["premiseMissionTaskName"] = self.premise_mission_task_name

        return properties
