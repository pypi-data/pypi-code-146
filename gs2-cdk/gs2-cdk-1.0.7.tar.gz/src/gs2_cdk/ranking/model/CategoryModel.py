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
from .options.CategoryModelOptions import CategoryModelOptions
from .options.CategoryModelScopeIsGlobalOptions import CategoryModelScopeIsGlobalOptions
from .options.CategoryModelScopeIsScopedOptions import CategoryModelScopeIsScopedOptions
from .enum.CategoryModelOrderDirection import CategoryModelOrderDirection
from .enum.CategoryModelScope import CategoryModelScope


class CategoryModel:
    name: str
    order_direction: CategoryModelOrderDirection
    scope: CategoryModelScope
    unique_by_user_id: bool
    metadata: Optional[str] = None
    minimum_value: Optional[int] = None
    maximum_value: Optional[int] = None
    calculate_fixed_timing_hour: Optional[int] = None
    calculate_fixed_timing_minute: Optional[int] = None
    calculate_interval_minutes: Optional[int] = None
    entry_period_event_id: Optional[str] = None
    access_period_event_id: Optional[str] = None
    generation: Optional[str] = None

    def __init__(
        self,
        name: str,
        order_direction: CategoryModelOrderDirection,
        scope: CategoryModelScope,
        unique_by_user_id: bool,
        options: Optional[CategoryModelOptions] = CategoryModelOptions(),
    ):
        self.name = name
        self.order_direction = order_direction
        self.scope = scope
        self.unique_by_user_id = unique_by_user_id
        self.metadata = options.metadata if options.metadata else None
        self.minimum_value = options.minimum_value if options.minimum_value else None
        self.maximum_value = options.maximum_value if options.maximum_value else None
        self.calculate_fixed_timing_hour = options.calculate_fixed_timing_hour if options.calculate_fixed_timing_hour else None
        self.calculate_fixed_timing_minute = options.calculate_fixed_timing_minute if options.calculate_fixed_timing_minute else None
        self.calculate_interval_minutes = options.calculate_interval_minutes if options.calculate_interval_minutes else None
        self.entry_period_event_id = options.entry_period_event_id if options.entry_period_event_id else None
        self.access_period_event_id = options.access_period_event_id if options.access_period_event_id else None
        self.generation = options.generation if options.generation else None

    @staticmethod
    def scope_is_global(
        name: str,
        order_direction: CategoryModelOrderDirection,
        unique_by_user_id: bool,
        calculate_interval_minutes: int,
        options: Optional[CategoryModelScopeIsGlobalOptions] = CategoryModelScopeIsGlobalOptions(),
    ) -> CategoryModel:
        return CategoryModel(
            name,
            order_direction,
            CategoryModelScope.GLOBAL,
            unique_by_user_id,
            CategoryModelOptions(
                calculate_interval_minutes,
                options.metadata,
                options.minimum_value,
                options.maximum_value,
                options.calculate_fixed_timing_hour,
                options.calculate_fixed_timing_minute,
                options.entry_period_event_id,
                options.access_period_event_id,
                options.generation,
            ),
        )

    @staticmethod
    def scope_is_scoped(
        name: str,
        order_direction: CategoryModelOrderDirection,
        unique_by_user_id: bool,
        options: Optional[CategoryModelScopeIsScopedOptions] = CategoryModelScopeIsScopedOptions(),
    ) -> CategoryModel:
        return CategoryModel(
            name,
            order_direction,
            CategoryModelScope.SCOPED,
            unique_by_user_id,
            CategoryModelOptions(
                options.metadata,
                options.minimum_value,
                options.maximum_value,
                options.calculate_fixed_timing_hour,
                options.calculate_fixed_timing_minute,
                options.entry_period_event_id,
                options.access_period_event_id,
                options.generation,
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
        if self.minimum_value is not None:
            properties["minimumValue"] = self.minimum_value
        if self.maximum_value is not None:
            properties["maximumValue"] = self.maximum_value
        if self.order_direction is not None:
            properties["orderDirection"] = self.order_direction.value
        if self.scope is not None:
            properties["scope"] = self.scope.value
        if self.unique_by_user_id is not None:
            properties["uniqueByUserId"] = self.unique_by_user_id
        if self.calculate_fixed_timing_hour is not None:
            properties["calculateFixedTimingHour"] = self.calculate_fixed_timing_hour
        if self.calculate_fixed_timing_minute is not None:
            properties["calculateFixedTimingMinute"] = self.calculate_fixed_timing_minute
        if self.calculate_interval_minutes is not None:
            properties["calculateIntervalMinutes"] = self.calculate_interval_minutes
        if self.entry_period_event_id is not None:
            properties["entryPeriodEventId"] = self.entry_period_event_id
        if self.access_period_event_id is not None:
            properties["accessPeriodEventId"] = self.access_period_event_id
        if self.generation is not None:
            properties["generation"] = self.generation

        return properties
