from __future__ import annotations

from tcsoa.gen.StructureManagement._2018_11.Structure import CreateGroupInput
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class StructureService(TcService):

    @classmethod
    def createInterchangeableGroups(cls, inputs: List[CreateGroupInput]) -> ServiceData:
        """
        Creates Occurrence level substitute groups or Item/ItemRevision level (global) alternate groups based on the
        input object type. 
        
        Interchangeable Groups are groups of "stockable parts" that needs to be all replaced together as repairs are
        made. They can be defined at two levels:
        &bull;    Occurrence: List of occurrences that must be replaced together with a list of Item objects within the
        same BVR.
        &bull;    Item/Item Revision (Global): List of Item/ItemRevision objects that must be replaced together with
        another list of Item objects &ndash; regardless of the assembly where they are used.
        
        Use cases:
        This operation creates an interchangeable group based on the input object type, source objects, interchangeable
        parts list and any properties to set on the interchangeable group. The new interchangeable group will be
        returned through 'ServiceData'.
        &bull;    User wants to provide a substitute group for a list of components in a structure. So in the input the
        user can choose Substitute Group type, provide source occurrences and select a list of Item object as
        substitute parts. The new substitute group for the structure will be returned through 'ServiceData'.
        &bull;    User wants to create a substitute group but also identify additional properties with properties
        input. So in the input the user can choose Substitute Group type, provide source occurrences and substitute
        parts list, also input additional properties. The new substitute group will be returned through 'ServiceData'.
        &bull;    User wants to create an alternate group. So in the input the user sets Alternate Group type, provide
        source Item/ItemRevision objects, and select a list of Item objects as alternate parts. The new alternate group
        will be returned through 'ServiceData'.
        """
        return cls.execute_soa_method(
            method_name='createInterchangeableGroups',
            library='StructureManagement',
            service_date='2018_11',
            service_name='Structure',
            params={'inputs': inputs},
            response_cls=ServiceData,
        )
