from __future__ import annotations

from tcsoa.gen.Rdv._2010_09.ContextManagement import UpdateSCOResponse, CreateSCOResponse, UpdateSCOInputInfo, CreateSCOInputInfo
from typing import List
from tcsoa.base import TcService


class ContextManagementService(TcService):

    @classmethod
    def updateSCO(cls, inputs: List[UpdateSCOInputInfo]) -> UpdateSCOResponse:
        """
        Updates the Structure Context Object (SCO) based on the inputs attributes. It sets the following properties on
        SCO object which is to be modified: Product Item Revision, Revision Rule, Variant Rule, Work parts, Search
        Criteria Group, Target and Background BOMLine objects from the input structure. This SCO will contain the Item,
        Item revisions, Target BOMLine objects, Background BOMLine objects. The operation is designed to support
        multiple SCOs creations in a single call. (Limitation: Though this operation can update multiple SCO objects
        however it can return reference of only one object). This operation first checks for the local ownership of the
        object to be updated. This operation will fail if null or incorrect reference to existing SCO object is passed
        in the input.
        
        Use cases:
        1. Update an SCO
        You can update an SCO object of type VisStructureContext using 'updateSCO' operation by providing the
        'UpdateSCOInputInfo' structure.
        - Create an SCO, object of StructureContext, using the 'createSCO' operation.
        - Retrieve the reference to StructureContext returned from above step.
        - Modify the required search criteria and populate the 'UpdateSCOInputInfo' structure.
        - Call 'updateSCO' which will modify the existing StructureContext object.
        
        """
        return cls.execute_soa_method(
            method_name='updateSCO',
            library='Rdv',
            service_date='2010_09',
            service_name='ContextManagement',
            params={'inputs': inputs},
            response_cls=UpdateSCOResponse,
        )

    @classmethod
    def createSCO(cls, inputs: List[CreateSCOInputInfo]) -> CreateSCOResponse:
        """
        Creates the Structure Context Object (SCO) based on the inputs supplied. It creates an SCO object and then sets
        the following properties on SCO object created: Product Item Revision, Revision Rule, Variant Rule, Work parts
        selected, Search Criteria Group, Target and Background BOMLine objects from the input structure. This SCO will
        contain the Item, Item revisions, Target BOMLine objects, Background BOMLine objects. The operation is designed
        to support multiple SCOs creations in a single call. (Limitation: Though this operation can create multiple SCO
        objects however it can return reference of only one object). The operation will initially create the SCO object
        using the name, type and description. Subsequently it would set the additional parameters supplied through the
        input structure. SCO object would still be created and saved even if setting of the additional parameters is
        not successful.
        
        Use cases:
        1. Create an SCO
        YouYou can create a new SCO object of type VisStructureContext using 'createSCO' operation by providing the
        'CreateSCOInputInfo' structure.
        """
        return cls.execute_soa_method(
            method_name='createSCO',
            library='Rdv',
            service_date='2010_09',
            service_name='ContextManagement',
            params={'inputs': inputs},
            response_cls=CreateSCOResponse,
        )
