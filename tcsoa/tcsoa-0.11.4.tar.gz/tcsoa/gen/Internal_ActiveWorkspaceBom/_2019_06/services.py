from __future__ import annotations

from tcsoa.gen.Internal.ActiveWorkspaceBom._2019_06.OccurrenceManagement import OccurrencesData2, OccurrencesResp2, RequestPreference2, PackElementsResp, CloneContentData, UserContextState2, InfoForAddElemResp2, InfoForAddElemData2, AddObjectResp2, AddObjectData2, PackElementsData
from tcsoa.gen.Internal.ActiveWorkspaceBom._2019_06.Compare import CompareContentAsyncData2
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class OccurrenceManagementService(TcService):

    @classmethod
    def addObject2(cls, input: AddObjectData2) -> AddObjectResp2:
        """
        This operation adds an object to a product as specified in Awb0ProductContextInfo or parent Awb0Element and
        creates Awb0Element representing newly created object. The new object is added as a sibling to the selected
        Awb0Element if that is provided in input. The Awb0ProductContextInfo and parent Awb0Element can be retrieved
        using getOccurrences.
        
        Use cases:
        User loads the product structure in Content. The Content is used for smart navigation of occurrences in a
        structure. User selects an occurrence in the Content and clicks on Add button. This actions will add a new
        occurrence as a child or sibling of the selected occurrence.
        """
        return cls.execute_soa_method(
            method_name='addObject2',
            library='Internal-ActiveWorkspaceBom',
            service_date='2019_06',
            service_name='OccurrenceManagement',
            params={'input': input},
            response_cls=AddObjectResp2,
        )

    @classmethod
    def cloneContent(cls, inputs: List[CloneContentData]) -> ServiceData:
        """
        This operation validates and clones content depending on the input criteria.
        
        If the clone operation type requested by the caller is not supported then the system will default to "Clone"
        operation for that line.
        The caller can define a specific naming pattern for the Item IDs for cloned structure. The default pattern can
        be defined by adding prefixes, suffixes or replacing part of the original name with a different pattern. The
        caller can also choose to allow the system to assign default ids. If input has insufficient or incorrect
        information then system will send an error in service data.
        """
        return cls.execute_soa_method(
            method_name='cloneContent',
            library='Internal-ActiveWorkspaceBom',
            service_date='2019_06',
            service_name='OccurrenceManagement',
            params={'inputs': inputs},
            response_cls=ServiceData,
        )

    @classmethod
    def cloneContentAsync(cls, inputs: List[CloneContentData]) -> None:
        """
        This operation performs asynchronous clone of the content depending on the input criteria.
        
        If the clone operation type requested by the caller is not supported then the system will default to "Clone"
        operation for that line.
        
        The caller can define a specific naming pattern for the Item IDs for cloned structure. The default pattern can
        be defined by adding prefixes, suffixes or replacing part of the original name with a different pattern. The
        caller can also choose to allow the system to assign default ids. If input has insufficient or incorrect
        information then system will send an error in service data.
        """
        return cls.execute_soa_method(
            method_name='cloneContentAsync',
            library='Internal-ActiveWorkspaceBom',
            service_date='2019_06',
            service_name='OccurrenceManagement',
            params={'inputs': inputs},
            response_cls=None,
        )

    @classmethod
    def getInfoForAddElement2(cls, getInfoForElementIn: InfoForAddElemData2) -> InfoForAddElemResp2:
        """
        This operation retreives information required for creating an Awb0Element under product specified in
        Awb0Element. The operation also returns allowable type name(s) to search existing object through Full Text
        Search. The preferred type is the parent type if that is allowed.This operation also indicates if allowable
        type is of Occurrence type.
        
        Use cases:
        &bull;    Returns the allowed child types for given parent type as Item or sub-types.
        &bull;    Returns the allowed child occurrence types for given parent type as ProductItem.
        &bull;    Returns the allowed child occurrence types for given parent type as occurrence.
        &bull;    Returns the allowed related object types for the given occurrence type.
        """
        return cls.execute_soa_method(
            method_name='getInfoForAddElement2',
            library='Internal-ActiveWorkspaceBom',
            service_date='2019_06',
            service_name='OccurrenceManagement',
            params={'getInfoForElementIn': getInfoForElementIn},
            response_cls=InfoForAddElemResp2,
        )

    @classmethod
    def getOccurrences2(cls, inputData: OccurrencesData2) -> OccurrencesResp2:
        """
        Retrieves the page of configured occurrences for given the top-level product and configuration parameters as
        input. The service provides the facility to optionally filter and sort the result by additional filters and
        sorting criteria that may be provided as input. The output also contains a cursor that defines the place to
        start the next page location. The cursor must be passed back in to any subsequent call to get the next page of
        occurrences.
        
        Exceptions:
        >Teamcenter::Soa::Server::ServiceException
        """
        return cls.execute_soa_method(
            method_name='getOccurrences2',
            library='Internal-ActiveWorkspaceBom',
            service_date='2019_06',
            service_name='OccurrenceManagement',
            params={'inputData': inputData},
            response_cls=OccurrencesResp2,
        )

    @classmethod
    def packSimilarElements(cls, input: PackElementsData) -> PackElementsResp:
        """
        The operation provides the "pack" or "unpack" functionality on a set of Awb0Element objects.
        """
        return cls.execute_soa_method(
            method_name='packSimilarElements',
            library='Internal-ActiveWorkspaceBom',
            service_date='2019_06',
            service_name='OccurrenceManagement',
            params={'input': input},
            response_cls=PackElementsResp,
        )

    @classmethod
    def saveUserWorkingContextState2(cls, contextState: UserContextState2, requestPref: RequestPreference2) -> ServiceData:
        """
        This operation saves current user's client state information for the opened object. The saved information is
        used to establish user's working state while opening the object again.
        """
        return cls.execute_soa_method(
            method_name='saveUserWorkingContextState2',
            library='Internal-ActiveWorkspaceBom',
            service_date='2019_06',
            service_name='OccurrenceManagement',
            params={'contextState': contextState, 'requestPref': requestPref},
            response_cls=ServiceData,
        )


class CompareService(TcService):

    @classmethod
    def compareContentAsync2(cls, input: CompareContentAsyncData2) -> None:
        """
        This operation performs asynchronous comparison of two contents (can also be refered to as source and target)
        and stores the output of comparision results in a dataset. The content can be Item BVR structures or a 4th
        Generation Design or BOM data contained within a Subset.
        """
        return cls.execute_soa_method(
            method_name='compareContentAsync2',
            library='Internal-ActiveWorkspaceBom',
            service_date='2019_06',
            service_name='Compare',
            params={'input': input},
            response_cls=None,
        )
