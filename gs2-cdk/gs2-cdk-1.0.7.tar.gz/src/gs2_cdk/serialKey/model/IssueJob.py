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


class IssueJobStatus:
    value: str

    def __init__(
        self,
        value: str,
    ):
        self.value = value


IssueJobStatus.PROCESSING = IssueJobStatus("PROCESSING")
IssueJobStatus.COMPLETE = IssueJobStatus("COMPLETE")


class IssueJobOptions:
    metadata: Optional[str]
    
    def __init__(
        self,
        metadata: Optional[str] = None,
    ):
        self.metadata = metadata


class IssueJob:
    name: str
    issued_count: int
    issue_request_count: int
    status: IssueJobStatus
    created_at: int
    metadata: Optional[str] = None

    def __init__(
        self,
        name: str,
        issued_count: int,
        issue_request_count: int,
        status: IssueJobStatus,
        created_at: int,
        options: Optional[IssueJobOptions] = None,
    ):
        self.name = name
        self.issued_count = issued_count
        self.issue_request_count = issue_request_count
        self.status = status
        self.created_at = created_at
        self.metadata = options.metadata if options.metadata else None

    def properties(
        self,
    ) -> Dict[str, Any]:
        properties: Dict[str, Any] = {}

        if self.properties is not None:
            properties["name"] = self.name
        if self.properties is not None:
            properties["metadata"] = self.metadata
        if self.properties is not None:
            properties["issuedCount"] = self.issued_count
        if self.properties is not None:
            properties["issueRequestCount"] = self.issue_request_count
        if self.properties is not None:
            properties["status"] = self.status
        if self.properties is not None:
            properties["createdAt"] = self.created_at

        return properties
