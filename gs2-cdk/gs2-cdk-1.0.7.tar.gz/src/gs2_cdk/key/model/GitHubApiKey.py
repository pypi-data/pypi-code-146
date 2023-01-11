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
from .options.GitHubApiKeyOptions import GitHubApiKeyOptions


class GitHubApiKey:
    name: str
    api_key: str
    encryption_key_name: str
    created_at: int
    updated_at: int
    description: Optional[str] = None

    def __init__(
        self,
        name: str,
        api_key: str,
        encryption_key_name: str,
        created_at: int,
        updated_at: int,
        options: Optional[GitHubApiKeyOptions] = GitHubApiKeyOptions(),
    ):
        self.name = name
        self.api_key = api_key
        self.encryption_key_name = encryption_key_name
        self.created_at = created_at
        self.updated_at = updated_at
        self.description = options.description if options.description else None

    def properties(
        self,
    ) -> Dict[str, Any]:
        properties: Dict[str, Any] = {}

        if self.name is not None:
            properties["name"] = self.name
        if self.description is not None:
            properties["description"] = self.description
        if self.api_key is not None:
            properties["apiKey"] = self.api_key
        if self.encryption_key_name is not None:
            properties["encryptionKeyName"] = self.encryption_key_name
        if self.created_at is not None:
            properties["createdAt"] = self.created_at
        if self.updated_at is not None:
            properties["updatedAt"] = self.updated_at

        return properties
