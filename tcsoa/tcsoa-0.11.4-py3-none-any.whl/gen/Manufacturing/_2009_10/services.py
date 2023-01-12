from __future__ import annotations

from tcsoa.gen.Manufacturing._2009_10.ModelDefinitions import PropDescInfo, RelationTypesInput, GetValidRelationTypesResponse, AttachedPropDescsResponse
from tcsoa.gen.BusinessObjects import BusinessObject, StructureContext, WorkspaceObject
from tcsoa.gen.Manufacturing._2009_10.Model import ResolveData, ResolvedNodesInput, FlowResponse, FlowInput, LogicalAssignmentData, CalculateCriticalPathResponse, GetResolvedNodesFromLAResponse
from tcsoa.gen.Manufacturing._2009_10.MFGPropertyCollector import CollectPropertiesResponse, CollectPropertiesInputInfo
from tcsoa.gen.Manufacturing._2009_10.StructureManagement import CopyEBOPStructureResponse, GetStructureContextLinesResponse, PasteDuplicateStructureResponse
from tcsoa.gen.Manufacturing._2009_10.DataManagement import DisconnectInput, CreateResponse, CreateIn
from typing import List
from tcsoa.gen.Manufacturing._2009_10.StructureSearch import MFGSearchCriteria, StructureSearchResultResponse, SearchExpressionSet
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ModelService(TcService):

    @classmethod
    def getResolvedNodesFromLA(cls, inputObjects: List[ResolvedNodesInput]) -> GetResolvedNodesFromLAResponse:
        """
        This service returns the resolved nodes for each of the received Logical Assignment objects.
        """
        return cls.execute_soa_method(
            method_name='getResolvedNodesFromLA',
            library='Manufacturing',
            service_date='2009_10',
            service_name='Model',
            params={'inputObjects': inputObjects},
            response_cls=GetResolvedNodesFromLAResponse,
        )

    @classmethod
    def removeFlow(cls, input: List[BusinessObject]) -> ServiceData:
        """
        Removing existing Flow objects.
        """
        return cls.execute_soa_method(
            method_name='removeFlow',
            library='Manufacturing',
            service_date='2009_10',
            service_name='Model',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def resolveLogicalAssignments(cls, laVec: List[BusinessObject], resolveObjects: List[ResolveData], externalSources: List[BusinessObject]) -> ServiceData:
        """
        This service will resolve and re-resolve logical assignments to concrete assignments against the product
        structure.
        """
        return cls.execute_soa_method(
            method_name='resolveLogicalAssignments',
            library='Manufacturing',
            service_date='2009_10',
            service_name='Model',
            params={'laVec': laVec, 'resolveObjects': resolveObjects, 'externalSources': externalSources},
            response_cls=ServiceData,
        )

    @classmethod
    def createFlow(cls, input: List[FlowInput]) -> FlowResponse:
        """
        Create a new mfgFlow object between two mfg objects i.e process or operation
        """
        return cls.execute_soa_method(
            method_name='createFlow',
            library='Manufacturing',
            service_date='2009_10',
            service_name='Model',
            params={'input': input},
            response_cls=FlowResponse,
        )

    @classmethod
    def editLogicalAssignments(cls, laEditVec: List[LogicalAssignmentData]) -> ServiceData:
        """
        This service enables editing the values of Logical Assignment objects.
        """
        return cls.execute_soa_method(
            method_name='editLogicalAssignments',
            library='Manufacturing',
            service_date='2009_10',
            service_name='Model',
            params={'laEditVec': laEditVec},
            response_cls=ServiceData,
        )

    @classmethod
    def calculateCriticalPath(cls, roots: List[BusinessObject]) -> CalculateCriticalPathResponse:
        """
        Calculate the critical paths for MFGBVRProcess, MFGBVROperation or MFGBVRActivity and their corresponding APS
        objects.
        A critical path is the sequence of processes, operations or activities that determine the minimum duration of
        the root object. Thereby only those MFG objects will be considered that are either direct sub elements or
        implementers of the root object.
        """
        return cls.execute_soa_method(
            method_name='calculateCriticalPath',
            library='Manufacturing',
            service_date='2009_10',
            service_name='Model',
            params={'roots': roots},
            response_cls=CalculateCriticalPathResponse,
        )


class StructureManagementService(TcService):

    @classmethod
    def getStructureContextLines(cls, scList: List[StructureContext]) -> GetStructureContextLinesResponse:
        """
        Return the top lines and any selected lines if present.
        """
        return cls.execute_soa_method(
            method_name='getStructureContextLines',
            library='Manufacturing',
            service_date='2009_10',
            service_name='StructureManagement',
            params={'scList': scList},
            response_cls=GetStructureContextLinesResponse,
        )

    @classmethod
    def pasteDuplicateStructure(cls, srcLines: List[BusinessObject], targetLines: List[BusinessObject], copyRulesKey: str, copyFutureEffectivity: bool) -> PasteDuplicateStructureResponse:
        """
        clone the selected lines to each of the targetline supplied. The 2 input vectors are not related. Currently,
        this functionality is only for EBOP structures.
        """
        return cls.execute_soa_method(
            method_name='pasteDuplicateStructure',
            library='Manufacturing',
            service_date='2009_10',
            service_name='StructureManagement',
            params={'srcLines': srcLines, 'targetLines': targetLines, 'copyRulesKey': copyRulesKey, 'copyFutureEffectivity': copyFutureEffectivity},
            response_cls=PasteDuplicateStructureResponse,
        )

    @classmethod
    def copyEBOPStructure(cls, newRoot: WorkspaceObject, configuringEBOPWindow: BusinessObject, workingWindow: BusinessObject, copyRulesKey: str, copyFutureEffectivity: bool) -> CopyEBOPStructureResponse:
        """
         Creates a clone of the supplied root of the configuringEBOPWindow under the rootObject specified.
        """
        return cls.execute_soa_method(
            method_name='copyEBOPStructure',
            library='Manufacturing',
            service_date='2009_10',
            service_name='StructureManagement',
            params={'newRoot': newRoot, 'configuringEBOPWindow': configuringEBOPWindow, 'workingWindow': workingWindow, 'copyRulesKey': copyRulesKey, 'copyFutureEffectivity': copyFutureEffectivity},
            response_cls=CopyEBOPStructureResponse,
        )


class ModelDefinitionsService(TcService):

    @classmethod
    def getValidRelationTypes(cls, relationTypesInput: List[RelationTypesInput]) -> GetValidRelationTypesResponse:
        """
        This service returns a list of occurrence types that are valid for assignment between two received object types.
        """
        return cls.execute_soa_method(
            method_name='getValidRelationTypes',
            library='Manufacturing',
            service_date='2009_10',
            service_name='ModelDefinitions',
            params={'relationTypesInput': relationTypesInput},
            response_cls=GetValidRelationTypesResponse,
        )

    @classmethod
    def getManufacturingPropretyDescs(cls, inputs: List[PropDescInfo]) -> AttachedPropDescsResponse:
        """
        Get the attached property descriptor based on input type name and property names structure.
        """
        return cls.execute_soa_method(
            method_name='getManufacturingPropretyDescs',
            library='Manufacturing',
            service_date='2009_10',
            service_name='ModelDefinitions',
            params={'inputs': inputs},
            response_cls=AttachedPropDescsResponse,
        )


class MFGPropertyCollectorService(TcService):

    @classmethod
    def collectProperties(cls, input: List[CollectPropertiesInputInfo]) -> CollectPropertiesResponse:
        """
        This function will call a Mfg function that takes the MfgNode, traversal rules and property names to collect
        and return a list of property values of input properties for every MfgNode in the BOP structure based on
        traversal rules.
        """
        return cls.execute_soa_method(
            method_name='collectProperties',
            library='Manufacturing',
            service_date='2009_10',
            service_name='MFGPropertyCollector',
            params={'input': input},
            response_cls=CollectPropertiesResponse,
        )


class StructureSearchService(TcService):

    @classmethod
    def nextSearch(cls, searchCursor: BusinessObject) -> StructureSearchResultResponse:
        """
        Process one additional step of the search identified by the cursor.
        """
        return cls.execute_soa_method(
            method_name='nextSearch',
            library='Manufacturing',
            service_date='2009_10',
            service_name='StructureSearch',
            params={'searchCursor': searchCursor},
            response_cls=StructureSearchResultResponse,
        )

    @classmethod
    def startSearch(cls, scope: List[BusinessObject], searchExpression: SearchExpressionSet, mfgSearchCriteria: MFGSearchCriteria) -> StructureSearchResultResponse:
        """
        Start searching a structure for a given search expression within the scope specified.
        search can also be narrowed to a specific object type, item name, and logical designator
        """
        return cls.execute_soa_method(
            method_name='startSearch',
            library='Manufacturing',
            service_date='2009_10',
            service_name='StructureSearch',
            params={'scope': scope, 'searchExpression': searchExpression, 'mfgSearchCriteria': mfgSearchCriteria},
            response_cls=StructureSearchResultResponse,
        )

    @classmethod
    def stopSearch(cls, searchCursor: BusinessObject) -> StructureSearchResultResponse:
        """
        Stop and close down a search identified by a cursor.
        Throws SearchAlreadyStoppedException if the search has already been stopped.
        """
        return cls.execute_soa_method(
            method_name='stopSearch',
            library='Manufacturing',
            service_date='2009_10',
            service_name='StructureSearch',
            params={'searchCursor': searchCursor},
            response_cls=StructureSearchResultResponse,
        )


class DataManagementService(TcService):

    @classmethod
    def createObjects(cls, input: List[CreateIn]) -> CreateResponse:
        """
        Generic operation for creation of manufacturing objects. This will also create any secondary(compounded)
        objects that need to be created, assuming the CreateInput for the secondary object is represented in the
        recursive CreateInput object e.g. Item is Primary Object that also creates ItemMasterForm, ItemRevision and
        ItemRevision in turn creates ItemRevisionMasterForm. The input for all these levels is passed in through the
        recursive CreateInput object.
        This operation creates the persistent objects and the runtime objects accordingly. This operation also connects
        the created objects to the specified target. The connection will be done by the relation defined as default.
        """
        return cls.execute_soa_method(
            method_name='createObjects',
            library='Manufacturing',
            service_date='2009_10',
            service_name='DataManagement',
            params={'input': input},
            response_cls=CreateResponse,
        )

    @classmethod
    def disconnectObjects(cls, input: List[DisconnectInput]) -> ServiceData:
        """
        Generic operation to disconnect objects.
        """
        return cls.execute_soa_method(
            method_name='disconnectObjects',
            library='Manufacturing',
            service_date='2009_10',
            service_name='DataManagement',
            params={'input': input},
            response_cls=ServiceData,
        )
