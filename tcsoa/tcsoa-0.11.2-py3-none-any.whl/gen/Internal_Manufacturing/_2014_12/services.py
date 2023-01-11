from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Manufacturing._2013_12.ResourceManagement import GetStepP21FileCountsResponse, ImportStepP21FilesResponse
from tcsoa.gen.Internal.Manufacturing._2014_12.ResourceManagement import GetVendorCatalogInfo2Response
from tcsoa.gen.Internal.Manufacturing._2014_12.Model import LAResolveAsyncData, LABatchDetails, UILocationInfo, UILocationsInfoResponse, ScopeFlowInfo
from typing import List
from tcsoa.gen.Internal.Manufacturing._2014_12.IPAManagement import SearchDynamicIPAsResponse
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ResourceManagementService(TcService):

    @classmethod
    def getStepP21FileCounts2(cls, classIds: List[str], catalogRootDirectories: List[str]) -> GetStepP21FileCountsResponse:
        """
        For each identified class, this operation counts all STEP P21 tool component definition files that are stored
        below the specified Generic Tool Catalog vendor catalog root directory and belong to the identified class or
        any of its subclasses.
        """
        return cls.execute_soa_method(
            method_name='getStepP21FileCounts2',
            library='Internal-Manufacturing',
            service_date='2014_12',
            service_name='ResourceManagement',
            params={'classIds': classIds, 'catalogRootDirectories': catalogRootDirectories},
            response_cls=GetStepP21FileCountsResponse,
        )

    @classmethod
    def getVendorCatalogInfo2(cls, catalogTypes: int) -> GetVendorCatalogInfo2Response:
        """
        The multi-value preference "MRMGTCVendorCatalogRootDir" specifies one or more root directories where vendor
        tool catalogs may be stored on the Teamcenter server machine.
        This operation retrieves additional information about valid vendor catalogs contained in these root
        directories. It scans the given root directories for vendor catalogs of the requested type and returns detailed
        information for each valid catalog.
        """
        return cls.execute_soa_method(
            method_name='getVendorCatalogInfo2',
            library='Internal-Manufacturing',
            service_date='2014_12',
            service_name='ResourceManagement',
            params={'catalogTypes': catalogTypes},
            response_cls=GetVendorCatalogInfo2Response,
        )

    @classmethod
    def importStepP21Files2(cls, classId: str, catalogRootDirectory: str, importOptions: int) -> ImportStepP21FilesResponse:
        """
        This operation imports STEP P21 files containing tool component data pertaining to vendor tool catalogs into
        the Classification classes that represent those vendor tool catalogs inside the database. It creates Internal
        Classification objects (ICOs) in those classes, and associated data that represents the tool components.
        Depending on the contents of the vendor catalog directory, it also creates associated items, item revisions,
        datasets, and associated files to store drawings and images that further describe those tool components.
        """
        return cls.execute_soa_method(
            method_name='importStepP21Files2',
            library='Internal-Manufacturing',
            service_date='2014_12',
            service_name='ResourceManagement',
            params={'classId': classId, 'catalogRootDirectory': catalogRootDirectory, 'importOptions': importOptions},
            response_cls=ImportStepP21FilesResponse,
        )


class ModelService(TcService):

    @classmethod
    def getUILocations(cls, contextLines: List[BusinessObject]) -> UILocationsInfoResponse:
        """
        This operation reads the absolute occurrence (Mfg0AbsOcc) and user interface (UI) location (Mfg0UILocation)
        property of Mfg0UILocationForm form attached to the input BOPLine objects, gets the BOPLine corresponding to
        the absolute occurrence and returns the BOPLine along with the UI location. The input BOPLine objects can be of
        type Mfg0BvrProcess, Mfg0BvrOperation, Mfg0BvrWorkarea or Mfg0BvrProcessArea. 
        """
        return cls.execute_soa_method(
            method_name='getUILocations',
            library='Internal-Manufacturing',
            service_date='2014_12',
            service_name='Model',
            params={'contextLines': contextLines},
            response_cls=UILocationsInfoResponse,
        )

    @classmethod
    def laAsyncResolve(cls, laResolveData: LAResolveAsyncData) -> None:
        """
        This service operation resolves logical assignments for a given scope. This is an asynchronous operation.
        Logical assignments are defined on a process (MEProcess) or an operation (MEOP). These contain a user defined
        criteria which can be used to assign parts to these process(s)/operation(s). This operation automatically
        searches the product structure(s) for the parts that satisfy the criteria defined on the logical assignments
        and assigns them to the process/operation.
        """
        return cls.execute_soa_method(
            method_name='laAsyncResolve',
            library='Internal-Manufacturing',
            service_date='2014_12',
            service_name='Model',
            params={'laResolveData': laResolveData},
            response_cls=None,
        )

    @classmethod
    def saveUILocations(cls, uiLocationsInfo: List[UILocationInfo]) -> ServiceData:
        """
        This operation creates Mfg0UILocationForm and attaches it to MEAppearancePathNode of the input
        contextLine(BOPLine) using the Mfg0UILocationFormRel relationship and stores absolute occurrence and user
        interface(UI) location of the BOPLine objects contained in the externalNodeInfo structure. 
        """
        return cls.execute_soa_method(
            method_name='saveUILocations',
            library='Internal-Manufacturing',
            service_date='2014_12',
            service_name='Model',
            params={'uiLocationsInfo': uiLocationsInfo},
            response_cls=ServiceData,
        )

    @classmethod
    def scheduleLAResolve(cls, laResolveData: LAResolveAsyncData, batchDetails: LABatchDetails) -> ServiceData:
        """
        This service operation schedules an asynchronous service operation laAsyncResolve to be executed at a specific
        time. The operation is scheduled to execute once or a number of times depending on the information provided in
        the parameter batchDetails.
        Logical assignments (LAs) are defined on a process (MEProcess) or an operation (MEOP). These contain a user
        defined criteria which can be used to assign parts to these process(s)/operation(s). The service operation
        laAsyncResolve automatically searches the product structure(s) for the parts that satisfy the criteria defined
        on the logical assignments and assigns them to the process/operation.
        """
        return cls.execute_soa_method(
            method_name='scheduleLAResolve',
            library='Internal-Manufacturing',
            service_date='2014_12',
            service_name='Model',
            params={'laResolveData': laResolveData, 'batchDetails': batchDetails},
            response_cls=ServiceData,
        )

    @classmethod
    def deleteScopeFlows(cls, scopeFlowsInfo: List[ScopeFlowInfo]) -> ServiceData:
        """
        This operation removes the Mfg0BvrScopeFlow object and the Mfg0ScopeFlowPredRel relation between the input
        predecessor and the successor BOPLine objects.
        """
        return cls.execute_soa_method(
            method_name='deleteScopeFlows',
            library='Internal-Manufacturing',
            service_date='2014_12',
            service_name='Model',
            params={'scopeFlowsInfo': scopeFlowsInfo},
            response_cls=ServiceData,
        )


class IPAManagementService(TcService):

    @classmethod
    def searchDynamicIPAs(cls, searchScopes: List[BusinessObject], returnOnFirstResult: bool) -> SearchDynamicIPAsResponse:
        """
        This operation searches and returns the dynamic in-process assembly objects present in the hierarchy of the
        search input bop line objects.
        """
        return cls.execute_soa_method(
            method_name='searchDynamicIPAs',
            library='Internal-Manufacturing',
            service_date='2014_12',
            service_name='IPAManagement',
            params={'searchScopes': searchScopes, 'returnOnFirstResult': returnOnFirstResult},
            response_cls=SearchDynamicIPAsResponse,
        )
