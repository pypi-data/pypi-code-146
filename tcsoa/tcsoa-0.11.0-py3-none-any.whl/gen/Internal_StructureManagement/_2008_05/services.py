from __future__ import annotations

from tcsoa.gen.Internal.StructureManagement._2008_05.Structure import BOMLinePair
from typing import List
from tcsoa.gen.Internal.StructureManagement._2008_05.Restructure import ReplaceInContextParameter
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class RestructureService(TcService):

    @classmethod
    def replaceInContext(cls, input: List[ReplaceInContextParameter]) -> ServiceData:
        """
        Replaces the line with a newly created item copied from the item to be replaced and copy the children from the
        original item, absolute occurrences, GRM links and Incremental Change Elements of the children will be copied.
        
        Note:
        o  The operation only supports items. Objects of General Design Elements are not supported.
        o  The item used to replace the selected line should be copied from the selected item by calling save as
        action, so that the occurrences of the old children will have clone stable id associated to the new children.
        o  The operation will invoke replace action, so restrictions to replace action will also apply to this
        operation:
        - Preference PS_replace_with_substructure will also apply
        - If the selected line has substitutes, the operation will fail.
        - If the selected line or its parent is linked to variant item, the operation will fail.
        - If the selected line is a variant item, the item to replace it should be a matching variant item.
        
        
        
        Use cases:
        User has a three level structure which has absolute occurrence data at leaf nodes. He saves the parent of the
        leaf node and save it as a new item and invokes this operation to replace the existing line while keep the
        children and absolute occurrence data.
        """
        return cls.execute_soa_method(
            method_name='replaceInContext',
            library='Internal-StructureManagement',
            service_date='2008_05',
            service_name='Restructure',
            params={'input': input},
            response_cls=ServiceData,
        )


class StructureService(TcService):

    @classmethod
    def syncAlignedOccurrences(cls, input: List[BOMLinePair]) -> ServiceData:
        """
        When alignment is out of sync, copy specified property values from source of the alignment to the target.
        
        Note:
        - Properties to be synchronized are determined by preference MEAlignedPropertiesList and
        MEAlignedPropertiesToExcludeFromSync.
        - Properties in out of the box preference MEAlignedPropertiesList are supported. Properties not in the list
        should be supported unless they require complex handling.
        - Use property 'bl_occ_effectivity' for occurrence effectivity. Legacy occurrence effectivity is not support.
        If the occurrence effectivity is shared, then EBOM and MBOM will share it, otherwise it will be copied.
        Preference CFMOccEffMode can be used to configure occurrence effectivity mode.
        - Only legacy variant condition is supported by using property 'bl_condition_tag', and condition is shared.
        Modular variant condition is not supported.
        
        
        
        Use cases:
        User finds out of sync alignments by calling operation 'checkAlignment', and calls this operation to
        synchronize the alignments.
        """
        return cls.execute_soa_method(
            method_name='syncAlignedOccurrences',
            library='Internal-StructureManagement',
            service_date='2008_05',
            service_name='Structure',
            params={'input': input},
            response_cls=ServiceData,
        )
