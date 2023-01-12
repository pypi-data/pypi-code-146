from __future__ import annotations

from tcsoa.gen.Internal.Manufacturing._2015_10.StructureManagement import GetEquivalentPropValuesElement, AlignLinesInBOMData, PasteOrReplaceAssemblyInContextResponse, GetEquivalentPropValuesResp, AlignLinesInBOMResponse, PasteOrReplaceAssemblyInContextInfo
from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.Manufacturing._2015_10.StructureSearch import FindEquivalentLinesResp, FindCPCResponse, FindEquivalentLinesIn
from typing import List
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def pasteOrReplaceAssemblyInContext(cls, assemblyInContextInput: List[PasteOrReplaceAssemblyInContextInfo]) -> PasteOrReplaceAssemblyInContextResponse:
        """
        This operation pastes an assembly item under a target assembly Item or replaces an existing assembly Item with
        a new assembly Item while retaining any in-context edits on the properties and attachments under the target
        assembly.  For the paste, the new assembly Item can be either a previously saved raw (with no child lines)
        Item, or the same assembly Item. For replace, the new assembly Item is always a saved raw assembly Item ( no
        child lines). A cloning rule controls which child lines and in-context attachments are to be cloned or
        referenced under the new assembly's BOMLine.
        
        Use cases:
        A user wants to reuse an existing assembly with occurrence effectivity 1-10, but wants the new assembly to have
        all the original in-context edits and attachments and then modify occurrence effectivity to 11-UP. User either
        wants the new assembly to be a new object or the same object itself which will be pasted under a target object.
        If user doesn't want the old item any more user can also replace the existing assembly with a new object. The
        new object or the same object ( in case of pasting the same object) will be modified according to a cloning
        rule before pasting onto the target. Then user can set new effectivities on original and the new assembly. 
        The cloning rule is specified by a preference "CopyAssemblyInContextTemplates" which points to another
        preference e.g. "Item.Item.CopyAssemblyInContext" implying that the source is of type "Item" and target is of
        type "Item". It specifies information on what objects to clone or reference. It will also include rules for any
        in-context attachments.
        Example clauses on the cloning rule are below.. Wildcard "*" refers to all objects:
        *:*:Attribute.items_tag:Clone
        *:*:Attribute.structure_revisions:Clone
        *:*:Attribute.bom_view:Clone
        *:*:Attribute.parent_item:Clone
        *:*:OccType.*:Reference
        *:*:Relation.*:Reference
        class.Folder:*:Attribute.contents:Reference
        """
        return cls.execute_soa_method(
            method_name='pasteOrReplaceAssemblyInContext',
            library='Internal-Manufacturing',
            service_date='2015_10',
            service_name='StructureManagement',
            params={'assemblyInContextInput': assemblyInContextInput},
            response_cls=PasteOrReplaceAssemblyInContextResponse,
        )

    @classmethod
    def alignLinesInBOM(cls, alignInputs: List[AlignLinesInBOMData]) -> AlignLinesInBOMResponse:
        """
        This service operation aligns ID in Context (Top Level) and Absolute Transformation Matrix between an
        Engineering BOM (EBOM) and a Manufacturing BOM (MBOM). The operation also optionally aligns occurrence
        properties based on the preference MEAlignedPropertiesList.
        
        Use cases:
        Case 1: Single line alignment
        Given a selected source BOMLine object in a structure (e.g., EBOM) and its equivalent target BOMLine object in
        another structure (e.g., MBOM), this operation aligns these two lines.
        
        Case 2: Assemblies alignment
        Given a list of source scopes (e.g., in EBOM) and a list of target scopes from non-reused assemblies (e.g., in
        MBOM), this operation traverses the specified scopes and aligns the equivalent scope lines and all equivalent
        BOMLine objects below the scopes. 
        
        Case 3: Reused assemblies alignment
        Given a list of source scopes (e.g., in EBOM) and a list of target scopes from reused assemblies (e.g., in
        MBOM), this operation traverses the specified scopes and aligns all equivalent BOMLine objects below the scopes.
        """
        return cls.execute_soa_method(
            method_name='alignLinesInBOM',
            library='Internal-Manufacturing',
            service_date='2015_10',
            service_name='StructureManagement',
            params={'alignInputs': alignInputs},
            response_cls=AlignLinesInBOMResponse,
        )

    @classmethod
    def getEquivalentPropertyValues(cls, input: List[GetEquivalentPropValuesElement]) -> GetEquivalentPropValuesResp:
        """
        This operation finds equivalent property values on an ItemRevision for a given list of input properties.  The 
        operation receives sets of property names associated with either an Item, ItemRevision, Item Master or Item
        Revision Master, an original ItemRevision and new Item Revision.    For each property it looks for an
        equivalent property for the original ItemRevision. If found, then its value is retrieved and returned in a map
        of input property names to equivalent property values. In addition it returns the attachment relation and
        secondary object  that match cloning rules.
        """
        return cls.execute_soa_method(
            method_name='getEquivalentPropertyValues',
            library='Internal-Manufacturing',
            service_date='2015_10',
            service_name='StructureManagement',
            params={'input': input},
            response_cls=GetEquivalentPropValuesResp,
        )


class StructureSearchService(TcService):

    @classmethod
    def findCollabPlanningContext(cls, inputScopes: List[BusinessObject]) -> FindCPCResponse:
        """
        This service operation searches and returns all the Collaboration Planning Contexts (CPCs) that refer to the
        given business objects. CPC is not a MECollaborationContext object, and is a term used for mix production.
        
        Use cases:
        - Use Case 1: You need to know what CPCs were created from a certain data (in the original structure like EBOP
        or WorkArea). You should than select the original data and search for CPCs that refer to this data.
        - Use Case 2: You can select any object i.e. Mfg0BvrPlantBOP/
        Mfg0BvrProcess/Mfg0BvrOperation/Mfg0BvrWorkarea/Mfg0BvrProcessLine/Mfg0BvrProcessStatio/ Mfg0BvrProcessArea and
        search for the CPC that contains it.
        
        """
        return cls.execute_soa_method(
            method_name='findCollabPlanningContext',
            library='Internal-Manufacturing',
            service_date='2015_10',
            service_name='StructureSearch',
            params={'inputScopes': inputScopes},
            response_cls=FindCPCResponse,
        )

    @classmethod
    def findEquivalentLines(cls, searchInputs: List[FindEquivalentLinesIn]) -> FindEquivalentLinesResp:
        """
        This operation finds equivalent lines between Engineering BOM (EBOM) and Manufacturing BOM (MBOM) using search
        criteria such as ID in Context (Top Level), Item ID and Absolute Transformation Matrix, or ID in Context (All
        Levels).
        
        Use cases:
        Case 1: Find equivalent lines in the other structure
        Given a list of BOMLine objects in one structure (e.g., MBOM), this operation will find their equivalent
        BOMLine objects in the other structure (e.g., EBOM), based on specified search criteria. In this case, the
        equivalent BOMLine objects of the source will be searched under the target scopes. The return will be a map
        between source BOMLine objects and their equivalent target BOMLine objects.
        """
        return cls.execute_soa_method(
            method_name='findEquivalentLines',
            library='Internal-Manufacturing',
            service_date='2015_10',
            service_name='StructureSearch',
            params={'searchInputs': searchInputs},
            response_cls=FindEquivalentLinesResp,
        )
