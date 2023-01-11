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


class LayerOptions:
    root: Optional[str]
    
    def __init__(
        self,
        root: Optional[str] = None,
    ):
        self.root = root


class Layer:
    area_model_name: str
    layer_model_name: str
    number_of_min_entries: int
    number_of_max_entries: int
    height: int
    created_at: int
    root: Optional[str] = None

    def __init__(
        self,
        area_model_name: str,
        layer_model_name: str,
        number_of_min_entries: int,
        number_of_max_entries: int,
        height: int,
        created_at: int,
        options: Optional[LayerOptions] = None,
    ):
        self.area_model_name = area_model_name
        self.layer_model_name = layer_model_name
        self.number_of_min_entries = number_of_min_entries
        self.number_of_max_entries = number_of_max_entries
        self.height = height
        self.created_at = created_at
        self.root = options.root if options.root else None

    def properties(
        self,
    ) -> Dict[str, Any]:
        properties: Dict[str, Any] = {}

        if self.properties is not None:
            properties["areaModelName"] = self.area_model_name
        if self.properties is not None:
            properties["layerModelName"] = self.layer_model_name
        if self.properties is not None:
            properties["root"] = self.root
        if self.properties is not None:
            properties["numberOfMinEntries"] = self.number_of_min_entries
        if self.properties is not None:
            properties["numberOfMaxEntries"] = self.number_of_max_entries
        if self.properties is not None:
            properties["height"] = self.height
        if self.properties is not None:
            properties["createdAt"] = self.created_at

        return properties
