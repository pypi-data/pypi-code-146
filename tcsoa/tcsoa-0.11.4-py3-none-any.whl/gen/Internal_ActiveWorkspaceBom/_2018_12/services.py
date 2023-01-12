from __future__ import annotations

from tcsoa.gen.Internal.ActiveWorkspaceBom._2018_12.OccurrenceManagement import AddObjectData, OccurrencesData, AddObjectResp, OccurrencesResp
from tcsoa.gen.Internal.ActiveWorkspaceBom._2018_12.Markup import ApplyMarkupData
from tcsoa.gen.BusinessObjects import BusinessObject, Awb0Element
from tcsoa.gen.Internal.ActiveWorkspaceBom._2018_12.Compare import CompareOptionsResponse, CompareContentData2, CompareResp2
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class OccurrenceManagementService(TcService):

    @classmethod
    def addObject(cls, input: AddObjectData) -> AddObjectResp:
        """
        This operation adds an object to a product as specified in Awb0ProductContextInfo or parent Awb0Element and
        creates Awb0Element representing newly created object. The new object is added as a sibling to the selected
        Awb0Element if that is provided in input. The Awb0ProductContextInfo and parent Awb0Element can be retrieved
        using getOccurrences7.
        
        Use cases:
        User loads the product structure in Content. The Content  is used for smart navigation of occurrences in a
        structure. User selects an occurrence in the Content and clicks on Add button. This actions will add a new
        occurrence as a child or sibling of the selected occurrence.
        """
        return cls.execute_soa_method(
            method_name='addObject',
            library='Internal-ActiveWorkspaceBom',
            service_date='2018_12',
            service_name='OccurrenceManagement',
            params={'input': input},
            response_cls=AddObjectResp,
        )

    @classmethod
    def getOccurrences(cls, inputData: OccurrencesData) -> OccurrencesResp:
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
            method_name='getOccurrences',
            library='Internal-ActiveWorkspaceBom',
            service_date='2018_12',
            service_name='OccurrenceManagement',
            params={'inputData': inputData},
            response_cls=OccurrencesResp,
        )


class MarkupService(TcService):

    @classmethod
    def cancelMarkup(cls, element: Awb0Element, markups: List[BusinessObject]) -> ServiceData:
        """
        This operation cancels the proposed markup changes for input element. This operation returns updated or removed
        Awb0Element objects. If the Awb0Element objects were created  as a markup proposal then the Awb0Element objects
        are removed.  If Awb0Element objects had property change markup proposals then the Awb0Element objects are
        returned as updated objects in ServiceData.
        """
        return cls.execute_soa_method(
            method_name='cancelMarkup',
            library='Internal-ActiveWorkspaceBom',
            service_date='2018_12',
            service_name='Markup',
            params={'element': element, 'markups': markups},
            response_cls=ServiceData,
        )

    @classmethod
    def applyMarkup(cls, input: List[ApplyMarkupData]) -> ServiceData:
        """
        This operation applies proposed changes that were stored in the active markup for the specified  Awb0Element
        object, if the evaluate flag is false. If the evaluate flag is true, the write access to perform the save is
        checked and no modification is actually attempted. If the recursive flag is set, then all active Markups in the
        elements under the specified element are evaluated and/or saved.
        """
        return cls.execute_soa_method(
            method_name='applyMarkup',
            library='Internal-ActiveWorkspaceBom',
            service_date='2018_12',
            service_name='Markup',
            params={'input': input},
            response_cls=ServiceData,
        )


class CompareService(TcService):

    @classmethod
    def compareContent2(cls, inputData: CompareContentData2) -> CompareResp2:
        """
        This operation compares two contents (can also be referred to as source and target) and returns a output of
        comparison results. The content can be Item BVR structures or a 4th Generation Design or BOM data contained
        within a Subset.
        
        Exceptions:
        >Teamcenter::Soa::Server::ServiceException:
        
        This operation may raise a ServiceException containing following errors:
        
        126001  :  An internal error has occurred in the Occurrence Management module. 
        126002  :  No Adapter could be found to handle the Request.
        """
        return cls.execute_soa_method(
            method_name='compareContent2',
            library='Internal-ActiveWorkspaceBom',
            service_date='2018_12',
            service_name='Compare',
            params={'inputData': inputData},
            response_cls=CompareResp2,
        )

    @classmethod
    def getCompareOptions(cls, sourceObject: BusinessObject, targetObject: BusinessObject) -> CompareOptionsResponse:
        """
        This operation retreives the list of options to compare two structures. Structures can be Item BVR structures
        or a 4th Generation Design or BOM data contained within a Subset.
        
        Exceptions:
        >ServiceException:
        This operation may raise a ServiceException containing following errors:
        
        126001 : An internal error has occurred in the Occurrence Management module. 
        126002 : No Adapter could be found to handle the Request.
        126254 : The input "Object" is invalid for compare.
        126255 : The input "Source Object" and "Target Object" combination is invalid for compare.
        """
        return cls.execute_soa_method(
            method_name='getCompareOptions',
            library='Internal-ActiveWorkspaceBom',
            service_date='2018_12',
            service_name='Compare',
            params={'sourceObject': sourceObject, 'targetObject': targetObject},
            response_cls=CompareOptionsResponse,
        )
