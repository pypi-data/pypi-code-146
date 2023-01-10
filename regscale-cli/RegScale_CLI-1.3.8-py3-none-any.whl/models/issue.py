#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports
from dataclasses import dataclass


@dataclass
class Issue:
    """Issue Model"""

    title: str = ""  # Required
    severityLevel: str = ""  # Required
    issueOwnerId: str = ""  # Required
    dueDate: str = ""  # Required

    id: int = None
    uuid: str = None
    dateCreated: str = None
    description: str = None
    issueOwner: str = None
    costEstimate: int = None
    levelOfEffort: int = None
    identification: str = None
    sourceReport: str = None
    status: str = None
    dateCompleted: str = None
    facility: str = None
    facilityId: int = None
    org: str = None
    orgId: int = None
    controlId: int = None
    assessmentId: int = None
    requirementId: int = None
    securityPlanId: int = None
    projectId: int = None
    supplyChainId: int = None
    policyId: int = None
    componentId: int = None
    incidentId: int = None
    jiraId: str = None
    serviceNowId: str = None
    wizId: str = None
    prismaId: str = None
    tenableId: str = None
    qualysId: str = None
    pluginId: str = None
    cve: str = None
    assetIdentifier: str = None
    falsePositive: str = None
    operationalRequirement: str = None
    autoApproved: str = None
    kevList: str = None
    dateFirstDetected: str = None
    changes: str = None
    vendorDependency: str = None
    vendorName: str = None
    vendorLastUpdate: str = None
    vendorActions: str = None
    deviationRationale: str = None
    parentId: int = None
    parentModule: str = None
    createdBy: str = None
    createdById: str = None
    lastUpdatedBy: str = None
    lastUpdatedById: str = None
    dateLastUpdated: str = None
    isPublic: bool = True

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
