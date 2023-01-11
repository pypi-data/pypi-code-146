from __future__ import annotations

from tcsoa.gen.Internal.Manufacturing._2019_06.ClosureRuleEditor import ClosureRuleTraversalResponse, ClosureRuleTraversalInput, PrimaryToSecondaryTraversalMap
from tcsoa.gen.Internal.Manufacturing._2019_06.ResourceManagement import GetICOMappingTargetsResponse
from typing import List
from tcsoa.gen.Internal.Manufacturing._2019_06.StructureSearch import PartsInProximityResponse, ProximityCriteriaInput
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class StructureSearchService(TcService):

    @classmethod
    def searchPartsInProximityOfMFGFeatures(cls, criteriaInput: List[ProximityCriteriaInput]) -> PartsInProximityResponse:
        """
        This operation retrieves the BOMLine objects representing parts that are in proximity of a given BOMLine of
        type Mfg0BvrManufacturingFeature.
        
        Use cases:
        Manufacturing Planner wants to view the BOMLine objects that are in proximity of a given BOMLine of type
        Mfg0BvrManufacturingFeature to select which BOMLine objects to connect to the given BOMLine of type
        Mfg0BvrManufacturingFeature.
        """
        return cls.execute_soa_method(
            method_name='searchPartsInProximityOfMFGFeatures',
            library='Internal-Manufacturing',
            service_date='2019_06',
            service_name='StructureSearch',
            params={'criteriaInput': criteriaInput},
            response_cls=PartsInProximityResponse,
        )


class ClosureRuleEditorService(TcService):

    @classmethod
    def setClosureRuleTraversalInfo(cls, updatedTraversalInfo: PrimaryToSecondaryTraversalMap, closureRuleName: str) -> ServiceData:
        """
        This service operation updates the closure rule clauses as per the changes made in traversal of objects by the
        user.
        
        Use cases:
        Use Case 1: Updating the closure rule clauses in the closure rule editor view.
        This operation can be used to update the closure rule clauses for the selected closure rule based on the
        modifications done in objects traversal by the user.
        """
        return cls.execute_soa_method(
            method_name='setClosureRuleTraversalInfo',
            library='Internal-Manufacturing',
            service_date='2019_06',
            service_name='ClosureRuleEditor',
            params={'updatedTraversalInfo': updatedTraversalInfo, 'closureRuleName': closureRuleName},
            response_cls=ServiceData,
        )

    @classmethod
    def getClosureRuleTraversalInfo(cls, input: ClosureRuleTraversalInput) -> ClosureRuleTraversalResponse:
        """
        This service operation fetches the traversal information for the given closure rule and the top BOMLine object.
        
        Use cases:
        Use Case 1: User opens the closure rule editor window/panel.
        This operation can be used to get the traversal information for the selected closure rule and BOMLine object
        and display it in the closure rule editor window/panel.
        """
        return cls.execute_soa_method(
            method_name='getClosureRuleTraversalInfo',
            library='Internal-Manufacturing',
            service_date='2019_06',
            service_name='ClosureRuleEditor',
            params={'input': input},
            response_cls=ClosureRuleTraversalResponse,
        )


class ResourceManagementService(TcService):

    @classmethod
    def getICOMappingTargets(cls, icoUIDs: List[str], viewType: int) -> GetICOMappingTargetsResponse:
        """
        This operation obtains target classes under MRL and views that a given source classification object (ICO) can
        be mapped to. Target classes are obtained using following steps. If a match is found at any step, the algorithm
        returns target classes at this step and next steps are not executed.
        1.    Search for the direct mapping classes based on class ID.
        2.    Search is done based on connection code attribute values of source ICO.
        3.    Vendor specific prefixes from the class associated with the ICO are removed and search is done.
        4.    "Bbased on" information in the source class is read and search is done.
        
        Use cases:
        The API will internally extract value for the class ID associated with input source ICO. 
        Checks will be done in following order.
        1.    Search for all views whose IDs match the given source class ID. If source class ID is
        "IS#MILTHGI_WIS$$MTH_MZYL10", search directly for "IS#MILTHGI_WIS$$MTH_MZYL10" views.
        2.    Read values of connection code attributes for source ICO. Obtain strings for 
        a.    GTC base class: <GTC_BASE>
        b.    The connection to the machine side: <MACH>
        c.    The connection to the workpiece side: <WKPS>
        Find mapping targets for above combination.
        3.    If mapping targets are not found, use source class ID to obtain strings for <GTC_BASE>, <MACH> and
        <WKPS>. Find mapping targets for this combination.
        """
        return cls.execute_soa_method(
            method_name='getICOMappingTargets',
            library='Internal-Manufacturing',
            service_date='2019_06',
            service_name='ResourceManagement',
            params={'icoUIDs': icoUIDs, 'viewType': viewType},
            response_cls=GetICOMappingTargetsResponse,
        )
