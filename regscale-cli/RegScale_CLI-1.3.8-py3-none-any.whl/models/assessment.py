#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dataclass for a RegScale assessment """
from dataclasses import dataclass, asdict


@dataclass
class Assessment:
    """Assessment Model"""

    leadAssessorId: str  # Required field
    title: str  # Required field
    assessmentType: str  # Required field
    plannedStart: str  # Required field
    plannedFinish: str  # Required field
    status: str = "Scheduled"  # Required field
    assessmentResult: str = ""
    actualFinish: str = ""
    assessmentReport: str = None
    masterId: int = None
    complianceScore: float = None
    targets: str = None
    automationInfo: str = None
    automationId: str = None
    metadata: str = None
    assessmentPlan: str = None
    oscalsspId: int = None
    oscalComponentId: int = None
    controlId: int = None
    requirementId: int = None
    securityPlanId: int = None
    projectId: int = None
    supplyChainId: int = None
    policyId: int = None
    componentId: int = None
    incidentId: int = None
    parentId: int = None
    parentModule: str = None
    createdById: str = None
    dateCreated: str = None
    lastUpdatedById: str = None
    dateLastUpdated: str = None
    isPublic: bool = True

    def __getitem__(self, key):
        """get attribute"""
        return getattr(self, key)

    def __setitem__(self, key, value):
        """set attribute"""
        return setattr(self, key, value)

    def dict(self):
        """create a dictionary from the dataclass"""
        return {k: v for k, v in asdict(self).items()}

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

    @staticmethod
    def xint(int_eval: int) -> int:
        """Int None to 0

        Args:
            int_eval (int): Integer

        Returns:
            int: 0 or int
        """
        if int is None:
            return 0
        return int(int_eval)
