from __future__ import annotations

from typing import List
from tcsoa.gen.Requirementsmanagement._2010_09.RequirementsManagement import MoveLineResponse, MoveLineInfo
from tcsoa.base import TcService


class RequirementsManagementService(TcService):

    @classmethod
    def moveLine(cls, input: List[MoveLineInfo]) -> MoveLineResponse:
        """
        This operation manipulates the BOMLine Structure (Requirement/ Function/ SEBlock structure) by moving the
        selected BOMLine object either Upwards, Downwards or to a specific position. A Number property will be updated
        for selected Fnd0BuildingBlockBOMLine object along with its children. 
        Following operation are supported by this service operation.
        - Move Up - To move up the selected BOM line (Fnd0BuildingBlockBOMLine) up in the structure with respect to its
        sibling. For instance, if a requirement structure "Req_01", we have two children "SubReq_01" and "SubReq_02".
        In move up structure modification can be done with respect to the parent. Requirements "SubReq_01" and
        "SubReq_02" can be move up in context of parent "Req_01".
        - Move Down - To move down the selected BOM line (Fnd0BuildingBlockBOMLine) up in the structure with respect to
        its sibling. For instance, if a requirement structure "Req_01", we have two children "SubReq_01" and
        "SubReq_02". In move down structure modification can be done with respect to the parent. Requirements
        "SubReq_01" and "SubReq_02" can be move down in context of parent "Req_01".
        - Promote - To indent the selected BOM line (Fnd0BuildingBlockBOMLine) up in the structure with respect to its
        sibling. For instance, promote a requirement previously occupying level 2, with number "1.1", moves to the
        level 1, with number "2.0". Children previously occupying level 3 with number "1.1.1", moves to the level 2,
        with number "2.1".
        - Demote - To out-dent the selected BOM line (Fnd0BuildingBlockBOMLine) up in the structure with respect to its
        sibling. For instance, demote a requirement previously occupying level 2, with number "1.0", moves to the level
        3, with number "1.1.1". Children previously occupying level 3, with number "1.1.1", moves to the level 4, with
        number "1.1.1.1".
        - Edit Number - To move the selected BOM line (Fnd0BuildingBlockBOMLine) up in the structure with respect to
        its sibling. You can able to move selected BOM line object from one level to other and from one parent to other
        parent.  For instance, if a requirement has number "1.1.1" which means it is under parent "1.1". If the number
        changed to "1.1.3", the requirement is repositioned under the parent. If the number is changed to "2.1", then
        requirement will be removed from the parent and put under the sibling of the parent.
        
        
        
        Use cases:
        You can manipulate the hierarchy for a selected Requirement /Function/ SEBlockBOMLine object by using the
        moveLine operation. The given Fnd0BuildingBlockBOMLine object will be moved as per the choice along with its
        children and the Number property will be updated with new values.
        """
        return cls.execute_soa_method(
            method_name='moveLine',
            library='Requirementsmanagement',
            service_date='2010_09',
            service_name='RequirementsManagement',
            params={'input': input},
            response_cls=MoveLineResponse,
        )
