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
from .LayerModel import LayerModel


class AreaModelOptions:
    metadata: Optional[str]
    layer_models: Optional[List[LayerModel]]
    
    def __init__(
        self,
        metadata: Optional[str] = None,
        layer_models: Optional[List[LayerModel]] = None,
    ):
        self.metadata = metadata
        self.layer_models = layer_models


class AreaModel:
    name: str
    metadata: Optional[str] = None
    layer_models: Optional[List[LayerModel]] = None

    def __init__(
        self,
        name: str,
        options: Optional[AreaModelOptions] = None,
    ):
        self.name = name
        self.metadata = options.metadata if options.metadata else None
        self.layer_models = options.layer_models if options.layer_models else None

    def properties(
        self,
    ) -> Dict[str, Any]:
        properties: Dict[str, Any] = {}

        if self.properties is not None:
            properties["name"] = self.name
        if self.properties is not None:
            properties["metadata"] = self.metadata
        if self.properties is not None:
            properties["layerModels"] = [
                v.properties(
                )
                for v in self.properties
            ]

        return properties
