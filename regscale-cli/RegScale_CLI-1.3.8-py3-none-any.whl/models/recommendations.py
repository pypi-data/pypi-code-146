#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" standard python imports """
from dataclasses import dataclass, field


@dataclass
class Recommendations:
    """Recommendations Model"""

    id: str  # Required
    data: dict  # Required
    analyzed: bool = False
    created: bool = False

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
