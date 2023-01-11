from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, BOMEdit
from tcsoa.gen.ChangeManagement._2008_06.ChangeManagement import FindContextDataInputs, GetAllChangeHomeFolderResponse, CreateChangeItemInputs, GetBOMEditResponse, UpdateSupercedureData, CreateBOMEditInput, CreateChangeItemsResponse, FindContextDataResponse, FindSupersedureResponse, ConfigureChangeSearchData, GetBOMEditInput, CreateSupercedureInput, CreateBOMEditResponse, CreateSupercedureResponse, UpdateChangeProperties
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ChangeManagementService(TcService):

    @classmethod
    def createSupercedures(cls, supercedureProperties: List[CreateSupercedureInput]) -> CreateSupercedureResponse:
        """
        This operation creates Supercedure objects for each 'CreateSupercedureInput' supplied. A Supercedure represents
        a relation that graphically displays the deleted components and the new components that replace them. Transfer
        Supercedure is a specific type that is created where a component is transferred from one assembly to another
        level in a different assembly.
        
        Use cases:
        An assembly modification results in the components being added to or removed from the assembly. Supercedure is
        a component replacement where a user specifically marks one or more added components with one or more removals.
        This use case is accomplished by the 'createSupercedure' operation. The Supercedure is created from:
        - The original product structure 
        - The new product structure which is currently being edited in response to change.
        
        """
        return cls.execute_soa_method(
            method_name='createSupercedures',
            library='ChangeManagement',
            service_date='2008_06',
            service_name='ChangeManagement',
            params={'supercedureProperties': supercedureProperties},
            response_cls=CreateSupercedureResponse,
        )

    @classmethod
    def deleteSupercedures(cls, supercedureTobeDeleted: List[BusinessObject]) -> ServiceData:
        """
        This operation deletes the Supercedures specified as the input parameter. A Supercedure defines the
        relationship between any number of additions or deletions implemented within a Bill of Material (BOM) assembly.
        The 'deleteSupercedures' enables a user to remove a Supercedure or delete a BOM add/cancel from a Supercedure.
        
        Use cases:
        A user can delete the supercedures by calling the 'deleteSupercedures' which takes in the list of Supercedure
        objects as input parameter.
        """
        return cls.execute_soa_method(
            method_name='deleteSupercedures',
            library='ChangeManagement',
            service_date='2008_06',
            service_name='ChangeManagement',
            params={'supercedureTobeDeleted': supercedureTobeDeleted},
            response_cls=ServiceData,
        )

    @classmethod
    def findContextData(cls, findcontextRequest: List[FindContextDataInputs]) -> FindContextDataResponse:
        """
        This operation provides a flexible way of retrieving objects or data for a variety of contexts to satisfy the
        RichClient usability requirements for BOM Change, Supersedure, and Genealogy in Teamcenter Structure Manager. 
        There are helper functions in the RichClient to facilitate the consumption and conversion of the retrieved
        information.  In other words, this operation may pose challenges to users of this operation who are unfamiliar
        with the intended usage of the returned details.  For RichClient developers, it is better to use the helper
        functions instead.
        The context is specified by the context string 'contextRelName' of an input structure, and based on the
        specified context, different input arguments can be supplied via a change revision object reference, and/or a
        pair of generic business object references.  The objects or data returned will be captured in an output
        structure.  The following are the possible values for the context string:
        - CM_impacted_of_solution
        - CM_associated_change
        - CM_supersedure_of_bomedit
        - CM_bomedits_of_occ
        - CM_supersedures_of_solution
        - CM_get_supersedures_of_bomcancel
        - CM_get_supersedures_of_bomadd
        - CM_get_first_supersedure
        - CM_get_pure_adds_cancels
        - CM_get_supersedure_for_WU
        - CM_get_pureAddsCancels_for_WU
        - CM_get_change_of_supersedure
        - CM_get_initial_rendering_details
        - CM_refresh_rendering_without_supersedure
        - CM_refresh_rendering_with_supersedure
        - CM_get_bomline_adds
        - CM_get_bomline_cancels
        
        
        
        Use cases:
        Use Case 1: Finding the impacted item given a change revision and a solution item
        For the input structure 'FindContextDataInputs',use CM_impacted_of_solution for 'contextRelName', supply the
        change revision as 'changeRev' and the solution item as 'primaryContextInputData'.  The requested impacted item
        can be found in the object list 'contextOutputData' of the corresponding output structure
        'FindContextDataOutput'.
        Use Case 2: Finding the associated change revision given a solution item
        For the input structure 'FindContextDataInputs',use CM_associated_change for 'contextRelName', supply the
        solution item as 'primaryContextInputData'.  The requested associated change revision can be found in the
        'changeRev' of the corresponding output structure 'FindContextDataOutput'.
        Use Case 3: Finding the supersedure given a BOMEdit object
        For the input structure 'FindContextDataInputs',use CM_supersedure_of_bomedit for 'contextRelName', supply the
        BOMEdit object as 'primaryContextInputData'.  The requested supersedure can be found in the object list of the
        corresponding output structure 'FindContextDataOutput'.
        Use Case 4: Finding all the BOMEdit objects associated with a given Occurrence
        For the input structure 'FindContextDataInputs',use CM_bomedits_of_occ for 'contextRelName', supply the
        occurrence object as 'primaryContextInputData'.  The requested BOMEdit object can be found in the object list
        of the corresponding output structure 'FindContextDataOutput'.
        Use Case 5: Finding all supersedures created for a given solution item
        For the input structure 'FindContextDataInputs',use CM_supersedures_of_solution for 'contextRelName', supply
        the solution item as 'primaryContextInputData'.  The requested supersedure objects can be found in the object
        list 'contextOutputData' of the corresponding output structure 'FindContextDataOutput'.
        Use Case 6: Finding all the supersedures associated with a given BOMEdit of type cancel
        For the input structure 'FindContextDataInputs',use CM_get_supersedures_of_bomcancel for 'contextRelName',
        supply the BOMEdit object as 'primaryContextInputData'.  The requested supersedure objects can be found in the
        object list 'contextOutputData' of the corresponding output structure 'FindContextDataOutput'.
        Use Case 7: Finding all the supersedures associated with a given BOMEdit of type add
        For the input structure 'FindContextDataInputs',use CM_get_supersedures_of_bomadd for 'contextRelName', supply
        the BOMEdit object as 'primaryContextInputData'.  The requested supersedure objects can be found in the object
        list 'contextOutputData' of the corresponding output structure 'FindContextDataOutput'.
        Use Case 8: Finding the first supersedure given a change object and a BOM line
        For the input structure 'FindContextDataInputs',use CM_get_first_supersedure for contextRelName, supply the
        change revision as changeRev and the BOM line as 'primaryContextInputData'.  The requested first supersedure
        can be found in the object list 'contextOutputData' of the corresponding output structure
        'FindContextDataOutput'.
        Use Case 9: Finding the Pure Adds and Pure Cancels for a given BOM line
        For the input structure 'FindContextDataInputs',use CM_get_pure_adds_cancels for 'contextRelName', supply the
        BOM line as 'primaryContextInputData'.  The requested Pure Adds and Pure Cancels can be found in the object
        list 'contextOutputData' of the corresponding output structure 'FindContextDataOutput'.  The list of
        vBomEditCount can be used to sort out the Adds and the Cancels.
        Use Case 10: Finding the first supersedure for a given bom line in the context of a whereused assembly
        For the input structure 'FindContextDataInputs',use CM_get_supersedure_for_WU for 'contextRelName', supply the
        BOM line as 'primaryContextInputData' and the whereused assembly as 'secondaryContextInputData'.  The requested
        first supersedure can be found in the object list 'contextOutputData' of the corresponding output structure
        'FindContextDataOutput'.
        Use Case 11: Finding all the Pure Adds and Pure Cancels for a given bom line in the context of a whereused
        assembly
        For the input structure 'FindContextDataInputs',use CM_get_pureAddsCancels_for_WU for 'contextRelName', supply
        the BOM line as 'primaryContextInputData' and the whereused assembly as 'secondaryContextInputData'.  The
        requested Pure Adds and Pure Cancels can be found in the object list 'contextOutputData' of the corresponding
        output structure 'FindContextDataOutput'.  The list of vBomEditCount can be used to sort out the Adds and the
        Cancels.
        Use Case 12: Finding the associated change revision given a supersedure
        For the input structure 'FindContextDataInputs',use CM_get_change_of_supersedure for 'contextRelName', supply
        the supersedure as 'primaryContextInputData'.  The requested associated change revision can be found in the
        'changeRev' of the corresponding output structure 'FindContextDataOutput'.
        Use Case 13: Finding all the BOM lines and the supersedures given a change revision and a pair of BOM windows
        representing the solution and the impacted items.
        For the input structure 'FindContextDataInputs',use CM_get_initial_rendering_details for 'contextRelName',
        supply the change revision as 'changeRev', the BOM windlow for the solution item as 'primaryContextInputData'
        and the BOM windlow for the impacted item as 'secondaryContextInputData'.  The requested BOM lines can be found
        in the object list 'contextOutputData' of the corresponding output structure 'FindContextDataOutput'.
        Use Case 14: Finding all the solution BOM lines and the impacted BOM lines given a change revision and an Add
        line and a Cancel line without including the supersedure data
        For the input structure 'FindContextDataInputs',use CM_refresh_rendering_without_supersedure for
        contextRelName, supply the change revision as 'changeRev', the Add line as 'primaryContextInputData' and the
        Cancel line as 'secondaryContextInputData'.  The requested BOM lines can be found in the object list of the
        corresponding output structure.
        Use Case 15: Finding all the solution BOM lines and the impacted BOM lines given a change revision and an Add
        line and a Cancel line including the supersedure data
        For the input structure 'FindContextDataInputs',use CM_refresh_rendering_with_supersedure for 'contextRelName',
        supply the change revision as 'changeRev', the Add line as 'primaryContextInputData' and the Cancel line as
        'secondaryContextInputData'.  The requested BOM lines can be found in the object list of the corresponding
        output structure. 
        Use Case 16: Finding all the Add BOM lines for a given supersedure
        For the input structure 'FindContextDataInputs',use CM_get_bomline_adds for 'contextRelName', supply the
        supersedure as 'primaryContextInputData'.  The requested Add BOM lines can be found in the object list
        'contextOutputData' of the corresponding output structure.
        Use Case 17: Finding all the Cancel BOM lines for a given supersedure
        For the input structure 'FindContextDataInputs',use CM_get_bomline_cancels for 'contextRelName', supply the
        supersedure as 'primaryContextInputData'.  The requested Cancel BOM lines can be found in the object list of
        the corresponding output structure.
        
        
        """
        return cls.execute_soa_method(
            method_name='findContextData',
            library='ChangeManagement',
            service_date='2008_06',
            service_name='ChangeManagement',
            params={'findcontextRequest': findcontextRequest},
            response_cls=FindContextDataResponse,
        )

    @classmethod
    def findSupersedure(cls, bomedit: List[BOMEdit]) -> FindSupersedureResponse:
        """
        This operation finds the Supersedures based on the BOMEdits supplied as input. A BOM change which encompasses a
        BOM Add or a BOM delete enables a Supersedure to be created. A user can create a Supersedure which defines the
        additions and deletions within a BOM.
        
        Use cases:
        Use case 1: Create Supercedures
        An assembly modification results in the components being added to or removed from the assembly. Supercedure is
        a component replacement where a user specifically marks one or more added components with one or more removals.
        The Supercedure is created from:
        - The original product structure 
        - The new product structure which is currently being edited in response to change.
        
        
        Use case 2: Find Supersedures
        Finding a BOM Supersedure can be accomplished by calling the 'findSupersedure' for each input 'bomeditRequest'.
        """
        return cls.execute_soa_method(
            method_name='findSupersedure',
            library='ChangeManagement',
            service_date='2008_06',
            service_name='ChangeManagement',
            params={'bomedit': bomedit},
            response_cls=FindSupersedureResponse,
        )

    @classmethod
    def getAllChangeHomeFolders(cls) -> GetAllChangeHomeFolderResponse:
        """
        This operation returns a list of all Change Home folders.  This operation is created to support the Change Home
        UI in Change Manager.  Change Home allows users to define their own set of folders whose contents are
        determined by the searches/queries that are executed when the folders are expanded.  When Change Home is being
        opened, this operation is used to retrieve the folders that are defined for use by the current user.  Change
        Home will then display them based on their settings.
        
        Use cases:
        Retreiving a list of all Change Home folders for the user
        Where there is a need to retrieve all the Change Home folders for the current user session, this operation can
        be invoked via an instance of the 'ChangeManagementService'.  No parameters are required.  The response of the
        operation is captured in the form of 'GetAllChangeHomeFolderResponse'.  It is important to note that the
        folders retrieved will include BOTH those defined at the site level as well as those defined at the user level.
         Site level folders are available to all users, whereas user level folders are only available to the current
        user.  The caller program can make intelligent use of the list by inspecting the details of each individual
        folder that are captured within the structure 'ConfigureChangeSearchData'.
        """
        return cls.execute_soa_method(
            method_name='getAllChangeHomeFolders',
            library='ChangeManagement',
            service_date='2008_06',
            service_name='ChangeManagement',
            params={},
            response_cls=GetAllChangeHomeFolderResponse,
        )

    @classmethod
    def getBOMEdits(cls, bomeditRequest: List[GetBOMEditInput]) -> GetBOMEditResponse:
        """
        This operation is to support the BOM Change tab in Change Manager which displays the details of the BOM Change
        associated with the selected change revision in the Open Change View.
        
        Use cases:
        Finding all BOMEdit objects for a given change revision
        When there is a need to find all BOMEdit objects of a certain type for a given change revision, this operation
        can be invoked via an instance of the 'ChangeManagementService'.  The caller program needs to be aware of all
        the possible types (as represented by 'bomEditType' in the 'GetBOMEditInput' structure) of BOMEdit in order to
        process the returned objects correctly.  It is important to note that a 'PSBOMViewRevision' object for the
        solution item will need to be located and supplied as the 'affectedBvr' element within the 'GetBOMEditInput'
        structure.  Any BOMEdit objects found will be captured in the list of 'GetBOMEditOutput' structures of the
        'GetBOMEditResponse'.
        """
        return cls.execute_soa_method(
            method_name='getBOMEdits',
            library='ChangeManagement',
            service_date='2008_06',
            service_name='ChangeManagement',
            params={'bomeditRequest': bomeditRequest},
            response_cls=GetBOMEditResponse,
        )

    @classmethod
    def updateChangeItems(cls, updateProps: List[UpdateChangeProperties]) -> ServiceData:
        """
        Updates a vector of change items by using the inputs provided in the argument
        returns the updated objects via the services data.
        """
        return cls.execute_soa_method(
            method_name='updateChangeItems',
            library='ChangeManagement',
            service_date='2008_06',
            service_name='ChangeManagement',
            params={'updateProps': updateProps},
            response_cls=ServiceData,
        )

    @classmethod
    def updateSupercedures(cls, supercedureTobeUpdated: List[UpdateSupercedureData]) -> ServiceData:
        """
        This operation updates Supercedures for each 'UpdateSupercedureData' supplied. The 'UpdateSupercedureData'
        contains information for properties such as bomAddorCancelFlag, operation, tags and the supTag which specifies
        the Supercedure business object to be updated. A Supercedure represents a relation that graphically displays
        the deleted components and new components that replace them. Once a Supercedure is created, new BOM elements
        can be added or removed which allows the user to indicate the Supercedure to be edited and updated.
        
        Use cases:
        Use case1: Create Supercedures
        An assembly modification results in the components being added to or removed from the assembly. Supercedure is
        a component replacement where a user specifically marks one or more added components with one or more removals.
        This use case is accomplished by the operation createSupercedure with the input structure
        'CreateSupercedureInput' utilizing a list of Supercedure properties. The Supercedure is created from:
        - The original product structure 
        - The new product structure which is currently being edited in response to change.
        
        
        Use case2: Update Supercedures
        An existing Supercedure can be updated at point in time and this is achieved by the operation
        'updateSupercedures'. This operation checks if the operation is of type ADD or CANCEL and correspondingly adds
        or deletes a list of business objects from the Supercedure business object specified in the input parameter.
        The input structure elements utilize the Change Management BOM_ADD/BOM_CANCEL and
        OPERARTION_TYPE_ADD/OPERATION_TYPE_CANCEL constants in the SOA based on which a decision is made by the user to
        append or remove components from the assembly.
        """
        return cls.execute_soa_method(
            method_name='updateSupercedures',
            library='ChangeManagement',
            service_date='2008_06',
            service_name='ChangeManagement',
            params={'supercedureTobeUpdated': supercedureTobeUpdated},
            response_cls=ServiceData,
        )

    @classmethod
    def configureChangeSearches(cls, input: List[ConfigureChangeSearchData]) -> ServiceData:
        """
        Add or remove a change specific searches folder with the given inputs.  This operation is created to support
        the Manage Saved Search capability for Change Home within Change Manager.  It is important to note that, if
        called directly, there is a possibility of overwriting any pre existing configurations for Change Home, at site
        and/or user level.  So, USE IT WITH CAUTION.
        
        Use cases:
        Adding and Removing change home folder(s)
        This can be accomplished by calling the 'configureChangeSearches' operation with a list of
        'ConfigureChangeSearchData' structures which specify a number of necessary attributes of the folders to be
        created or removed.  Each 'ConfigureChangeSearchData' structure will contain the name of the folder (which
        should be unique), a visible/invisible indicator, the saved search/query associated with the folder, any query
        criteria and their corresponding values, a site/user level indicator, and an add/remove operation indicator.  A
        site level folder is available to all site users, whereas a user level folder is available only to the user of
        the current user session.  The add/remove operation indicator will determine if the operation is to add or to
        remove the folder.
        """
        return cls.execute_soa_method(
            method_name='configureChangeSearches',
            library='ChangeManagement',
            service_date='2008_06',
            service_name='ChangeManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def createBOMEdits(cls, bomEditRequest: List[CreateBOMEditInput]) -> CreateBOMEditResponse:
        """
        This operation is to support the creation of BOM Change in Structure Manager.  A number of BOMEdit objects are
        created when the solution item BOMViewRevision (BVR) is saved and then compared to the impacted item BVR in two
        side by side BOM windows.  Central to this operation is the change revision object that ties all the BOMEdit
        objects together to represent the whole BOM Change.
        
        Use cases:
        Creating a BOM Change within the Structure Manager
        A change revision has been created with an identified impacted item.  A user working on a solution will first
        revise the impacted item, relate the new revision to the change revision as solution item, and then make
        structural changes to the new revision in Structure Manager. When the work is complete, the solution item is
        saved.   The save operation will detect if the object saved is associated with a change revision as the
        solution item.  If it is, it will proceed to render the solution item and the impacted item in two side by side
        BOM windows, and then invoke the 'createBOMEdits' operation via an instance of the 'ChangeManagementService'
        with the 'CreateBOMEditInput' structure that contains the associated change revision and the two BOM windows .
        """
        return cls.execute_soa_method(
            method_name='createBOMEdits',
            library='ChangeManagement',
            service_date='2008_06',
            service_name='ChangeManagement',
            params={'bomEditRequest': bomEditRequest},
            response_cls=CreateBOMEditResponse,
        )

    @classmethod
    def createChangeItems(cls, changeItemProps: List[CreateChangeItemInputs]) -> CreateChangeItemsResponse:
        """
        Creates an list of Change Items of specified type and any associated data with each change item including
        Change Item Revision,
        Change Item Master Form, and Change Item Revision Master form based on the input attribute structures.
        Also it creates relationship between the objects passed as in input properties and assigns created change item
        to a specified
        user as requestor, analyst, admin or role that is specified in the input.
        It also updates any additional properties of the change item that is passed in the input.
        If the relation data contains a change item an attempt will be made to propagate values from this parent change
        item to
        the newly create item based on the propagation rules defined in the change configuration also an attempt will
        be made to
        create the prpoer types of relations between the change item that is created and input objects.
        Incase of Problem Report (PR) if the CMRoles is empty the requestor of the PR will be the same as the creator
        of the PR.
        """
        return cls.execute_soa_method(
            method_name='createChangeItems',
            library='ChangeManagement',
            service_date='2008_06',
            service_name='ChangeManagement',
            params={'changeItemProps': changeItemProps},
            response_cls=CreateChangeItemsResponse,
        )
