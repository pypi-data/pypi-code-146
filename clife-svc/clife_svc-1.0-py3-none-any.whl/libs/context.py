#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'YAnho.wen'
__mtime__ = '2021/12/21'

"""
from contextvars import ContextVar
from typing import Optional

# 申明请求ID变量
request_id: ContextVar[Optional[str]] = ContextVar('Id of request', default="")
