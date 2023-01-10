#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" standard python imports """
from dataclasses import dataclass


@dataclass
class Component:
    """Component Model"""

    title: str
    description: str
    componentType: str
    componentOwnerId: str
    purpose: str = None
    securityPlansId: int = None
    cmmcAssetType: str = None
    createdBy: str = None
    createdById: str = None
    dateCreated: str = None
    lastUpdatedBy: str = None
    lastUpdatedById: str = None
    dateLastUpdated: str = None
    status: str = "Active"
    uuid: str = None
    componentOwner: str = None
    cmmcExclusion: str = False
    id: int = None
    isPublic: str = True

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
