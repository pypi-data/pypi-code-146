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


class SerialKeyStatus:
    value: str

    def __init__(
        self,
        value: str,
    ):
        self.value = value


SerialKeyStatus.ACTIVE = SerialKeyStatus("ACTIVE")
SerialKeyStatus.USED = SerialKeyStatus("USED")
SerialKeyStatus.INACTIVE = SerialKeyStatus("INACTIVE")


class SerialKeyOptions:
    metadata: Optional[str]
    used_user_id: Optional[str]
    used_at: Optional[int]
    
    def __init__(
        self,
        metadata: Optional[str] = None,
        used_user_id: Optional[str] = None,
        used_at: Optional[int] = None,
    ):
        self.metadata = metadata
        self.used_user_id = used_user_id
        self.used_at = used_at


class SerialKeyStatusIsActiveOptions:
    metadata: Optional[str]
    used_at: Optional[int]
    
    def __init__(
        self,
        metadata: Optional[str] = None,
        used_at: Optional[int] = None,
    ):
        self.metadata = metadata
        self.used_at = used_at


class SerialKeyStatusIsUsedOptions:
    metadata: Optional[str]
    used_at: Optional[int]
    
    def __init__(
        self,
        metadata: Optional[str] = None,
        used_at: Optional[int] = None,
    ):
        self.metadata = metadata
        self.used_at = used_at


class SerialKeyStatusIsInactiveOptions:
    metadata: Optional[str]
    used_at: Optional[int]
    
    def __init__(
        self,
        metadata: Optional[str] = None,
        used_at: Optional[int] = None,
    ):
        self.metadata = metadata
        self.used_at = used_at


class SerialKey:
    campaign_model_name: str
    code: str
    status: SerialKeyStatus
    created_at: int
    updated_at: int
    metadata: Optional[str] = None
    used_user_id: Optional[str] = None
    used_at: Optional[int] = None

    def __init__(
        self,
        campaign_model_name: str,
        code: str,
        status: SerialKeyStatus,
        created_at: int,
        updated_at: int,
        options: Optional[SerialKeyOptions] = None,
    ):
        self.campaign_model_name = campaign_model_name
        self.code = code
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.metadata = options.metadata if options.metadata else None
        self.used_user_id = options.used_user_id if options.used_user_id else None
        self.used_at = options.used_at if options.used_at else None

    @staticmethod
    def status_is_active(
        campaign_model_name: str,
        code: str,
        created_at: int,
        updated_at: int,
        options: Optional[SerialKeyStatusIsActiveOptions] = None,
    ):
        return SerialKey(
            campaign_model_name,
            code,
            SerialKeyStatus.ACTIVE,
            created_at,
            updated_at,
            SerialKeyOptions(
                options.metadata,
                options.used_at,
            ),
        )

    @staticmethod
    def status_is_used(
        campaign_model_name: str,
        code: str,
        created_at: int,
        updated_at: int,
        used_user_id: str,
        options: Optional[SerialKeyStatusIsUsedOptions] = None,
    ):
        return SerialKey(
            campaign_model_name,
            code,
            SerialKeyStatus.USED,
            created_at,
            updated_at,
            SerialKeyOptions(
                used_user_id,
                options.metadata,
                options.used_at,
            ),
        )

    @staticmethod
    def status_is_inactive(
        campaign_model_name: str,
        code: str,
        created_at: int,
        updated_at: int,
        options: Optional[SerialKeyStatusIsInactiveOptions] = None,
    ):
        return SerialKey(
            campaign_model_name,
            code,
            SerialKeyStatus.INACTIVE,
            created_at,
            updated_at,
            SerialKeyOptions(
                options.metadata,
                options.used_at,
            ),
        )

    def properties(
        self,
    ) -> Dict[str, Any]:
        properties: Dict[str, Any] = {}

        if self.properties is not None:
            properties["campaignModelName"] = self.campaign_model_name
        if self.properties is not None:
            properties["code"] = self.code
        if self.properties is not None:
            properties["metadata"] = self.metadata
        if self.properties is not None:
            properties["status"] = self.status
        if self.properties is not None:
            properties["usedUserId"] = self.used_user_id
        if self.properties is not None:
            properties["createdAt"] = self.created_at
        if self.properties is not None:
            properties["usedAt"] = self.used_at
        if self.properties is not None:
            properties["updatedAt"] = self.updated_at

        return properties
