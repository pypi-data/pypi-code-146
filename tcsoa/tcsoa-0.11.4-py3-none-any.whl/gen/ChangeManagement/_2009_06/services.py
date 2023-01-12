from __future__ import annotations

from tcsoa.gen.ChangeManagement._2009_06.ChangeManagement import GetNoteVariantsInput, GetNoteVariantResponse
from typing import List
from tcsoa.base import TcService


class ChangeManagementService(TcService):

    @classmethod
    def getNoteVariantChanges(cls, getNoteVariantRequest: List[GetNoteVariantsInput]) -> GetNoteVariantResponse:
        """
        This operation is specifically designed to handle the retrieval of information for Note or Variant changes to
        be consumed by the Teamcenter Structure Manager Rich Client UI.  There are helper functions in the Rich Client
        to facilitate the consumption and interpretation of the retrieved information.  In other words, this operation
        may pose challenges to users of this operation who are unfamiliar with the intended usage of the returned
        details.  For Rich Client developers, it is better to use the helper functions instead.
        The operation accepts as input a list of 'GetNoteVariantsInput' structures, each containing an object reference
        to a 'BOMEdit' whose integer type is EITHER 6 (=Note Change) OR 7(=Variant Change) and a matching context
        string of one of the following two possible values:
        - CM_note_change_details
        - CM_variant_change_details
        
        
        Based on the input structures, the operation will assemble the retrieved information in a list of
        'GetNoteVariantOutput' structures, and package them together with a standard service data in the returned
        'GetNoteVariantResponse' structure.
        
        Use cases:
        Use Case 1: Getting the details for a note change
        This operation can be invoked via an instance of the 'ChangeManagementService'.  The caller program will need
        to supply an object reference to a 'BOMEdit' whose integer type is 6 and a matching context string of
        CM_note_change_details in the input structure 'GetNoteVariantsInput'.  The corresponding output structure
        'GetNoteVariantOutput' contains object references to 1) the BOMEdit, 2) the associated change revision, 3) the
        solution bvr, and 4) the impacted bvr.  It also contains a list of details count and a list of strings
        representing some textual details of the note change.  The caller program will use the count to read the
        strings for details.
        Use Case 2: Getting the details for a variant change
        This operation can be invoked via an instance of the 'ChangeManagementService'.  The caller program will need
        to supply an object reference to a 'BOMEdit' whose integer type is 7 and a matching context string of
        CM_variant_change_details in the input structure 'GetNoteVariantsInput'.  The corresponding output structure
        'GetNoteVariantOutput' contains object references to 1) the BOMEdit, 2) the associated change revision, 3) the
        solution bvr, and 4) the impacted bvr.  It also contains a list of details count and a list of strings
        representing some textual details of the variant change.  The caller program will use the count to read the
        strings for details.
        
        """
        return cls.execute_soa_method(
            method_name='getNoteVariantChanges',
            library='ChangeManagement',
            service_date='2009_06',
            service_name='ChangeManagement',
            params={'getNoteVariantRequest': getNoteVariantRequest},
            response_cls=GetNoteVariantResponse,
        )
