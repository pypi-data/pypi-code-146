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
from .options.CounterScopeModelOptions import CounterScopeModelOptions
from .options.CounterScopeModelResetTypeIsNotResetOptions import CounterScopeModelResetTypeIsNotResetOptions
from .options.CounterScopeModelResetTypeIsDailyOptions import CounterScopeModelResetTypeIsDailyOptions
from .options.CounterScopeModelResetTypeIsWeeklyOptions import CounterScopeModelResetTypeIsWeeklyOptions
from .options.CounterScopeModelResetTypeIsMonthlyOptions import CounterScopeModelResetTypeIsMonthlyOptions
from .enum.CounterScopeModelResetType import CounterScopeModelResetType
from .enum.CounterScopeModelResetDayOfWeek import CounterScopeModelResetDayOfWeek


class CounterScopeModel:
    reset_type: CounterScopeModelResetType
    reset_day_of_month: Optional[int] = None
    reset_day_of_week: Optional[CounterScopeModelResetDayOfWeek] = None
    reset_hour: Optional[int] = None

    def __init__(
        self,
        reset_type: CounterScopeModelResetType,
        options: Optional[CounterScopeModelOptions] = CounterScopeModelOptions(),
    ):
        self.reset_type = reset_type
        self.reset_day_of_month = options.reset_day_of_month if options.reset_day_of_month else None
        self.reset_day_of_week = options.reset_day_of_week if options.reset_day_of_week else None
        self.reset_hour = options.reset_hour if options.reset_hour else None

    @staticmethod
    def reset_type_is_not_reset(
        options: Optional[CounterScopeModelResetTypeIsNotResetOptions] = CounterScopeModelResetTypeIsNotResetOptions(),
    ) -> CounterScopeModel:
        return CounterScopeModel(
            CounterScopeModelResetType.NOT_RESET,
            CounterScopeModelOptions(
            ),
        )

    @staticmethod
    def reset_type_is_daily(
        reset_hour: int,
        options: Optional[CounterScopeModelResetTypeIsDailyOptions] = CounterScopeModelResetTypeIsDailyOptions(),
    ) -> CounterScopeModel:
        return CounterScopeModel(
            CounterScopeModelResetType.DAILY,
            CounterScopeModelOptions(
                reset_hour,
            ),
        )

    @staticmethod
    def reset_type_is_weekly(
        reset_day_of_week: CounterScopeModelResetDayOfWeek,
        reset_hour: int,
        options: Optional[CounterScopeModelResetTypeIsWeeklyOptions] = CounterScopeModelResetTypeIsWeeklyOptions(),
    ) -> CounterScopeModel:
        return CounterScopeModel(
            CounterScopeModelResetType.WEEKLY,
            CounterScopeModelOptions(
                reset_day_of_week,
                reset_hour,
            ),
        )

    @staticmethod
    def reset_type_is_monthly(
        reset_day_of_month: int,
        reset_hour: int,
        options: Optional[CounterScopeModelResetTypeIsMonthlyOptions] = CounterScopeModelResetTypeIsMonthlyOptions(),
    ) -> CounterScopeModel:
        return CounterScopeModel(
            CounterScopeModelResetType.MONTHLY,
            CounterScopeModelOptions(
                reset_day_of_month,
                reset_hour,
            ),
        )

    def properties(
        self,
    ) -> Dict[str, Any]:
        properties: Dict[str, Any] = {}

        if self.reset_type is not None:
            properties["resetType"] = self.reset_type.value
        if self.reset_day_of_month is not None:
            properties["resetDayOfMonth"] = self.reset_day_of_month
        if self.reset_day_of_week is not None:
            properties["resetDayOfWeek"] = self.reset_day_of_week.value
        if self.reset_hour is not None:
            properties["resetHour"] = self.reset_hour

        return properties
