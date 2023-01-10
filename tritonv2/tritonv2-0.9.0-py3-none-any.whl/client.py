# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
triton client package
"""


class TritonClient(object):
    """
    TritonClient is a wrapper class for TritonClient
    """
    def __init__(self):
        """
        Constructor
        """
        self._client = None
