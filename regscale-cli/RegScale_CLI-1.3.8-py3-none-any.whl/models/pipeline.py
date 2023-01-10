#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" standard python imports """
from dataclasses import dataclass


@dataclass
class Pipeline:
    """Pipeline Model"""

    email: str  # Required
    fullName: str = None
    pipelines: any = None
    totalTasks: int = None
    analyzed: bool = False
    emailed: bool = False

    def __getitem__(self, key):
        """get attribute"""
        return getattr(self, key)

    def __setitem__(self, key, value):
        """set attribute"""
        return setattr(self, key, value)

    @staticmethod
    def xstr(str_eval: str) -> str:
        """String None to Empty

        Args:
            str_eval (str): String

        Returns:
            str: Empty or String
        """
        if str_eval is None:
            return ""
        return str(str_eval)
