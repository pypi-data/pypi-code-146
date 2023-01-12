from __future__ import annotations

from tcsoa.gen.Cad._2009_04.StructureManagement import CreateOrUpdateRelativeStructureResponse, CreateOrUpdateRelativeStructurePref, CreateOrUpdateRelativeStructureInfo
from typing import List
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def createOrUpdateRelativeStructure(cls, inputs: List[CreateOrUpdateRelativeStructureInfo], pref: CreateOrUpdateRelativeStructurePref) -> CreateOrUpdateRelativeStructureResponse:
        """
        This operation creates or updates the relative structure for the input parent assembly and child components. 
        The objects created or updated by this operation include a BOM view (BV), BOM view revision (BVR) and
        occurrence data (PSOccurrence, PSOccurrenceThread).
         
        Before creating the relative structure objects and relations, this operation will check that the structure to
        be created does not already exist.  If the occurrence exists but the input attribute values differ from those
        already set, an attempt is made to update the values.
        
        This operation assumes the input is in a bottom up format such that if any failures occur, the structure that
        is created will still be consumable.  For example:
        
        Parent assembly A, subassembly B and child C are input into this operation.  If the relative structure for
        subassembly B and child C is created successfully but an error occurs during the creation of the structure for
        assembly A and subassembly B, the client can still access the subassembly B, child C relative structure.
        
        No attempt is made in the operation to rearrange the input and process it in the correct order. One parent
        context object is processed at one time and it is assumed that all edits for a given parent context come in as
        one set of input. 
        
        
        Use cases:
        Use Case 1:
        
        User adds an existing component to an existing assembly to create a relative occurrence.
        For this operation, the assembly is passed in as the parent and the component is passed in as the child.  The
        relative occurrence is created and a map of the input 'clientID' to 'MappedReturnData' is returned in 'output'
        and the occurrence, BOM view and BOM view revision are returned as created objects in 'ServiceData'.
        
        Use Case 2:
        
        User wants to update the position of the child component relative to the parent assembly.
        For this operation, the transform on the child occurrence information is updated with the new position relative
        to the parent.  The assembly is passed in as the parent and the component is passed in as the child.  The
        relative occurrence is updated and a map of the 'clientID' to 'MappedReturnData' is returned in 'output' and
        the occurrence and BOM view revision are returned as updated objects in 'ServiceData'.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateRelativeStructure',
            library='Cad',
            service_date='2009_04',
            service_name='StructureManagement',
            params={'inputs': inputs, 'pref': pref},
            response_cls=CreateOrUpdateRelativeStructureResponse,
        )
