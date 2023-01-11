from __future__ import annotations

from tcsoa.gen.Manufacturing._2014_06.DataManagement import EstablishOriginLinkInfo, CloneAssemblyInputData, CloneAssemblyResponse, AddOrRemoveContextsInfo, EstablishOriginLinkResponse, ProcResourceResponseInfo
from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Manufacturing._2014_06.ResourceManagement import CheckToolParametersResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.gen.Manufacturing._2014_06.StructureSearch import SrchConnectedLinesResponse
from tcsoa.base import TcService


class ResourceManagementService(TcService):

    @classmethod
    def checkToolParameters(cls, icoIds: List[str], checkLevel: str, checkTypes: List[str]) -> CheckToolParametersResponse:
        """
        This operation checks for a list of tools if they define the required attribute values to create their 3D
        graphics or use them as cutters in NX CAM.  The list of tools is identified by their internal classification
        object IDs (ICO IDs).   The caller can select the level and type of checking that gets performed. The operation
        will return a check result consisting of a status and report for each tool  being checked.
        """
        return cls.execute_soa_method(
            method_name='checkToolParameters',
            library='Manufacturing',
            service_date='2014_06',
            service_name='ResourceManagement',
            params={'icoIds': icoIds, 'checkLevel': checkLevel, 'checkTypes': checkTypes},
            response_cls=CheckToolParametersResponse,
        )


class DataManagementService(TcService):

    @classmethod
    def cloneAssemblyAndProcessObjects(cls, input: List[CloneAssemblyInputData]) -> CloneAssemblyResponse:
        """
        This operation clones an assembly in manufacturing Bill of Material (mBOM) as a reaction to changes in
        engineering BOM (eBOM) planning or clones a process in Bill Of Processes as a reaction to changes in mBOM
        planning. As a result of this operation, the original assembly/process is cloned and occurrence effectivity is
        set correctly on both original and cloned assembly/process.
        
        For eBOM-mBOM cloning some of the parts from the new assembly in the mBOM are replaced with the new parts that
        were introduced to the eBOM as a replacement in that unit effectivity.
        
        For mBOM-BOP cloning the process that used to refer to the original assembly in the mBOM is cloned and all
        references are fixed to point at the new assembly.
        
        Use cases:
        Clone subassembly with effectivity Use Case.
        Use Case Description:
        In this use case, the user detects changes in the eBOM, and would like to make the appropriate changes to the
        Mbom. The changes entail cloning the target assembly where the parts are in the mBom.
        Use Case Goal:
        Handle changes in eBOM by creating the appropriate stock-able assembly in the mBom.
        
        Description:
        This use case may be regarded as a direct continuation of the Clone assembly with effectivity Use Case. In this
        use case, the user continues to handle the change, by cloning the process to which the "original" assembly was
        assigned (and its hierarchy), and fixing all internal references to the new copy.
        Use Case Goals:
        Handle changes in mBom by creating the appropriate structure to consume it in the BOP.
        
        """
        return cls.execute_soa_method(
            method_name='cloneAssemblyAndProcessObjects',
            library='Manufacturing',
            service_date='2014_06',
            service_name='DataManagement',
            params={'input': input},
            response_cls=CloneAssemblyResponse,
        )

    @classmethod
    def addOrRemoveAssociatedContexts(cls, input: List[AddOrRemoveContextsInfo]) -> ServiceData:
        """
        Generic operation to set or remove different kinds of associations. 
        The input parameter to the operation governs the target context to associate to, list of source contexts, the
        relation name to associate or disassociate with and the additional action required to add or remove the context.
        
        
        Use cases:
        - Use Case 1: Add the origin link between the Generic Bill Of Processes (BOP) and Product BOP or Product BOP
        and Plant BOP.
        
        
                Description: An origin link (association) can be added between Generic BOP and Product BOP or Product
        BOP and Plant BOP.
        
        - Use Case 2: Remove the origin link between the Generic BOP and Product BOP or Product BOP and Plant BOP.
        
        
                Description: An origin link can be removed between Generic BOP and Product BOP or Product BOP and Plant
        BOP. 
        
        - Use Case 3: Remove the origin link and allocations between BOPs
        
        
                Description: After removing the origin link between Generic BOP and Product BOP or Product BOP and
        Plant BOP, the user will have an option to remove the origin link between the allocations. Also the user will
        have option to remove the allocated  operations or processes. 
        """
        return cls.execute_soa_method(
            method_name='addOrRemoveAssociatedContexts',
            library='Manufacturing',
            service_date='2014_06',
            service_name='DataManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def establishOriginLink(cls, input: EstablishOriginLinkInfo) -> EstablishOriginLinkResponse:
        """
        This service operation establishes the origin link between process and/or operations. It can directly establish
        origin link between the input source (process and/or operation from Generic Bill Of Process (BOP) or Product
        BOP and target(s) (process and/or operation from Product BOP or Plant BOP. 
        The input parameter to the operation governs whether origin link need to be established or it's simply a dry
        run, whether hierarchy should be considered and the criteria based on which the origin link is established.
        
        Use cases:
        - Use case 1 : Establish origin link between Process/Operation.
        
        
        Description : An origin link can be established between Process/Operation where source is a process/operation
        from Generic BOP or Product BOP and targets are the processes/operations from Product BOP or Plant BOP. The
        input parameter "action" must be specified as "Link".
        
        - Use case 2 : Dry-run without establishing the origin link.
        
        
        Description : This service can identify the candidate targets to be linked to the process/operation from
        Generic BOP or Product BOP to the processes/operations from Product BOP or Plant BOP on the basis of the
        provided criteria. The input parameter "action" must be specified as "DryRun".
        """
        return cls.execute_soa_method(
            method_name='establishOriginLink',
            library='Manufacturing',
            service_date='2014_06',
            service_name='DataManagement',
            params={'input': input},
            response_cls=EstablishOriginLinkResponse,
        )

    @classmethod
    def getProcessResourceRelatedInfo(cls, input: List[BusinessObject], objectPreference: str) -> ProcResourceResponseInfo:
        """
        This service operation fetches the information related to process resource (work content performed by
        resource(s) in a manufacturing plant ) and the operation/process that are allocated/unallocated to
        process-resource. The operation takes object for which information is required. The object can be process
        station, process line, process area, or process resource. The object must be in the context of Plant Bill of
        Processes (BOP).
        
        Use cases:
        Use Case 1: Fetching process resource for a given process area.
        This operation can be used to fetch the process resource of specific process area. In context of a Plant BOP,
        this operation can be called on the process area BOM line. In response, all the process lines and process
        stations under the process area are fetched apart from  process resources for each process station and
        allocated/unallocated operations/processes. The result is populated on a view providing information on process
        resources, process station it belongs to and allocated/unallocated operations/processes.
        
        Use Case 2: Fetching processes/operations for a given process resource.
        This operation can be used to fetch the process/operation that are allocated to process resource. 
        In context of a Plant BOP, this operation can be called on the process resource BOM line. In response, all
        allocated/unallocated operations/processes are fetched. The result is populated on a view providing information
        on process resources and allocated operations/processes.
        
        Use Case 3: Fetching processes/operaions that are not allocated to process resource for a given process area 
        and process
        This operation can be used to fetch the process/operation that are not allocated to process resource. In
        context of a Plant BOP, this operation can be called on the process area or process BOM line. In response, all
        unallocated operations/processes are fetched. The result is populated on a view providing information on
        process resources and unallocated operations/processes.
        """
        return cls.execute_soa_method(
            method_name='getProcessResourceRelatedInfo',
            library='Manufacturing',
            service_date='2014_06',
            service_name='DataManagement',
            params={'input': input, 'objectPreference': objectPreference},
            response_cls=ProcResourceResponseInfo,
        )


class StructureSearchService(TcService):

    @classmethod
    def searchConnectedLines(cls, inputConnLines: List[BusinessObject]) -> SrchConnectedLinesResponse:
        """
        This operation searches and returns the connected BOMLine objects for the input connection BOMLine objects.
        """
        return cls.execute_soa_method(
            method_name='searchConnectedLines',
            library='Manufacturing',
            service_date='2014_06',
            service_name='StructureSearch',
            params={'inputConnLines': inputConnLines},
            response_cls=SrchConnectedLinesResponse,
        )
