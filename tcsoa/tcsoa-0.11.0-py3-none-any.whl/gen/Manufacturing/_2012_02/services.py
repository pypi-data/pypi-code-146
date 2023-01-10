from __future__ import annotations

from tcsoa.gen.Manufacturing._2012_02.DataManagement import AssociateAndAllocateInput, AssociateAndAllocateResponse, AllocationMap, ConnectObjectResponse, GetAssociatedContextsInputData, AssociationResponse, AutomaticAllocatePreviewResponse, DisconnectFromOriginInputData, AddAssociationInput, ConnectObjectsInputData
from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Manufacturing._2012_02.Model import ResolveDataInfo, CandidateToolsForToolRequirement, ToolRequirementResponse, ToolRequirementInput
from tcsoa.gen.Manufacturing._2012_02.IPAManagement import DeleteFilteredIPAInputInfo, GetFilteredIPATypeResponse
from tcsoa.gen.Manufacturing._2012_02.Constraints import ValidateProcessAreaAssignmentsResponse, ValidateConstraintConsistencyInputs, ValidateConstraintConsistencyResponse, GetPrecedenceConstraintsResponse, GetPrecedenceConstraintPathsInputs, ValidateProcessAreaAssignmentsInputs, GetPrecedenceConstraintsIn, GetPrecedenceConstraintPathsResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def addAssociatedContexts(cls, input: List[AddAssociationInput]) -> ServiceData:
        """
        Generic operation for setting different kinds of associations. It could be between Plant BOP and Product BOP
        (Leading Plant BOP in the future), Product (root) and Process (root) structures, regular Plant (Workarea)
        (root) and Process (root) structures, EBOM-MBOM. For now we will use it as threshold for Plant BOP and Product
        BOP. Other types are defined as target.
        This SOA will be used for add operation. Remove/disconnect (future) will be implemented in separate SOA.
        """
        return cls.execute_soa_method(
            method_name='addAssociatedContexts',
            library='Manufacturing',
            service_date='2012_02',
            service_name='DataManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def connectObjects(cls, input: List[ConnectObjectsInputData]) -> ConnectObjectResponse:
        """
        Generic operation for connecting MFG nodes      
        int        quantityNum - number of BOMLines to create (used in paste special). Default value is 1.
        int        occurrenceNumber - for packed lines. Number of occurrences to create (used in paste special).
        Default value is 1.
        int        findNumber - find number. Always passed by client.
        """
        return cls.execute_soa_method(
            method_name='connectObjects',
            library='Manufacturing',
            service_date='2012_02',
            service_name='DataManagement',
            params={'input': input},
            response_cls=ConnectObjectResponse,
        )

    @classmethod
    def disconnectFromOrigin(cls, inputVector: List[DisconnectFromOriginInputData]) -> ServiceData:
        """
        Disconnects objects and their children from their origin relation. Origin relation is created when the objects
        are assigned from the Product BOP/Generic BOP to the Plant BOP/Product BOP. This functionality removes the
        origin relation created during the assignment. Also this functionality can be called recursively for the
        processes below. This functionality can return an error in the following conditions, the object on which
        disconnect function was called called does not have an origin in case of non-recursive calls. This error will
        have a severity level of information. And This functionality is not available on this type of object only
        ProcessAreas, WorkAreas, Partitions, Processes and Operations type objects are expected.
        """
        return cls.execute_soa_method(
            method_name='disconnectFromOrigin',
            library='Manufacturing',
            service_date='2012_02',
            service_name='DataManagement',
            params={'inputVector': inputVector},
            response_cls=ServiceData,
        )

    @classmethod
    def associateAndAllocateByPreview(cls, input: AssociateAndAllocateInput, allocationMap: AllocationMap) -> AssociateAndAllocateResponse:
        """
        This function is the second function call in case a preview is required for automatic allocation this function
        does the actual allocation from Source Product BOP to a Target Plant BOP on the basis of a Reference Product
        BOP. This is done by passing the allocation map back to the server which we recived in the 
        automaticAllocatePreview command. This function also associates the Source Product BOP with the Target Plant
        BOP in case they are not associated. This function can throw the following exceptions, Reference Product BOP is
        not linked to the Target Plant BOP and Some allocation from the source structure to the target structure were
        unsuccessful please see the log for more details. Both these error messages will have the severity level of
        error.
        """
        return cls.execute_soa_method(
            method_name='associateAndAllocateByPreview',
            library='Manufacturing',
            service_date='2012_02',
            service_name='DataManagement',
            params={'input': input, 'allocationMap': allocationMap},
            response_cls=AssociateAndAllocateResponse,
        )

    @classmethod
    def getAssociatedContexts(cls, input: List[GetAssociatedContextsInputData]) -> AssociationResponse:
        """
        Returns associated contexts with the input context
        """
        return cls.execute_soa_method(
            method_name='getAssociatedContexts',
            library='Manufacturing',
            service_date='2012_02',
            service_name='DataManagement',
            params={'input': input},
            response_cls=AssociationResponse,
        )

    @classmethod
    def automaticAllocatePreview(cls, input: AssociateAndAllocateInput) -> AutomaticAllocatePreviewResponse:
        """
        This function is the first function call in case a preview is required for automatic allocation from Source
        Product BOP to a Target Plant BOP on the basis of a Reference Product BOP. This function finds the allocated
        lines from the reference product BOP to the Plant BOP and equivalent lines in the source Product BOP and
        generates a preview for the automatic allocation in CSV format . Also this function returns an allocationMap,
        which needs to be sent back to server in case the user wants to go ahead with the allocation , for which it
        calls the second server call associateAndAllocateMap command . This function can throw the following
        exceptions, Reference Product BOP is not linked to the Target Plant BOP . This error messages will have
        severity level of error.
        """
        return cls.execute_soa_method(
            method_name='automaticAllocatePreview',
            library='Manufacturing',
            service_date='2012_02',
            service_name='DataManagement',
            params={'input': input},
            response_cls=AutomaticAllocatePreviewResponse,
        )

    @classmethod
    def automaticAssociateAndAllocate(cls, input: AssociateAndAllocateInput) -> AssociateAndAllocateResponse:
        """
        This function is a single call function that does the allocation from Source Product BOP to a Target Plant BOP
        on the basis of a Reference Product BOP. This function finds the allocated lines from the reference product BOP
        to the Plant BOP and equivalent lines in the source Product BOP and does the allocation from the Source Product
        BOP to the Target Plant BOP in a single call. This function also associates the Source Product BOP with the
        Target Plant BOP in case they are not associated. This function can throw the following exceptions, Reference
        Product BOP is not linked to the Target Plant BOP and Some allocation from the source structure to the target
        structure were unsuccessful please see the log for more details. Both these error messages will have the
        severity level of error.
        """
        return cls.execute_soa_method(
            method_name='automaticAssociateAndAllocate',
            library='Manufacturing',
            service_date='2012_02',
            service_name='DataManagement',
            params={'input': input},
            response_cls=AssociateAndAllocateResponse,
        )


class ModelService(TcService):

    @classmethod
    def getToolRequirements(cls, parentObject: List[BusinessObject], toolRequirementStatus: List[str]) -> ToolRequirementResponse:
        """
        Fetches the Tool Requirement for the given operation or process. Based on the status of the Tool Requirement.
        either all. resolved or unresolved Tool Requirements are returned. The respective options for the status are
        ALL. RESOLVED and UNRESOLVED.
        Note that the Tool requirement assigned to child operation or process is not considered.
        """
        return cls.execute_soa_method(
            method_name='getToolRequirements',
            library='Manufacturing',
            service_date='2012_02',
            service_name='Model',
            params={'parentObject': parentObject, 'toolRequirementStatus': toolRequirementStatus},
            response_cls=ToolRequirementResponse,
        )

    @classmethod
    def resolveToolRequirement(cls, resolveObjects: List[ResolveDataInfo]) -> ServiceData:
        """
        Resolves the Tool Requirement with the provided tool. As a result the Tool is assigned to the Tool Requirement
        and to the Operation for which Tool Requirement is defined. This resolve operation  is allowed only in the
        Plant BOP.
        """
        return cls.execute_soa_method(
            method_name='resolveToolRequirement',
            library='Manufacturing',
            service_date='2012_02',
            service_name='Model',
            params={'resolveObjects': resolveObjects},
            response_cls=ServiceData,
        )

    @classmethod
    def updateFlows(cls, input: List[BusinessObject], isSubHierarchies: bool) -> ServiceData:
        """
        Updates flows between the children of input object(s) based on Find number value. Input objects should be an
        instance of BOM line. This service does not return any resulting or affected objects. The client needs to
        update cache of affected objects manually(children of the input object are affected ). If isSubHierarchies
        parameter is true, flows are recursively updated for all children.
        """
        return cls.execute_soa_method(
            method_name='updateFlows',
            library='Manufacturing',
            service_date='2012_02',
            service_name='Model',
            params={'input': input, 'isSubHierarchies': isSubHierarchies},
            response_cls=ServiceData,
        )

    @classmethod
    def getCandidateToolsForToolRequirement(cls, resolveObjects: List[ToolRequirementInput]) -> CandidateToolsForToolRequirement:
        """
        Gets the candidate tools against which Tool Requirement could be resolved. The candidate tools are fetched
        based on the search criteria specified on the Tool Requirement. The input parameter tool source specifies the
        source from where candidate tools are supposed to be fetched.  The candidate tool can be fetched only in the
        Plant BOP.
        """
        return cls.execute_soa_method(
            method_name='getCandidateToolsForToolRequirement',
            library='Manufacturing',
            service_date='2012_02',
            service_name='Model',
            params={'resolveObjects': resolveObjects},
            response_cls=CandidateToolsForToolRequirement,
        )


class ConstraintsService(TcService):

    @classmethod
    def validateConstraintConsistency(cls, inputData: List[ValidateConstraintConsistencyInputs]) -> ValidateConstraintConsistencyResponse:
        """
        This SOA invokes the consistency check service. It checks whether the constraints defined in the product BOP or
        a sub structure thereof are consistent.
        """
        return cls.execute_soa_method(
            method_name='validateConstraintConsistency',
            library='Manufacturing',
            service_date='2012_02',
            service_name='Constraints',
            params={'inputData': inputData},
            response_cls=ValidateConstraintConsistencyResponse,
        )

    @classmethod
    def validateProcessAreaAssignments(cls, inputData: List[ValidateProcessAreaAssignmentsInputs]) -> ValidateProcessAreaAssignmentsResponse:
        """
        This SOA invokes the constraint validation service. It checks whether the assignments of operations or
        processes of a Product BOP to process areas in a Plant BOP are consistent with the constraint definitions.
        """
        return cls.execute_soa_method(
            method_name='validateProcessAreaAssignments',
            library='Manufacturing',
            service_date='2012_02',
            service_name='Constraints',
            params={'inputData': inputData},
            response_cls=ValidateProcessAreaAssignmentsResponse,
        )

    @classmethod
    def getPrecedenceConstraintPaths(cls, inputData: List[GetPrecedenceConstraintPathsInputs]) -> GetPrecedenceConstraintPathsResponse:
        """
        Returns all operations/processes in the precedence chain starting from the given start operation/process up to
        the end operation/process, i.e., all operations/processes succeeding the start operation/process and preceding
        the end operation/process.
        """
        return cls.execute_soa_method(
            method_name='getPrecedenceConstraintPaths',
            library='Manufacturing',
            service_date='2012_02',
            service_name='Constraints',
            params={'inputData': inputData},
            response_cls=GetPrecedenceConstraintPathsResponse,
        )

    @classmethod
    def getPrecedenceConstraints(cls, inputData: List[GetPrecedenceConstraintsIn]) -> GetPrecedenceConstraintsResponse:
        """
        Fetches all precedence constraints defined on the given input objects - traverses 'm' levels in the predecessor
        chain and 'n' levels in the successor chain
        """
        return cls.execute_soa_method(
            method_name='getPrecedenceConstraints',
            library='Manufacturing',
            service_date='2012_02',
            service_name='Constraints',
            params={'inputData': inputData},
            response_cls=GetPrecedenceConstraintsResponse,
        )


class IPAManagementService(TcService):

    @classmethod
    def deleteFilteredIPA(cls, input: List[DeleteFilteredIPAInputInfo]) -> ServiceData:
        """
        This API will delete the filtered IPA(s) under the process depending on the boolean member "isRecursive" of the
        input structure.
        If " isRecursive" is true, then all the filtered IPAs in the hierarchy of the member "process" will be deleted.
        Else just one filtered IPA directly under the process will be deleted.
        """
        return cls.execute_soa_method(
            method_name='deleteFilteredIPA',
            library='Manufacturing',
            service_date='2012_02',
            service_name='IPAManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def getFilteredIPAType(cls, processes: List[BusinessObject]) -> GetFilteredIPATypeResponse:
        """
        For each process, return the type of the FIPA used for this process structure. 
        For processes from the same process structure, the answer is the same. Therefore, from perforemence point of
        view, it is better to pass the process context (topline) as an input, instead of sending several processes from
        the same structure.
        """
        return cls.execute_soa_method(
            method_name='getFilteredIPAType',
            library='Manufacturing',
            service_date='2012_02',
            service_name='IPAManagement',
            params={'processes': processes},
            response_cls=GetFilteredIPATypeResponse,
        )
