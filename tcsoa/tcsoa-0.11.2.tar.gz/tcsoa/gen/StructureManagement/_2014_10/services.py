from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, ItemRevision
from tcsoa.gen.StructureManagement._2014_10.Structure import CloneStructureResponse, CloneStructureExpandOrUpdateItemsInfo, CloneStructureInputInfo, CloneStructureExpandOrUpdateResponse
from tcsoa.gen.StructureManagement._2014_10.MassUpdate import UpdateImpactedObjectEndResponse, UpdateImpactedObjectStartResponse, ManageImpactedObjectUpdateInput, ExecuteMarkupChangeResponse, ExecuteMarkupChangeInput, ImpactedObjectDetailsResponse, ImpactedObjectsQueryInput, UpdateImpactedObjectInput, ImpactedObjectsQueryResponse, ExpandOneLevelSearchScopeResponse, GetMarkupChangesForUpdateResponse, UpdateImpactedObjectResponse, ExpandOneLevelSearchScopeInput, ValidateChangeObjectForMassUpdateResponse, ManageImpactedObjectUpdatesResponse, GetRevisionRulesResponse, ImpactedObjectDetailsInput
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class MassUpdateService(TcService):

    @classmethod
    def getRevisionRules(cls, operation: int) -> GetRevisionRulesResponse:
        """
        This operation returns the list of valid revision rules applicable for specific mass update operation type.
        """
        return cls.execute_soa_method(
            method_name='getRevisionRules',
            library='StructureManagement',
            service_date='2014_10',
            service_name='MassUpdate',
            params={'operation': operation},
            response_cls=GetRevisionRulesResponse,
        )

    @classmethod
    def manageImpactedObjectUpdates(cls, input: List[ManageImpactedObjectUpdateInput]) -> ManageImpactedObjectUpdatesResponse:
        """
        This operation performs Add impacted object to or Remove impacted object from Change ItemRevision Markup as per
        the client request
        """
        return cls.execute_soa_method(
            method_name='manageImpactedObjectUpdates',
            library='StructureManagement',
            service_date='2014_10',
            service_name='MassUpdate',
            params={'input': input},
            response_cls=ManageImpactedObjectUpdatesResponse,
        )

    @classmethod
    def updateImpactedObjects(cls, input: List[UpdateImpactedObjectInput], updateRequestId: str) -> UpdateImpactedObjectResponse:
        """
        This operation performs an update on input impacted objects by replacing target ItemRevision with replacement
        ItemRevision. 
        """
        return cls.execute_soa_method(
            method_name='updateImpactedObjects',
            library='StructureManagement',
            service_date='2014_10',
            service_name='MassUpdate',
            params={'input': input, 'updateRequestId': updateRequestId},
            response_cls=UpdateImpactedObjectResponse,
        )

    @classmethod
    def updateImpactedObjectsEnd(cls, input: List[UpdateImpactedObjectInput]) -> UpdateImpactedObjectEndResponse:
        """
        This operation performs the post update cleanup activity. This operation should be called only once after all
        the update batches are executed using 'updateImpactedObjects'. If all the update batches are executed
        successfully then this operation deletes the markup associated with input change ItemRevision. 
        
        Use cases:
        - User wants to update the realizations saved on change ItemRevision. Operation 'getMarkupChangesForUpdate' is
        called by providing change ItemRevision as an input. This operation returns the Fnd0MarkupChange objects having
        information about impacted objects to be updated.
        - If the number of markup change objects is more than the update batch size then objects are updated in
        batches. Operation 'executeMarkupChanges' is then called per batch to update the batched markup change objects.
        This operation performs update on the impacted objects using information available on Fnd0MarkupChange objects.
        - Operation 'updateImpactedObjectsEnd' ends the update process and performs the cleanup activity if required.
        E.g. If the update is performed in context of change ItemRevision and if all the batches are executed
        successfully then this operation deletes the Fnd0Markup object associated with change ItemRevision in context
        of which the update has been performed. 
        
        """
        return cls.execute_soa_method(
            method_name='updateImpactedObjectsEnd',
            library='StructureManagement',
            service_date='2014_10',
            service_name='MassUpdate',
            params={'input': input},
            response_cls=UpdateImpactedObjectEndResponse,
        )

    @classmethod
    def updateImpactedObjectsStart(cls, input: List[UpdateImpactedObjectInput]) -> UpdateImpactedObjectStartResponse:
        """
        This operation builds the prerequisite information required to perform an update in batches. E.g. this
        operation generates an update request identifier that is used by all update batch requests. This operation
        should be called only once before calling the 'updateImpactedObjects' operation per batch.
        
        Use cases:
        - User wants to update the realizations (of a target ItemRevision) to a specific replacement ItemRevision. To
        do the update all impacted objects needs to be identified. Operation 'getImpactedObjects' is called by
        providing an input target ItemRevision as an input. This operation returns all the impacted objects.
        - Operation 'getImpactedObjectDetails' is then called by providing all the impacted objects as an input to
        check whether the impacted objects are modifiable or not.
        - User then selects the modifiable impacted objects to perform update upon them. If the number of selected
        impacted objects is more than the update batch size then impacted objects are updated in batches. Operation
        'updateImpactedObjectsStart' starts the update process with some preprocessing. e.g. operation
        'updateImpactedObjectsStart' builds the update request identifier that is common for all the subsequent update
        batch requests. Operation 'updateImpactedObjectsStart' should be called only once before calling the
        'updateImpactedObjects' operation per batch
        - Operation 'updateImpactedObjects' is then called per batch to update the batched impacted objects. This
        operation updates the impacted objects as per the input replacement ItemRevision.
        
        """
        return cls.execute_soa_method(
            method_name='updateImpactedObjectsStart',
            library='StructureManagement',
            service_date='2014_10',
            service_name='MassUpdate',
            params={'input': input},
            response_cls=UpdateImpactedObjectStartResponse,
        )

    @classmethod
    def validateChangeObjectForMassUpdate(cls, input: List[ItemRevision], massUpdateType: str) -> ValidateChangeObjectForMassUpdateResponse:
        """
        This operation validates the input change ChangeItemRevision object for a given Mass Update type. When invoked
        with "massUpdate" as an input, it validates whether the input ChangeItemRevision is valid for 'Mass Update'
        action. When invoked with "massUpdateRealization" as an input, it validates whether the input
        ChangeItemRevision is valid for 'Mass Update Realization' action.
        
        Use cases:
        Select ChangeItemRevision and perform 'Mass Update' or 'Mass Update Realization'. Operation
        'validateChangeObjectForMasUpdate' is invoked to validate whether the selected ChangeItemRevision is valid for
        the respective action 'Mass Update' or 'Mass Update Realization' initiated by the user.
        """
        return cls.execute_soa_method(
            method_name='validateChangeObjectForMassUpdate',
            library='StructureManagement',
            service_date='2014_10',
            service_name='MassUpdate',
            params={'input': input, 'massUpdateType': massUpdateType},
            response_cls=ValidateChangeObjectForMassUpdateResponse,
        )

    @classmethod
    def executeMarkupChanges(cls, input: List[ExecuteMarkupChangeInput]) -> ExecuteMarkupChangeResponse:
        """
        This operation executes the markup change objects corresponding to input Fnd0MarkupChange object UID list. Each
        markup change object holds the information like object to be modified, the input required for object
        modification and type of modification. When markup change object is executed, it modifies the required object
        with the help of information available on markup change object.
        
        Use cases:
        Execute markup changes associated with ChangeItemRevision
        - Invoke MassUpdate service operation getImpactedObjects by providing target ItemRevision. This API returns the
        list of impacted object UIDs.
        - Invoke MassUpdate service operation getImpactedObjectDetails by supplying the batch of impacted object UIDs.
        This API returns the information specifying whether each of the input impacted objects is modifiable or not.
        - Invoke MassUpdate service operation manageImpactedObjectUpdates providing the list of modifiable impacted
        objects and a ChangeItemRevision. This service operation when invoked with
        executionMode=murAddImpactedObjectToMarkup, adds the input impacted objects on the input ChangeItemRevision.
        - Invoke MassUpdate service operation getMarkupChangesForUpdate by providing a ChangeItemRevision as input. It
        returns the list of Fnd0MarkupChange object UIDs referenced by Fnd0Markup object associated with input
        ChangeItemRevision. 
        - Invoke MassUpdate service operation  executeMarkupChanges in loop by providing a batch of Fnd0MarkupChange
        objects UIDs until all the Fnd0MarkupChange UIDs are processed for execution. Once all the batches are executed
        successfully then delete the Fnd0Markup object associated with input ChangeItemRevision.
        
        """
        return cls.execute_soa_method(
            method_name='executeMarkupChanges',
            library='StructureManagement',
            service_date='2014_10',
            service_name='MassUpdate',
            params={'input': input},
            response_cls=ExecuteMarkupChangeResponse,
        )

    @classmethod
    def expandOneLevel(cls, input: List[ExpandOneLevelSearchScopeInput]) -> ExpandOneLevelSearchScopeResponse:
        """
        This operation expands the given parent product structure node to fetch its immediate children. A call to this
        operation is made when defining a search scope for impacted object search.
        """
        return cls.execute_soa_method(
            method_name='expandOneLevel',
            library='StructureManagement',
            service_date='2014_10',
            service_name='MassUpdate',
            params={'input': input},
            response_cls=ExpandOneLevelSearchScopeResponse,
        )

    @classmethod
    def getImpactedObjectDetails(cls, input: List[ImpactedObjectDetailsInput]) -> ImpactedObjectDetailsResponse:
        """
        This operation gathers the impacted object details required to perform mass update. Details like whether the
        impacted object is selectable for performing an update, if not selectable then the reason for it being
        non-selectable, whether the impacted object is out of date etc. is returned as an output response.
        """
        return cls.execute_soa_method(
            method_name='getImpactedObjectDetails',
            library='StructureManagement',
            service_date='2014_10',
            service_name='MassUpdate',
            params={'input': input},
            response_cls=ImpactedObjectDetailsResponse,
        )

    @classmethod
    def getImpactedObjects(cls, input: List[ImpactedObjectsQueryInput]) -> ImpactedObjectsQueryResponse:
        """
        This operation searches for product structure objects where  a given target ItemRevision is used.
        """
        return cls.execute_soa_method(
            method_name='getImpactedObjects',
            library='StructureManagement',
            service_date='2014_10',
            service_name='MassUpdate',
            params={'input': input},
            response_cls=ImpactedObjectsQueryResponse,
        )

    @classmethod
    def getMarkupChangesForUpdate(cls, input: List[ItemRevision]) -> GetMarkupChangesForUpdateResponse:
        """
        This operation queries Fnd0MarkupChange objects referenced by Fnd0Markup object associated with input
        ChangeItemRevision and returns UIDs of the Fnd0MarkupChange objects to the client.
        
        Use cases:
        Execute markup changes associated with ChangeItemRevision object
        - Invoke MassUpdate service operation getImpactedObjects by providing target ItemRevision. This operation
        returns the list of impacted object UIDs.
        - Invoke MassUpdate service operaion getImpactedObjectDetails by supplying the batch of impacted object UIDs.
        This API returns the information specifying whether each of the input impacted objects is modifiable or not.
        - Invoke MassUpdate service operation manageImpactedObjectUpdates providing the list of modifiable impacted
        objects and a ChangeItemRevision. This API when invoked with executionMode=murAddImpactedObjectToMarkup, adds
        the input impacted objects on the input ChangeItemRevision.
        - Invoke MassUpdate service operation getMarkupChangesForUpdate by providing a ChangeItemRevision as input. It
        returns the list of Fnd0MarkupChange object UIDs referenced by Fnd0Markup object associated with input
        ChangeItemRevision. 
        - Invoke MassUpdate service operation executeMarkupChanges in loop by providing a batch of Fnd0MarkupChange
        object UIDs until all the Fnd0MarkupChange UIDs are processed for execution.
        
        """
        return cls.execute_soa_method(
            method_name='getMarkupChangesForUpdate',
            library='StructureManagement',
            service_date='2014_10',
            service_name='MassUpdate',
            params={'input': input},
            response_cls=GetMarkupChangesForUpdateResponse,
        )


class StructureService(TcService):

    @classmethod
    def cloneStructure(cls, inputs: List[CloneStructureInputInfo]) -> CloneStructureResponse:
        """
        This operation validates and creates a duplicate (clone) of the input structure from its top level down or a
        selected sub assembly.
        
        Depending on the input arguments, all or some of the original structure is duplicated and the rest are
        referenced, revised or replaced.
        
        The caller can define a specific naming pattern for the Item ids of the duplicated (cloned) structure. The
        caller can define specific Item ids for individually selected ItemRevision objects or a default naming pattern
        for the duplicated structure. The default pattern can be defined by adding prefixes, suffixes or replacing part
        of the original name with a different pattern. The caller can also choose to allow the system to assign default
        ids.
        
        If project(s) have been passed in as input, the cloned structure is assigned to that project(s). By default the
        projects to which the top BOMLine in the duplicate dialog belongs and to which the user has access, is used to
        populate the project list. The user has the option to modify that list based on which projects are available to
        that user.
        
        All of the structure dependent data of the input structure like Datasets and attachments are copied to the
        duplicated structure based on the Business Modeler IDE Deep Copy Rules for SaveAs or the Deep Copy Data
        override rules parameter passed in to the input structure. The duplicate operation internally uses SaveAs at
        every level of the structure; therefore it uses the SaveAs Deep Copy Rules.
        
        If the structure being cloned is a Requirements Manager structure,Tracelink GRMs are handled based on the deep
        copy rules set for ReqRev for SaveAs.
        CAD specific attachments and relations are copied based on the transfer mode defined for the Business Modeler
        IDE global constant StructureCloneTransferModes. The transfer mode contains dependent closure rules for
        expansion and cloning. The value for the closure rules is added by the installed CAD system. 
        
        The caller can also tell the operation to just validate only and do not perform a duplicate of the input
        structures.
        
        Note: The difference between the operations duplicate4 and cloneStructure are the following:
        
        Duplicate4 and cloneStructure
        - cloneStructure was created as a result of the project to get NX CAD on board. The difference is
        cloneStructure will now process set based inputs, it combines the validate and duplicate actions into one API,
        provides a validate only mode, introduces the ability to override DeepCopyData GRM rules to change the core
        default DeepCopy rules behavior (with exception of restricted rules), the ability to choose the folder to store
        new cloned root item revisions into, added two new action types revise and replace along with the reference and
        clone action types for determining what to do with the children of the structure being cloned and  the
        cloneStructure will return all cloned mapping information to client if requested by cloneFlags.
        
        
        Use cases:
        Use case1: Simple Clone
        
        A user has an assembly which does not have cad dependencies nor does it belong to a specific project(s). The
        user wants to duplicate the entire structure with a specific naming pattern for the ItemIds. The naming pattern
        is a prefix "test_".
        The user invokes the duplicate operation by passing in the top BOMLine of the structure to be cloned, and the
        naming pattern for the new structure. The result is a new structure with the following naming pattern for the
        ItemIds -> test_OriginalItemId.
        
        Use case2: CAD Clone
        
        A user has an assembly structure which has cad dependencies. The user wants to start a new product with a
        similar structure and cad dependencies. The expansion and cloning rules have been defined in the Business
        Modeler IDE global constant StructureCloneTransferModes. 
        The user invokes the duplicate operation by passing in the top BOMLine of the structure to be cloned. 
        The user selects the cad dependency option Part Family Master. The expansion and cloning will be done based on
        the closure rules defined for Part Family Master in the CAD closure rules.
        The "Rename Cad Files" will be passed to the CAD integration in a callback. If the "Rename Cad Files", is set
        to true by the user, the cad files need to be renamed by the cad integration.
        The result will be a duplicated structure with the expected cad dependencies and it will open in the CAD tool
        without any errors.
        
        Use case3: Requirements Manager (Systems Engineering) clone:
        
        The user has a requirements manager structure with internal and/or external tracelink GRMs that need to be
        copied to the cloned structure. The user defines a set of projects to which the newly cloned structure should
        belong. The user does not want to clone the entire structure only a sub-assembly.
        The precondition to this operation, is that the deep copy rules for SaveAs have been setup correctly
        The user invokes the duplicate operation by passing in the selected BOMLine of the sub structure to be cloned.
        The projects to which the cloned structure should belong are passed in as input. The naming rule for the ItemId
        is passed in. 
        The result is a requirement manager structure with the tracelink relations pointing to the correct objects in
        the new structure. And the newly cloned structure belongs to the defined projects for which the user has
        permissions.
        
        Use Case 4: Validate and Duplicate Process with Revise and Replace Child Component Options
        
        A user has an assembly to start a new product with a similar structure but wants to replace and revise some
        components for the new structure. The user will need to select the components to revise from the client
        interface and mark those selected as a revise action to be recorded in the data map. Then the user will need to
        select the components to replace from the client interface and enter an existing component to be the replacing
        component for the components selected for replace. The replacing action will also be recorded in the data map.
        The results will be a cloned structure where the children selected for replace and revise will be replaced and
        revised in the new cloned structure.
        
        Use Case 5: Validate Only Mode
        
        A user has an assembly and wants to validate it before trying to clone it. User selects the assembly structure
        and selects the "Validate Only"  option.
        The results is the structure will run through a validation routine and not be cloned at all. The information of
        the validation will be returned to the client where the user then can fix any issues or proceed with the
        cloning.
        
        Use Case 6: Run In Background Mode
        
        A user has a very large assembly and wants to clone it in background mode so they can free up there client
        interface to perform other work. The user selects the assembly structure and selects the "Run In Background" 
        option.
        The system will return a message saying the job was dispatched. Then the system will validate the structure
        against the input provided and then duplicate the structure in an Asynchronous Teamcenter server thread. The
        results of the "Run In Background" process will be recorded in a text dataset that will be sent to the user via
        Teamcenter Mail Envelope.
        
        Use Case 7: Simple Validate and Duplicate Process And Return Cloned Data to Client
        
        A user has an assembly and wants to the cloned information to be returned to the client. The user selects the
        assembly structure and sets the "return cloned object information"  option for the cloneFlags.
        The results of the "return cloned object information " option will be returned to the client.
        Note: The "return cloned object information " option is primarily used for CAD Integrations to resolve there
        internal part to part links that Teamcenter would not know about. The RAC Duplicate Dialog does not use this
        option.
        """
        return cls.execute_soa_method(
            method_name='cloneStructure',
            library='StructureManagement',
            service_date='2014_10',
            service_name='Structure',
            params={'inputs': inputs},
            response_cls=CloneStructureResponse,
        )

    @classmethod
    def cloneStructureAsync(cls, inputs: List[CloneStructureInputInfo]) -> None:
        """
        This operation validates and creates a duplicate (clone) of the input structure from its top level down or a
        selected sub assembly. This operation runs asynchronously in its own server in the background.
        
        Depending on the input arguments, all or some of the original structure is duplicated and the rest is
        referenced, revised or replaced.
        
        The caller can define a specific naming pattern for the Item ids of the duplicated (cloned) structure. The
        caller can define specific Item ids for individually selected ItemRevision objects or a default naming pattern
        for the duplicated structure. The default pattern can be defined by adding prefixes, suffixes or replacing part
        of the original name with a different pattern. The caller can also choose to allow the system to assign default
        ids.
        
        If project(s) have been passed in as input, the cloned structure is assigned to that project(s). All of the
        structure dependent data of the input structure like Datasets and attachments are copied to the duplicated
        structure based on the Business Modeler IDE Deep Copy Rules for SaveAs or the Deep Copy Data override rules
        parameter passed in to the input structure. The duplicate operation internally uses SaveAs at every level of
        the structure; therefore it uses the SaveAs Deep Copy Rules.
        
        If the Systems Engineering/Requirements Manager structure, has tracelink GRMs they will be handled based on the
        deep copy rules set for ReqRev for SaveAs.
        
        CAD specific attachments and relations are copied based on the transfer mode defined for the Business Modeler
        IDE global constant StructureCloneTransferModes. The transfer mode contains dependent closure rules for
        expansion and cloning. The value for the closure rules is added by the installed CAD system. 
        
        Any errors during this operation will be captured and recorded in a Text dataset and attached to a Teamcenter
        Mail Envelop that will be sent to the user who initiated the process.
        
        Notes:
        
        
        
                -cloneStructureAsync was created as a result of the project to get NX CAD on board. The difference is
        cloneStructureAsync will now process set based inputs, it combined the validate and duplicate actions into one
        API, provides a validate only mode, introduces the ability to override DeepCopyData GRM rules to change the
        core default DeepCopy rules behavior (with exception of restricted rules), the ability to choose the folder to
        store new cloned root item revisions into, added 2 new action types revise and replace along with the reference
        and clone action types for determining what to do with the children of the structure being cloned.
        
        Use cases:
        A user has a very large assembly and wants to clone it in background mode so they can free up there client
        interface to perform other work. The user selects the assembly structure and selects the "Run In Background" 
        option.
        The system will then do the following:
        - A Message will be displayed to the user that the job was sent to the dispatcher.
        - The dispatcher will then send a Teamcenter Mail Envelope to the user informing them the Asynchronous
        Duplicate process has started. Note: if Teamcenter Mail is configured to send e-mails the user will then
        receive an e-mail stating the job has started.
        - The system will the start the validation and duplication of the structure.
        - When the duplicate process is done another Teamcenter Mail Envelope is sent to the user saying the duplicate
        process has completed. Also attached to the Mail Envelope is the new cloned toplevel item revision and a text
        dataset with information that was captured during the validate and duplicate process. Note: if Teamcenter Mail
        is configured to send e-mails the user will then receive an e-mail stating the job has completed.
        
        """
        return cls.execute_soa_method(
            method_name='cloneStructureAsync',
            library='StructureManagement',
            service_date='2014_10',
            service_name='Structure',
            params={'inputs': inputs},
            response_cls=None,
        )

    @classmethod
    def cloneStructureExpandOrUpdate(cls, opInput: List[CloneStructureExpandOrUpdateItemsInfo], selectionOption: int) -> CloneStructureExpandOrUpdateResponse:
        """
        This operation expand structures one level at a time and gets structure dependent data.
        
        When the 'selectionOption" is set to "1" for smart selection, it will try to solve the uncertain smart
        selection by expansion, in which case only qualified ItemRevision objects will be returned.
        
        The following are the CAD Dependency options the user can use when expanding or Updating a structure to be
        cloned.
        - Drawings
        - Required
        - PartFamilyMaster
        - PartFamilyMember
        - AllDep
        - Internal
        
        
        
        The CAD Dependency options correspond with the CAD Dependency rules defined by the Business Modeler IDE global
        constant "StructureCloneTransferModes". The CAD specific rules defined in the "StructureCloneTransferModes"
        will determine which of the CAD specific attachments and relationships can be expanded and included as part of
        the structure to be cloned. The values for the closure rules is added by the installed CAD system.
        
        Note: The differences between expandOrUpdateDuplicateItems3 and cloneStructureExpandOrUpdate are as follows:
        - The CAD options passed into this operation are now strings and no longer integers.
        - The cloneStructureExpandOrUpdate API calls a DuplicateExpandOrUpdate Business Object operation.The new
        Business Object operation allows CAD integrations to register extension code to identify CAD specific
        "Internal" relations to a structure being duplicated that are not published to Teamcenter.
        
        
        
        Use cases:
        Use case 1: selectionOption is 0 and the original structure has CAD data:
        
        The user sends in a structure for expansion, it will be expanded one level at a time and all dependent data
        will be returned based on the input and the value of the defined closure rule. The input consists of the
        BOMLine for expansion and ItemRevision objects on which to perform the expansion, the dependency types, and the
        selectionOption. The ItemRevision objects could be null, in which case the ItemRevision object(s) gotten from
        the expansion of the BOMLine are used. The dependency types are checked against the definition in the closure
        rules to determine what dependent data is expanded. 
        
        Use case 2: selectionOption is 1 and the original structure has no CAD data
        
        The user sends in a structure for expansion, it will be expanded one level at a time and all dependent data
        will be returned based on the input. In this case no closure rule may be defined, since the structure has no
        CAD data. The input consists of the BOMLine for expansion and ItemRevision objects on which to perform the
        expansion, the dependency types, and the selectionOption. The ItemRevision objects could be null, in which case
        the ItemRevision object(s) gotten from the expansion of the BOMLine are used. Since the selectionOption is 1,
        the input lines will be checked based on the top.
        """
        return cls.execute_soa_method(
            method_name='cloneStructureExpandOrUpdate',
            library='StructureManagement',
            service_date='2014_10',
            service_name='Structure',
            params={'opInput': opInput, 'selectionOption': selectionOption},
            response_cls=CloneStructureExpandOrUpdateResponse,
        )

    @classmethod
    def toggleOccurrenceSuppression(cls, inputs: List[BOMLine]) -> ServiceData:
        """
        This operation toggles occurrence suppression of the selected lines. 
        
        Use cases:
        User wants to suppress some lines after the structure is constructed, user can call this operation to toggle
        the occurrence suppression of the lines.
        """
        return cls.execute_soa_method(
            method_name='toggleOccurrenceSuppression',
            library='StructureManagement',
            service_date='2014_10',
            service_name='Structure',
            params={'inputs': inputs},
            response_cls=ServiceData,
        )

    @classmethod
    def togglePrecision(cls, inputs: List[BOMLine]) -> ServiceData:
        """
        This operation toggles precision of all lines.
        Note: 
        -    leaf lines cannot change precision.
        -    If multiple lines for same item revision are passed in to the operation, the precision for the structure
        of the lines will be changed only once. 
        
        
        Use cases:
        User wants to change precision of some lines after the structure is constructed, user can call this operation
        to toggle the precisions of the lines.
        """
        return cls.execute_soa_method(
            method_name='togglePrecision',
            library='StructureManagement',
            service_date='2014_10',
            service_name='Structure',
            params={'inputs': inputs},
            response_cls=ServiceData,
        )
