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

from ...core.model import CdkResource, Stack
from ...core.func import GetAttr

from ..ref.RoomRef import RoomRef

from .options.RoomOptions import RoomOptions


class Room(CdkResource):
    stack: Stack
    owner_id: str
    namespace_name: str
    name: str
    ip_address: Optional[str] = None
    port: Optional[int] = None
    encryption_key: Optional[str] = None

    def __init__(
        self,
        stack: Stack,
        owner_id: str,
        namespace_name: str,
        name: str,
        options: Optional[RoomOptions] = RoomOptions(),
    ):
        super().__init__(
            "Realtime_Room_" + name
        )

        self.stack = stack
        self.owner_id = owner_id
        self.namespace_name = namespace_name
        self.name = name
        self.ip_address = options.ip_address if options.ip_address else None
        self.port = options.port if options.port else None
        self.encryption_key = options.encryption_key if options.encryption_key else None
        stack.add_resource(
            self,
        )


    def alternate_keys(
        self,
    ):
        return "name"

    def resource_type(
        self,
    ) -> str:
        return "GS2::Realtime::Room"

    def properties(
        self,
    ) -> Dict[str, Any]:
        properties: Dict[str, Any] = {}

        if self.owner_id is not None:
            properties["OwnerId"] = self.owner_id
        if self.namespace_name is not None:
            properties["NamespaceName"] = self.namespace_name
        if self.name is not None:
            properties["Name"] = self.name
        if self.ip_address is not None:
            properties["IpAddress"] = self.ip_address
        if self.port is not None:
            properties["Port"] = self.port
        if self.encryption_key is not None:
            properties["EncryptionKey"] = self.encryption_key

        return properties

    def ref(
        self,
    ) -> RoomRef:
        return RoomRef(
            self.namespace_name,
            self.name,
        )

    def get_attr_room_id(
        self,
    ) -> GetAttr:
        return GetAttr(
            None,
            None,
            "Item.RoomId",
        )
