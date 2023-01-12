from __future__ import annotations

from tcsoa.gen.Cad._2008_03.StructureManagement import AskChildPathBOMLinesInfo
from tcsoa.gen.Cad._2013_05.StructureManagement import CreateWindowsInfo2, AskChildPathBOMLinesResponse2, CreateOrUpdateRelativeStructureInfo4
from tcsoa.gen.Cad._2007_01.StructureManagement import CreateBOMWindowsResponse
from tcsoa.gen.Cad._2009_04.StructureManagement import CreateOrUpdateRelativeStructurePref, CreateOrUpdateRelativeStructureResponse
from typing import List
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def createBOMWindows2(cls, info: List[CreateWindowsInfo2]) -> CreateBOMWindowsResponse:
        """
        Creates a list of window and sets the respective input ItemRevision as the top line. This operation can be used
        to set multiple saved variant rules or single stored option set to the window. For setting Product Configurator
        authored varaint rule on the window, value of preference PSM_enable_product_configurator must be true.It can be
        used to set certain window property, if sent as a part of input. It can be used to create the BOMLine for input
        to Expand Product Structure services.  All BOMLines under this window are unpacked.  To use the Teamcenter
        default unitNo or use your input RevisionRule with no changes, you must set unitNo to -1 in
        RevisionRuleEntryProps::unitNo.  If it is not specified, your input rule will function as a modified/transient
        revision rule with a unitNo of 0.
        
        Use cases:
        This operation creates a list of window and sets the respective input Item revision as the top line. This
        operation can be used to set multiple saved variant rules or single stored option set to the window.
        """
        return cls.execute_soa_method(
            method_name='createBOMWindows2',
            library='Cad',
            service_date='2013_05',
            service_name='StructureManagement',
            params={'info': info},
            response_cls=CreateBOMWindowsResponse,
        )

    @classmethod
    def createOrUpdateRelativeStructure(cls, inputs: List[CreateOrUpdateRelativeStructureInfo4], pref: CreateOrUpdateRelativeStructurePref) -> CreateOrUpdateRelativeStructureResponse:
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
        
        This operation can also perform structure move operations. The move operation is performed within the context
        of the lowest common parent. Along with moving the occurrence from one parent to a new parent, any absolute
        occurrence data present in the original occurrence will also be moved to the new occurrence. The input for the
        move operation is specified in the 'MoveInfo' substructure of 'RelOccInfo'. The 'MoveInfo' data is specified in
        the context of the 'RelativeStructureChildInfo3'. Each 'RelativeStructureChildInfo3' will allow specifying only
        moving of one instance only. In cases where there are multiple instances of the same occurrence, 'MoveInfo' has
        to be specified for each instance. In such cases, each instance data will be specified in its own
        'RelativeStructureChildInfo3' structure. However, the 'child' object is specified only once per occurrence. For
        the other instances of the same occurrence, the 'child' object in the 'RelativeStructureChildInfo3' is
        specified as NULL.
        
        In the following example, to move Part_P1 (instance 1) to SubAssembly_B (instance 1), create a new occurrence
        of Part_P1 under SubAssembly_B. After this add, SubAssembly_B (instance 1) will have a child  Part_P1 (instance
        1) and SubAssembly_B (instance 2) will have a child  Part_P1 (instance 2). Specify the move from the occurrence
        of Part_P1 (instance 1) under SubAssembly_C to the Part_P1 (instance 1) under SubAssembly_B (instance 1).  And
        similarly for the instance 2.
        
        Move Example:
        Assembly_A
             |
             |-->SubAssembly_B  (instance 1)
             |
             |-->SubAssembly_B  (instance 2)
             |
             |-->SubAssembly_C
             |       |
             |       |-->Part_P1    (instance 1)
             | 
             |-->SubAssembly_C
             |       |
             |       |-->Part_P1    (instance 2)
        
        
        To move "Part_P1" from SubAssembly_C to Sub_Assembly_B:
        'relStrInfo4s''[''0''] = new ''CreateOrUpdateRelativeStructureInfo4''();
        ''relStrInfo4s''[''0''].''parentInfo'' = new ''RelativeStructureParentInfo''();
        ''relStrInfo4s''[''0''].''parentInfo.parent'' = ''SubAssembly_B_ItemRev'';
        ''relStrInfo4s''[''0''].''childInfo'' = new ''RelativeStructureChildInfo3''[''1''];
        
        ''relStrInfo4s''[''0''].''childInfo''[''0''] = new ''RelativeStructureChildInfo3''();
        ''relStrInfo4s''[''0''].''childInfo''[''0''].''clientId'' = "''Add_Part_P1_to_SubAssembly_B''";
        ''relStrInfo4s''[''0''].''childInfo''[''0''].child = ''Part_P1'';
        ''relStrInfo4s''[''0''].''childInfo''[''0''].''occInfo'' = new ''RelOccInfo''();
        ''relStrInfo4s''[''0''].''childInfo''[''0''].''occInfo.moveInfo'' = new ''MoveInfo''();
        ''relStrInfo4s''[''0''].''childInfo''[''0''].''occInfo.moveInfo.commonParent'' = ''Assembly_A_ItemRev'';
        ''relStrInfo4s''[''0''].''childInfo''[''0''].''occInfo.moveInfo.sourceAssembly'' = ''SubAssembly_C_ItemRev'';
        ''relStrInfo4s''[''0''].''childInfo''[''0''].''occInfo.moveInfo.occThreadPathToBeMoved'' =
        ''occThreadPathToBeMoved'';
        ''relStrInfo4s''[''0''].''childInfo''[''0''].''occInfo.moveInfo.occThreadPathTargetParent'' =
        ''targetParentOccThr'';'
        
        relStrInfo4s[0].childInfo[1] = new RelativeStructureChildInfo3();
        relStrInfo4s[0].childInfo[1].clientId = "Add_Part_P1_instance_2_to_SubAssembly_B";
        relStrInfo4s[0].childInfo[1].child = NULL;   // For the second instance, set child to NULL
        relStrInfo4s[0].childInfo[1].occInfo = new RelOccInfo();
        relStrInfo4s[0].childInfo[1].occInfo.moveInfo = new MoveInfo();
        relStrInfo4s[0].childInfo[1].occInfo.moveInfo.commonParent = Assembly_A_ItemRev;
        relStrInfo4s[0].childInfo[1].occInfo.moveInfo.sourceAssembly = SubAssembly_C_ItemRev;
        relStrInfo4s[0].childInfo[1].occInfo.moveInfo.occThreadPathToBeMoved = occThreadPathToBeMoved;
        relStrInfo4s[0].childInfo[1].occInfo.moveInfo.occThreadPathTargetParent = targetParentOccThr;
        
        
        Use cases:
        Use Case 1:
        
        User adds an existing component to an existing assembly to create a relative occurrence.
        For this operation, the assembly is passed in as the parent and the component is passed in as the child. The
        relative occurrence is created and a map of the input 'clientID' to 'MappedReturnData' is returned in output
        and the occurrence, BOM view and BOM view revision are returned as created objects in 'ServiceData'.
        
        Use Case 2:
        
        User wants to update the position of the child component relative to the parent assembly.
        For this operation, the transform on the child occurrence information is updated with the new position relative
        to the parent. The assembly is passed in as the parent and the component is passed in as the child. The
        relative occurrence is updated and a map of the 'clientID' to 'MappedReturnData' is returned in 'output' and
        the occurrence and BOM view revision are returned as updated objects in 'ServiceData'.
        
        Exceptions:
        >Service exceptions are thrown for the following error situations:
        
        215005: The BOM view revision (BVR) is not checked out by the current user.
        215006: The BOM view revision is checked out by another user.
        215009: The object type name specified in the input preference does not exist.
        215010: The input CAD occurrence identifier does not correspond to a valid BOM line. This is an error when the
        complete input is false.
        215033: The input last modified date differs from actual.
        215034: The dataset or BVR was modified even when the input last modified dates was different than the current
        last modified data.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateRelativeStructure',
            library='Cad',
            service_date='2013_05',
            service_name='StructureManagement',
            params={'inputs': inputs, 'pref': pref},
            response_cls=CreateOrUpdateRelativeStructureResponse,
        )

    @classmethod
    def askChildPathBOMLines2(cls, input: List[AskChildPathBOMLinesInfo]) -> AskChildPathBOMLinesResponse2:
        """
        This operation returns the BOMLine objects corresponding to input sets of child paths.
        
        The child path is defined by an ordered set of PSOccurrenceThread UIDs, starting from the top level assembly to
        a child node. The child node can be an immediate child or can be multi-level deep. 
        
        This operation will return the BOMLine for each input child path. If a particular child path no longer exists
        in the Teamcenter product structure, there will be no entry for that input child path in the output
        'AskChildPathClientIdToBOMLineMap'.
        
        This operation works on existing BOM windows. The BOM window must have been created prior to using this
        operation.
        
        Use cases:
        If the client has a previously saved list of PSOccurrenceThread paths of a product structure, a new BOM window
        for the top level Item can be created and all the BOM line objects corresponding to the leaf node of the
        PSOccurrenceThread paths can be queried through this operation.
        """
        return cls.execute_soa_method(
            method_name='askChildPathBOMLines2',
            library='Cad',
            service_date='2013_05',
            service_name='StructureManagement',
            params={'input': input},
            response_cls=AskChildPathBOMLinesResponse2,
        )
