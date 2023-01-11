from __future__ import annotations

from tcsoa.gen.Bom._2008_06.StructureManagement import BaselineResponse, RemoveChildrenFromParentLineResponse, AddOrUpdateChildrenToParentLineResponse, BaselineInput, AddOrUpdateChildrenToParentLineInfo
from tcsoa.gen.BusinessObjects import BOMLine
from typing import List
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def removeChildrenFromParentLine(cls, bomlines: List[BOMLine]) -> RemoveChildrenFromParentLineResponse:
        """
        This operation allows developers to remove a BOMLine from an assembly /product structure. This operation takes
        vector of BOMLine business objects as input, which allows removal of multiple BOMLines from the structure in a
        single operation.
        
        Use cases:
        User wants to remove two lines. He/She invokes the operation with the lines, and the lines are removed.
        """
        return cls.execute_soa_method(
            method_name='removeChildrenFromParentLine',
            library='Bom',
            service_date='2008_06',
            service_name='StructureManagement',
            params={'bomlines': bomlines},
            response_cls=RemoveChildrenFromParentLineResponse,
        )

    @classmethod
    def createBaseline(cls, inputs: List[BaselineInput]) -> BaselineResponse:
        """
        Creates a new Baseline ItemRevision based on a work in progress ItemRevision.  If the input ItemRevision
        consists of a PSBOMViewRevision that represents a multi level structure, all components of the structure are
        baselined in a recursive fashion. If smart baseline option is enabled at the site, then components of the
        structure will be baselined only if they satisfy the criteria set forth by smart baseline feature. Released
        ItemRevision objects are not baselined, unless the specific name of ReleaseStatus object is mentioned in the
        preference Baseline_allowed_baserev_statuses.
        """
        return cls.execute_soa_method(
            method_name='createBaseline',
            library='Bom',
            service_date='2008_06',
            service_name='StructureManagement',
            params={'inputs': inputs},
            response_cls=BaselineResponse,
        )

    @classmethod
    def addOrUpdateChildrenToParentLine(cls, inputs: List[AddOrUpdateChildrenToParentLineInfo]) -> AddOrUpdateChildrenToParentLineResponse:
        """
        This operation takes item / item revision (depending on precise or imprecise structure) or a GDE. It takes view
        type to create a BOMView for the parent line in a product structure.  When the BOMLine for the item/item
        revision is provided and client id is empty, an update will be performed.
        
        Use cases:
        - User wants to update properties of two lines. He/She invokes the operation with the two lines and property
        values. The two lines will be updated with the specified property values.
        - User wants to create two lines with certain initial property values. He/she invokes the operation with the
        parent line, the two items to add and the initial property values. Two new lines will be created with the
        initial property values.  
        
        """
        return cls.execute_soa_method(
            method_name='addOrUpdateChildrenToParentLine',
            library='Bom',
            service_date='2008_06',
            service_name='StructureManagement',
            params={'inputs': inputs},
            response_cls=AddOrUpdateChildrenToParentLineResponse,
        )
