from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BOMWindow
from tcsoa.gen.StructureManagement._2011_06.Structure import ValidateStructureItemIdsInfo3, UnloadType, ExpandOrUpdateDuplicateItemsResponse2, DuplicateInputInfo3, ValidateStructureItemIdsResponse3, ClosureRuleVariableInfo
from tcsoa.gen.StructureManagement._2008_06.Structure import ExpandOrUpdateDuplicateItemsInfo, DuplicateResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class StructureService(TcService):

    @classmethod
    def setClosureRuleVariablesAndValues(cls, window: BOMWindow, closureRuleName: str, closureRuleVariableInfos: List[ClosureRuleVariableInfo]) -> ServiceData:
        """
        Sets ClosureRule on the BOMWindow. If ClosureRule has variables then respective values supplied are used during
        ClosureRule evaluation. Only ClosureRule with scope PIE_TEAMCENTER is considered by this operation.
        
        In case if ClosureRule should be reset on BOMWindow then input ClosureRule name should be empty string.
        
        Use cases:
        Perform controlled BOM expansion using ClosureRule.
        """
        return cls.execute_soa_method(
            method_name='setClosureRuleVariablesAndValues',
            library='StructureManagement',
            service_date='2011_06',
            service_name='Structure',
            params={'window': window, 'closureRuleName': closureRuleName, 'closureRuleVariableInfos': closureRuleVariableInfos},
            response_cls=ServiceData,
        )

    @classmethod
    def unloadBelow(cls, bomlines: List[BOMLine], unloadType: UnloadType) -> ServiceData:
        """
        This operation unloads and destroy the BOM structure ( i.e. BOMLine objects) below supplied BOMLine object or
        objects. It would unload associated persistence objects like Item, ItemRevision, PSBomViewrevision and
        PSOccurrence etc. and free up memory.
        
        Use cases:
        The operation is intended to improve the scalability of BOM structure expansion. From a large BOM structure,
        user can unload the BOM structure that he has finished working on. This will free up the memory which would be
        used for expanding another sub-structure that user starts working on.
        """
        return cls.execute_soa_method(
            method_name='unloadBelow',
            library='StructureManagement',
            service_date='2011_06',
            service_name='Structure',
            params={'bomlines': bomlines, 'unloadType': unloadType},
            response_cls=ServiceData,
        )

    @classmethod
    def validateStructureItemIds3(cls, inputs: List[ValidateStructureItemIdsInfo3]) -> ValidateStructureItemIdsResponse3:
        """
        This operation is called as part of the duplicate/clone operation.  It will validate the un-validated ItemIds
        and user selected projects that will be used to clone(duplicate) an assembly structure.   All portions of the
        structure that are displayed in the duplicate dialog have been validated by the client.
        
        Note: The differences between the three operations 'validateStructureItemIds', 'validateStructureItemIds2' and
        'validateStructureItemIds3' are the following:
        - In 'validateStructureItemIds' the input is the top BOMLine of the original configured structure in Structure
        Manager.  In 'validateStructureItemIds2' the input is the selected BOMLine of the configured structure in
        Structure Manager or Systems Engineering.  i.e. the user can select to clone a sub-assembly of the original
        structure or the entire assembly.  The input for 'validateStructureItemIds2' includes project(s).  The cloned
        structure is assigned to those project(s).  'validateStructureItemIds' did not have projects as input.
        
        - 'validateStructureItemIds3' was created as a result of the Multi Field Key(MFK) project.  The difference
        between 'validateStructureItemIds2' and 'validateStructureItemIds3' is that in 'validateStructureItemIds2' the
        input and output have a 'DuplicateIdMap2' whereas to align with the MFK project, 'validateStructureItemIds3'
        has a 'DuplicateIdStructure'.
        
        Use cases:
        The user sends in a structure for validation of the new ItemIds.  The input to this operation is the top
        BOMLine or the selected BOMLine, a structure of old item components to new ItemId and new ItemName for those
        Item objects that are already validated, the default naming scheme and a list of user defined projects to which
        the duplicated Item objects will be added.  Based on the structure traversal, the input structure, and the
        naming scheme this operation validates whether the proposed names for the un-validated Item objects are valid
        and whether the user can add the new structure to the list of user defined projects.
        """
        return cls.execute_soa_method(
            method_name='validateStructureItemIds3',
            library='StructureManagement',
            service_date='2011_06',
            service_name='Structure',
            params={'inputs': inputs},
            response_cls=ValidateStructureItemIdsResponse3,
        )

    @classmethod
    def duplicate3(cls, inputs: List[DuplicateInputInfo3]) -> DuplicateResponse:
        """
        This operation will create a duplicate (clone) of the input structure from its top level down or a selected sub
        assembly. 
         
        Depending on the user action, all or some of the original structure is duplicated and the rest is referenced. 
        The user has the option to de-select a sub assembly or leaf Item on the duplicate dialog.  Those Item objects
        that are not selected in the duplicate dialog will not be cloned but referenced from the original structure.  
        
        The user can define a specific naming pattern for the ItemIds of the duplicated (cloned) structure.  The user
        can define specific ItemIds for individually selected ItemRevision objects or a default naming pattern for the
        duplicated structure.   The default pattern can be defined by adding prefixes, suffixes or replacing part of
        the original name with a different pattern.  The user can also choose to allow the system to assign default ids.
        
        If project(s) have been passed in as input, the cloned structure is assigned to that project(s).  By default
        the projects to which the top BOMLine in the duplicate dialog belongs and to which the user has access, is used
        to populate the project list.  The user has the option to modify that list based on which projects are
        available to that user.
        
        All of the structure dependent data of the input structure like datasets and attachments are copied to the
        duplicated structure based on the Business Modeler IDE deep copy rules for 'SaveAs'.  The duplicate operation
        internally uses 'SaveAs' at every level of the structure; therefore it uses the 'SaveAs' deep copy rules.
        
        If the structure being cloned is a Requirements Manager structure, tracelink GRMs are handled based on the deep
        copy rules set for ReqRev for 'SaveAs'.  
        Target                             ReqRev
        Relation                           FND_TraceLink                
        Attached Type                ReqRev
        Operation                        SaveAs
        Action                             CopyAsReference
        Condition
        Direction                         IsTargetPrimary= false
        
        CAD specific attachments and relations are copied based on the transfer mode defined for the Business Modeler
        IDE global constant StructureCloneTransferModes.  The transfer mode contains dependent closure rules for
        expansion and cloning.  The value for the closure rules is added by the installed CAD system.
        For e.g. The closure rule defined for IPEM ProE integration (ipemSCloneClosureRule) looks like this:
        TYPE.ProPrt:CLASS.ItemRevision:RELATIONP2S.IPEM_master_dependency:PROCESS:PartFamilyMaster:R,
        TYPE.ProAsm:CLASS.ItemRevision:RELATIONP2S.IPEM_master_dependency:PROCESS:PartFamilyMaster:R,
        TYPE.ProPrt:CLASS.ItemRevision:RELATIONS2P.IPEM_master_dependency:PROCESS+TRAVERSE:PartFamilyMember, 
        
        Note: The difference between the three operations 'duplicate', 'duplicate2' and 'duplicate3' are the following:
        'duplicate' and 'duplicate2'
         - In 'duplicate' the input top BOMLine is the top BOMLine of the original configured structure in Structure
        Manager.  In 'duplicate2' the input top BOMLine is the selected BOMLine from the configured structure in
        Structure Manager or Systems Engineering.  i.e. the user can select to clone a sub-assembly of the original
        structure.
        - The input for 'duplicate2' includes project(s).  The cloned structure is assigned to those project(s). 
        'duplicate' does not have projects as input.
        
        'duplicate2' and 'duplicate3'
        - 'duplicate3' was created as a result of the Multi Field Key (MFK ) project.   The difference between
        'duplicate2' and 'duplicate3' is that in 'duplicate2' is that the input and output had a 'DuplicateIdMap2'
        whereas to align with the MFK project, 'duplicate3' has a 'DuplicateIdStructure'.
        
        
        Use cases:
        Use case1: Simple Clone
        A user has an assembly which does not have cad dependencies nor does it belong to a specific project(s).  The
        user wants to duplicate the entire structure with a specific naming pattern for the ItemIds.  The naming
        pattern is a prefix "test_".
        The user invokes the duplicate operation by passing in the top BOMLine of the structure to be cloned, and the
        naming pattern for the new structure.  The result is a new structure with the following naming pattern for the
        ItemIds -> test_OriginalItemId.
        
        Use case2: CAD Clone
        A user has an assembly structure which has cad dependencies.  The user wants to start a new product with a
        similar structure and cad dependencies.  The expansion and cloning rules have been defined in the Business
        Modeler IDE global constant StructureCloneTransferModes. 
        The user invokes the duplicate operation by passing in the top BOMLine of the structure to be cloned.  
        The user selects the cad dependency option Part Family Master.  The expansion and cloning will be done based on
        the closure rules defined for Part Family Master in the CAD closure rules.
        The "'Rename Cad Files'" will be passed to the CAD integration in a callback.  If the "'Rename Cad Files'", is
        set to true by the user, the cad files need to be renamed by the cad integration.
        The result will be a duplicated structure with the expected cad dependencies and it will open in the CAD tool
        without any errors.
        
        Use case3: Requirements Manager (Systems Engineering) clone:
        The user has a requirements manager structure with internal and/or external tracelink GRMs that need to be
        copied to the cloned structure.  The user defines a set of projects to which the newly cloned structure should
        belong.  The user does not want to clone the entire structure only a sub-assembly.
        The precondition to this operation, is that the deep copy rules for 'SaveAs' have been setup correctly
        The user invokes the duplicate operation by passing in the selected BOMLine of the sub structure to be cloned. 
        The projects to which the cloned structure should belong are passed in as input.  The naming rule for the
        ItemId is passed in.  
        The result is a requirement manager structure with the tracelink relations pointing to the correct objects in
        the new structure.  And the newly cloned structure belongs to the defined projects for which the user has
        permissions. 
        
        """
        return cls.execute_soa_method(
            method_name='duplicate3',
            library='StructureManagement',
            service_date='2011_06',
            service_name='Structure',
            params={'inputs': inputs},
            response_cls=DuplicateResponse,
        )

    @classmethod
    def expandOrUpdateDuplicateItems3(cls, opInput: List[ExpandOrUpdateDuplicateItemsInfo], selectionOption: int) -> ExpandOrUpdateDuplicateItemsResponse2:
        """
        This operation  is designed to expand structures one level at a time and get structure dependent data. When it
        is flagged for smart selection, it will try to solve the uncertain smart selection by expansion, in which case
        only qualified ItemRevision objects will be returned. This operation is used by the duplicate (clone) structure
        feature.  The dependencies have been defined to allow duplication of CAD dependent structure.  The
        'expandOrUpdateDuplicateItems3'  operation uses Business Modeler IDE global constant
        StructureCloneTransferModes to determine which  of the cad specific attachments and relationships can be
        expanded. This constant defines the transfer modes containing dependent closure rules for expansion and
        cloning.  The value for the closure rules is added by the installed CAD system.  For this version of the
        operation a mandatory clause has been added in the closure rules that removes the limit on one level of
        relationship traversal.   This was done to enhance the Duplicate functionality to ensure that the duplicated
        structure is CAD consistent.
        
        Note: The difference between 'expandOrUpdateDuplicateItems', 'expandOrUpdateDuplicateItems2' and
        'expandOrUpdateDuplicateItems3' is as follows:
        
        Difference in 'expandOrUpdateDuplicateItems' and 'expandOrUpdateDuplicateItems2'
        -    We allow the user to select a sub assembly for duplication.  There is a performance problem that was
        uncovered.  Even though a sub assembly is sent for duplication, traversal on the server side was happening from
        the top BOMLine of the structure.  To improve the performance we get a BOB object.
        
        -    The smart selection logic was added to decide whether to clone or reference an Item in a structure based
        on the project that the top line of the original structure belongs to.  This smart selection logic is bottom
        up, so if a child is selected based on project assignment, the parent will be selected, no matter whether the
        parent belongs to the top item project assignment or not.
        
        Difference in 'expandOrUpdateDuplicateItems2' and 'expandOrUpdateDuplicateItems3'
        The mandatory flag is passed back to the client.  When a cad option has been flagged with a mandatory flag, a
        "R" predicate in the closure rules, that option will come up in the Duplicate Dialog pre-checked and its
        selected status will be un-changeable.  This will prevent the user from un-checking those ItemRevision objects
        that were added in to make the structure cad consistent.  That is if a family table member in the assembly
        structure has been selected for duplication, then automatically include all its masters from the referenced
        ItemRevision all the way to the top master.  Including the masters automatically will only happen if the CAD
        closure rules are defined with a predicate "R" that says this CAD relation is mandatory for duplication. 
        
        
        Use cases:
        Use case 1: selectionOption is 0 and the original structure has cad data:
        The user sends in a structure for expansion, it will be expanded one level at a time and all dependent data
        will be returned based on the input and the value of the defined closure rule.  The input consists of the
        BOMLine for expansion and ItemRevision objects on which to perform the expansion,  the dependency types, and
        the selectionOption.  The ItemRevision objects could be null, in which case the ItemRevision object(s) gotten
        from the expansion of the BOMLine are used.  The dependency types are checked against the definition in the
        closure rules to determine  what dependent data is expanded. 
        
        Use case 2: selectionOption is 1 and the original structure has no cad data
        The user sends in a structure for expansion, it will be expanded one level at a time and all dependent data
        will be returned based on the input.  In this case no closure rule may be defined, since the structure has no
        cad data.   The input consists of the BOMLine for expansion and ItemRevision objects on which to perform the
        expansion,  the dependency types, and the selectionOption.  The ItemRevision objects could be null, in which
        case the ItemRevision object(s) gotten from the expansion of the BOMLine are used.  Since the selectionOption
        is 1, the input lines will be checked based on the top Use case 1: selectionOption is 0 and the original
        structure has cad data:
        The user sends in a structure for expansion, it will be expanded one level at a time and all dependent data
        will be returned based on the input and the value of the defined closure rule.  The input consists of the
        BOMLine for expansion and ItemRevision objects on which to perform the expansion,  the dependency types, and
        the selectionOption.  The ItemRevision objects could be null, in which case the ItemRevision object(s) gotten
        from the expansion of the BOMLine are used.  The dependency types are checked against the definition in the
        closure rules to determine  what dependent data is expanded. 
        """
        return cls.execute_soa_method(
            method_name='expandOrUpdateDuplicateItems3',
            library='StructureManagement',
            service_date='2011_06',
            service_name='Structure',
            params={'opInput': opInput, 'selectionOption': selectionOption},
            response_cls=ExpandOrUpdateDuplicateItemsResponse2,
        )
