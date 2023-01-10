from __future__ import annotations

from tcsoa.gen.Qualification._2014_06.QualificationManagement import QualificationLevelInfo, ManageQualificationInfo, RemoveUserQualificationInfo, UpdateQualificationInfo, AssignUserQualificationInfo
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class QualificationManagementService(TcService):

    @classmethod
    def removeQualificationLevel(cls, qualificationLevelInfo: List[QualificationLevelInfo]) -> ServiceData:
        """
        Removes a level from the list of Qualification levels. 
        """
        return cls.execute_soa_method(
            method_name='removeQualificationLevel',
            library='Qualification',
            service_date='2014_06',
            service_name='QualificationManagement',
            params={'qualificationLevelInfo': qualificationLevelInfo},
            response_cls=ServiceData,
        )

    @classmethod
    def removeUserQualification(cls, removeUserQualificationInfo: List[RemoveUserQualificationInfo]) -> ServiceData:
        """
        Removes a Fnd0Qualification object that is assigned to a Teamcenter User by deleting the Fnd0UserHasQual
        relation object that relates the User and the Fnd0Qualification.
        """
        return cls.execute_soa_method(
            method_name='removeUserQualification',
            library='Qualification',
            service_date='2014_06',
            service_name='QualificationManagement',
            params={'removeUserQualificationInfo': removeUserQualificationInfo},
            response_cls=ServiceData,
        )

    @classmethod
    def updateQualification(cls, updateQualificationInfo: List[UpdateQualificationInfo]) -> ServiceData:
        """
        This operation updates a list of Fnd0Qualification objects.
        """
        return cls.execute_soa_method(
            method_name='updateQualification',
            library='Qualification',
            service_date='2014_06',
            service_name='QualificationManagement',
            params={'updateQualificationInfo': updateQualificationInfo},
            response_cls=ServiceData,
        )

    @classmethod
    def createQualification(cls, qualificationInfo: List[ManageQualificationInfo]) -> ServiceData:
        """
        Creates a list of Fnd0Qualification objects. A single Fnd0Qualification object is created for each
        ManageQualificationInfo structure in the list.
        """
        return cls.execute_soa_method(
            method_name='createQualification',
            library='Qualification',
            service_date='2014_06',
            service_name='QualificationManagement',
            params={'qualificationInfo': qualificationInfo},
            response_cls=ServiceData,
        )

    @classmethod
    def appendQualificationLevel(cls, qualificationLevelInfo: List[QualificationLevelInfo]) -> ServiceData:
        """
        Appends a level to the ordered list of Fnd0Qualification levels.
        """
        return cls.execute_soa_method(
            method_name='appendQualificationLevel',
            library='Qualification',
            service_date='2014_06',
            service_name='QualificationManagement',
            params={'qualificationLevelInfo': qualificationLevelInfo},
            response_cls=ServiceData,
        )

    @classmethod
    def assignUserQualification(cls, assignUserQualificationInfo: List[AssignUserQualificationInfo]) -> ServiceData:
        """
        Assigns a Fnd0Qualification object to a Teamcenter User. Each AssignUserQualificationInfo structure in the
        input list contains information required to assign a Fnd0Qualification object to a Teamcenter User. A
        Fnd0UserHasQual relation object will be created on successful assignment of Fnd0Qualification to a User.
        """
        return cls.execute_soa_method(
            method_name='assignUserQualification',
            library='Qualification',
            service_date='2014_06',
            service_name='QualificationManagement',
            params={'assignUserQualificationInfo': assignUserQualificationInfo},
            response_cls=ServiceData,
        )
