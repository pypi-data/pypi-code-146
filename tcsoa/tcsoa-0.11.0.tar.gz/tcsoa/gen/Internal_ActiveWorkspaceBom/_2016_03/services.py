from __future__ import annotations

from tcsoa.gen.Internal.ActiveWorkspaceBom._2016_03.OccurrenceManagement import ReplaceInput, ReplaceElementResponse, AddToBookmarkResp2, AddToBookmarkInputData2, EffectivityInput, SubsetInput2
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.gen.Internal.ActiveWorkspaceBom._2015_07.OccurrenceManagement import SubsetResponse
from tcsoa.base import TcService


class OccurrenceManagementService(TcService):

    @classmethod
    def addOrRemoveOccurrenceEffectivities(cls, input: EffectivityInput) -> ServiceData:
        """
        This operation adds or removes Effectivity objects to/from the input list of Awb0Element(s). The impacted
        Awb0Element(s) are reconfigured with new effectivities.
        """
        return cls.execute_soa_method(
            method_name='addOrRemoveOccurrenceEffectivities',
            library='Internal-ActiveWorkspaceBom',
            service_date='2016_03',
            service_name='OccurrenceManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def addToBookmark2(cls, input: AddToBookmarkInputData2) -> AddToBookmarkResp2:
        """
        This operation adds a product with current configuration parameters to the Awb0AutoBookmark associated with the
        input Awb0SavedBookmark. This operation does not update the Awb0SavedBookmark itself.
        """
        return cls.execute_soa_method(
            method_name='addToBookmark2',
            library='Internal-ActiveWorkspaceBom',
            service_date='2016_03',
            service_name='OccurrenceManagement',
            params={'input': input},
            response_cls=AddToBookmarkResp2,
        )

    @classmethod
    def getSubsetInfo2(cls, subsetInputs: List[SubsetInput2]) -> SubsetResponse:
        """
        This operation retrieves filters and recipes which are used to find matching Awb0Element objects for input
        Awb0ProductContextInfo.
        """
        return cls.execute_soa_method(
            method_name='getSubsetInfo2',
            library='Internal-ActiveWorkspaceBom',
            service_date='2016_03',
            service_name='OccurrenceManagement',
            params={'subsetInputs': subsetInputs},
            response_cls=SubsetResponse,
        )

    @classmethod
    def replaceElement(cls, input: ReplaceInput) -> ReplaceElementResponse:
        """
        This operation replaces an underlying object of the Awb0Element with input BusinessObject. The
        Awb0ProductContextInfo provides configuration information for the 'replacement'.
        """
        return cls.execute_soa_method(
            method_name='replaceElement',
            library='Internal-ActiveWorkspaceBom',
            service_date='2016_03',
            service_name='OccurrenceManagement',
            params={'input': input},
            response_cls=ReplaceElementResponse,
        )
