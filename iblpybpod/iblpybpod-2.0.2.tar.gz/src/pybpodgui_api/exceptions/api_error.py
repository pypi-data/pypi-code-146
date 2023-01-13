# !/usr/bin/python3
# -*- coding: utf-8 -*-


class APIError(Exception):
    """

    """

    def __init__(self, value, original_exception=None):
        self.value = value
        self.original_exception = original_exception

    def __str__(self):
        return self.value
