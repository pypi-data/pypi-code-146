from __future__ import annotations

from tcsoa.gen.Internal.Cad._2017_05.StructureManagement import GetProductStructureArrangementsResp, ProductStructureArrangementInput
from typing import List
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def getProductStructureArrangements(cls, psArrInput: List[ProductStructureArrangementInput]) -> GetProductStructureArrangementsResp:
        """
        This operation returns arrangement data for given product structures. The product structures are identified in
        one of two ways, through input of either:
        * a "root" PSBOMViewRevision.  For each root structure, a list of any additional substructures from which to
        obtain arrangement data can be provided. 
        * a BOMWindow with list of Fnd0BOMLineLite (LightWeightBOM or LWB) lines of that window.
        This operation does not load objects. It provides Access Manager (AM) data access checks at the database level,
        for any data returned.
        
        For each product structure, a "base" arrangement is created and returned. 
        A base arrangement consists of relative occurrence transformation information for each immediate child
        occurrence of the product structure, along with any overrides of those occurrences that are not in context of
        any arrangement. These are transformation or geometry (jt) overrides. 
        Note that the base arrangement will contain information for all immediate child occurrences. No configuration
        evaluation is performed, e.g. no occurrence effectivity or variant configuration is applied. 
        If no AssemblyArrangements are found for a product structure, the return for that product structure is only the
        base arrangement.
        
        Use cases:
        UseCase: Multilevel structure with overrides on substructure lines
        
        Given the following structure with arrangements defined:
        TopAssembly with arrangements TopDefault, Top0
        ------SubAssembly with arrangements SubDefault, Sub0
        ------------Part1 with transformation override in context of TopAssembly, no arrangement
        ------------Part2 with transformation override in context of SubAssembly, SubDefault arrangement
        ------------Part3 with transformation override in context of SubAssembly, Sub0 arrangement
        The TopDefault arrangement "uses" the SubDefault arrangement on the SubAssembly child.
        The Top0 arrangement "uses" the Sub0 arrangement on the SubAssembly child.
        
        With psArrInput vector containing a singele element which itself  is a vector with the single input of Top
        Assembly PSBOMViewRevision, the returned output vector contains a single element which itself is a vector with
        the single arrangementData structure for TopAssembly. The arrangementData structure contains the following:
        -TopAssembly base arrangement, with:
           * Occurrence data for the immediate child SubAssembly (occurrencePath and relative transformation)
           * Occurrence override data for the immediate child SubAssembly&rsquo;s Part1 transformation override which
        is in context of TopAssembly.
        -TopAssembly arrangement TopDefault, with override data uses SubDefault arrangement (the arrangmentID.)
        -TopAssembly arrangement Top0, with override data uses Sub0 arrangement (the arrangmentID.)
        Note that the ArrangementID is a structure defined to hold the arrangementName and subfileID that identifies
        the specific Arrangement.
        
        With psArrInput vector containing a singele element which itself  is a vector with 2 inputs, Top Assembly and
        SubAssembly PSBOMViewRevisions, the returned output vector contains a single element which itself is a vector
        of size 2 holding the arrangementData for the input as follows.
        TopAssembly:
        -TopAssembly base arrangement, with:
           * Occurrence data for the immediate child SubAssembly (occurrencePath and relative transformation)
           * Occurrence override data for the immediate child SubAssembly&rsquo;s Part1 transformation override which
        is in context of TopAssembly.
        -TopAssembly arrangement TopDefault, with override data uses SubDefault arrangement (the arrangmentID.)
        -TopAssembly arrangement Top0, with override data uses Sub0 arrangement (the arrangmentID.) 
        
        SubAssembly: 
        -SubAssembly base arrangement with:
           * Occurrence data for each of the the immediate children Part1, Part2, Part3 (occurrencePath and relative
        transformation)
        -SubAssembly arrangement SubDefault, with transformation override data for Part2
        -SubAssembly arrangement Sub0, with transformation override data for Part3
        """
        return cls.execute_soa_method(
            method_name='getProductStructureArrangements',
            library='Internal-Cad',
            service_date='2017_05',
            service_name='StructureManagement',
            params={'psArrInput': psArrInput},
            response_cls=GetProductStructureArrangementsResp,
        )
