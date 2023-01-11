from __future__ import annotations

from tcsoa.gen.Internal.Manufacturing._2018_11.ResourceManagement import AutoPositionComponentByCSYSResponse
from tcsoa.gen.Internal.Manufacturing._2018_11.StructureManagement import FindBrokenPartsInPVResponse, EvaluateLinksData, FindBrokenPartsInPVInputInfo, FindBrokenProductViewsInputInfo, FindBrokenProductViewsResponse, EvaluateLinksResponse
from typing import List
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def evaluateLinks(cls, input: List[EvaluateLinksData]) -> EvaluateLinksResponse:
        """
        This service operation converts the URL representing a BOMLine to a BOMLine instance. Additionally, returns a
        structure which encapsulates the CCObject or StructureContext representing the context. The parent chain of the
        BOMLine are returned in the serviceData.
        
        Use cases:
        A user can capture the links from Teamcenter representing the BOMLine objects using a utility like
        tc_to_intosite, and use those links with this API to reconstruct the BOMLine objects that were used to create
        the links. These BOMLine objects will have the same configuration and context as the time of the link creation.
        """
        return cls.execute_soa_method(
            method_name='evaluateLinks',
            library='Internal-Manufacturing',
            service_date='2018_11',
            service_name='StructureManagement',
            params={'input': input},
            response_cls=EvaluateLinksResponse,
        )

    @classmethod
    def findBrokenPartsInProductView(cls, input: FindBrokenPartsInPVInputInfo) -> FindBrokenPartsInPVResponse:
        """
        This operation finds the one or more broken parts in the input Dataset product view (PV)objects.
        For a broken PV, it is not possible for the viewer to be able to resolve some or all parts saved during its
        creation. The supplied PV contains such unresolved parts which needs to be updated.
        The operation provides interface to identify broken parts in a PV, so the User can take appropriate actions on
        them.
        
        Use cases:
        User creates a broken PV either by restructuring or deleting elements of BOMLine structure.
        User invokes the service operation with a broken PV Dataset. The operation returns the list of all broken parts
        for given input.
        """
        return cls.execute_soa_method(
            method_name='findBrokenPartsInProductView',
            library='Internal-Manufacturing',
            service_date='2018_11',
            service_name='StructureManagement',
            params={'input': input},
            response_cls=FindBrokenPartsInPVResponse,
        )

    @classmethod
    def findBrokenProductViews(cls, input: FindBrokenProductViewsInputInfo) -> FindBrokenProductViewsResponse:
        """
        This operation finds the one or more broken product views (PV) in the input BOMLine objects.
        For a broken PV, it is not possible for the viewer to be able to resolve some or all parts saved during its
        creation. The supplied PV contains such unresolved parts which needs to be updated.
        The operation provides interface to identify broken PVs and their associated BOMLine objects, so the User can
        take appropriate actions on them.
        
        Use cases:
        User creates a broken PV either by restructuring or deleting elements of BOMLine structure.
        User invokes the service operation with BOMLine objects containing such broken PVs.
        The operation returns the list of all such broken PVs for the given scopes as well as their attached BOMLine
        objects.
        """
        return cls.execute_soa_method(
            method_name='findBrokenProductViews',
            library='Internal-Manufacturing',
            service_date='2018_11',
            service_name='StructureManagement',
            params={'input': input},
            response_cls=FindBrokenProductViewsResponse,
        )


class ResourceManagementService(TcService):

    @classmethod
    def autoPositionComponentByCSYS(cls, strSourceBOMLines: List[str], strTargetBOMLine: str, strSourceCSYS: str, strTargetCSYS: str) -> AutoPositionComponentByCSYSResponse:
        """
        This operation positions a newly added target component so that it fits to the source component geometrically
        based on coordinate systems (CSYSs). This opeation is used when the user 
        a) adds a classified component, 
        b) adds a component with Guided Component Search (GCS) or 
        c) adds a component with copy and paste 
        in Teamcenter Rich Application Client (RAC).
        The source object can be a component, a CSYS or a GCS Connection Point (CP).
        
        This operation analyses the source and target CSYSs and GCS CPs and does the geometrical positioning by setting
        the transformation matrix in the target component BOMLine. (In one specific case (GCS Add Upwards), the target
        component is positioned to the zero position and the source position is adjusted correspondingly.)
        
        If the source object is a component or a GCS CP, it can happen that there are multiple possible source CSYSs.
        In this case the operation returns those CSYSs in the response object and does NOT autoposition, if no specific
        source CSYS was specified. The operation has to be called in that case again with an unique source CSYS.
        
        If the target object (always a component) has multiple possible target CSYSs, the operation returns those CSYSs
        in the response object and does NOT autoposition, if no specific target CSYS was specified. The operation has
        to be called in this case again with an unique target CSYS.
        
        Use cases:
        When the user creates resource assembly in Resource Manager components will be positioned correctly if both
        parent and child components have appropriate CSYSs. The user can do add/paste/GCS add components by selecting a
        component, CSYS or selecting one or multiple GCS CP lines. The system then analyzes the CSYSs under the parent
        and child component and carry out the positioning. If there are appropriate multiple CSYS for positioning, the
        system asks the user to select one of them.
        """
        return cls.execute_soa_method(
            method_name='autoPositionComponentByCSYS',
            library='Internal-Manufacturing',
            service_date='2018_11',
            service_name='ResourceManagement',
            params={'strSourceBOMLines': strSourceBOMLines, 'strTargetBOMLine': strTargetBOMLine, 'strSourceCSYS': strSourceCSYS, 'strTargetCSYS': strTargetCSYS},
            response_cls=AutoPositionComponentByCSYSResponse,
        )
