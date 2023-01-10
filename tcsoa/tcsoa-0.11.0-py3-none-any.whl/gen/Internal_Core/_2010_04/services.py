from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine
from tcsoa.gen.Internal.Core._2010_04.DataManagement import GetSubscribableTypesAndSubtypesResponse
from typing import List
from tcsoa.gen.Internal.Core._2010_04.ProjectLevelSecurity import ProjectSmartFolderHierarchyOutputResponse2
from tcsoa.base import TcService
from tcsoa.gen.Internal.Core._2010_04.StructureManagement import ValidateInStructureAssociationsResponse


class ProjectLevelSecurityService(TcService):

    @classmethod
    def getProjectsSmartFolderHierarchy2(cls, projectIDs: List[str]) -> ProjectSmartFolderHierarchyOutputResponse2:
        """
        This operation returns smart folder hierarchy as configured by the administrator for the given TC_Project
        objects. This operation returns both internal names and corresponding client locale specific display names for
        each project smart folder. If no project with any of the given project IDs exists in the system error code
        101007: the project ID is invalid; will be returned in a partial error.in the SeviceData of the output
        structure.
        """
        return cls.execute_soa_method(
            method_name='getProjectsSmartFolderHierarchy2',
            library='Internal-Core',
            service_date='2010_04',
            service_name='ProjectLevelSecurity',
            params={'projectIDs': projectIDs},
            response_cls=ProjectSmartFolderHierarchyOutputResponse2,
        )


class DataManagementService(TcService):

    @classmethod
    def getSubscribableTypesAndSubTypes(cls, childTypeOption: str) -> GetSubscribableTypesAndSubtypesResponse:
        """
        This operation retrieves  types and subtypes of business objects for which notification subscriptions can be
        created. It returns types names, subtype names and associated display names of those subscribable types based
        on the 'childTypeOption'.
        
        Use cases:
        - Search for subscribable subtypes:
        
        
        It will search for subscribable subtypes when 'childTypeOption' is specified as 'subtype'.
        """
        return cls.execute_soa_method(
            method_name='getSubscribableTypesAndSubTypes',
            library='Internal-Core',
            service_date='2010_04',
            service_name='DataManagement',
            params={'childTypeOption': childTypeOption},
            response_cls=GetSubscribableTypesAndSubtypesResponse,
        )


class StructureManagementService(TcService):

    @classmethod
    def validateInStructureAssociations(cls, associationType: str, bomlines: List[BOMLine], numLevels: int) -> ValidateInStructureAssociationsResponse:
        """
        Given an array of BOMLine business objects and association_type, this function validates the instructure
        association for all Mechatronics core and ESM relations. The associations like ConnectTo, RealizedBy,
        ImplementedBy, Embeds, Dependenton, GatewayOf, or the Signal relations for the given BOMLine business objects
        and its children as per the number of levels are validated. If the relation type is all, validation is done for
        all types of relations. It validates whether any of the existing relation of any of the passed BOMLine business
        objects are violating the business rule. It also validates whether the original context of the relation is
        changed. If so, it adds such relation to the invalid association list and returns the list. If the number of
        levels is zero value, either entire subtree of the selected lines or immediate children of the selected lines
        are processed. Based on relation value, either validation process is done for specific relation or all
        relations.
        
        Use cases:
        When an assembly or product structure is restructured then user might want to call this operation to validate
        the associations. The user can perform restructure operations like insert level, remove level, MoveTo, split
        occurrences, etc. on the structure. Later the user can use this operation to validate for Mechatronics
        relations after performing these operations.
        """
        return cls.execute_soa_method(
            method_name='validateInStructureAssociations',
            library='Internal-Core',
            service_date='2010_04',
            service_name='StructureManagement',
            params={'associationType': associationType, 'bomlines': bomlines, 'numLevels': numLevels},
            response_cls=ValidateInStructureAssociationsResponse,
        )
