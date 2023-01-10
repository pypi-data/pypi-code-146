# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
triton client constants
"""
from __future__ import annotations

from typing import List

from pydantic import BaseModel

GRPC_SERVICE = "inference.GRPCInferenceService"

class NameItem(BaseModel):
    service: str


class RetryPolicy(BaseModel):
    maxAttempts: int
    initialBackoff: str
    maxBackoff: str
    backoffMultiplier: int
    retryableStatusCodes: List[str]


class MethodConfigItem(BaseModel):
    name: List[NameItem]
    retryPolicy: RetryPolicy


class ServiceConfig(BaseModel):
    methodConfig: List[MethodConfigItem]


