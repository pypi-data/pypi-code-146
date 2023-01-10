#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" standard python imports """
from dataclasses import dataclass


@dataclass
class Threat:
    """Threat Model"""

    title: str
    threatType: str
    threatOwnerId: str
    dateIdentified: str
    targetType: str
    description: str
    vulnerabilityAnalysis: str
    mitigations: str
    dateCreated: str
    uuid: str = None
    id: int = None
    investigationResults: str = ""
    notes: str = ""
    status: str = "Under Investigation"
    source: str = "Open Source"

    def __getitem__(self, key):
        """getter"""
        return getattr(self, key)

    def __setitem__(self, key, value):
        """setter"""
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
