from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.ChangeManagement._2015_03.ChangeManagement import UpdateChangeNoticeRelationsResp, UpdateChangeNoticeRelationsIn, ConnectChangeNoticeToContextResp, CreateOrUpdatePreviousEffResp, PreviousEffectivity, ConnectChangeNoticeToContextInElem
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ChangeManagementService(TcService):

    @classmethod
    def disconnectChangeNoticeFromContext(cls, input: List[BusinessObject]) -> ServiceData:
        """
        This operation disconnects a previously associated ChangeNoticeRevision from the context (currently, the
        context must be a BOMWindow). The ChangeNoticeRevision would have been associated to a BOMWindow using the
        runtime property "cm0ChangeItemRev" or the connectChangeNoticeToContext operation. If no ChangeNoticeRevision
        is currently associated with the BOMWindow, the operation does not do any further processing for that
        particular element in the input.
        """
        return cls.execute_soa_method(
            method_name='disconnectChangeNoticeFromContext',
            library='Internal-ChangeManagement',
            service_date='2015_03',
            service_name='ChangeManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def removePrevEffectivityFromChgNotice(cls, input: List[BusinessObject]) -> ServiceData:
        """
        This operation disconnects a previously associated ConfigurationContext from ChangeNoticeRevision. If previous
        effectivity does not exist on the ChangeNoticeRevision, the operation proceeds to the next input element.
        """
        return cls.execute_soa_method(
            method_name='removePrevEffectivityFromChgNotice',
            library='Internal-ChangeManagement',
            service_date='2015_03',
            service_name='ChangeManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def updateChangeNoticeRelations(cls, inputs: List[UpdateChangeNoticeRelationsIn]) -> UpdateChangeNoticeRelationsResp:
        """
        This operation manages the secondary ItemRevision objects related to the ChangeNoticeRevision associated with a
        BOMWindow, by adding/removing these objects to/from the relations. The managed secondary ItemRevision objects
        will have appropriate sharing of the release statuses of the ChangeNoticeRevision, based on the sharing mode
        controlled by BOMWindow property cm0ChangeNoticeRevShareMode. If this property is not set, the default "Share"
        mode will be used.
        """
        return cls.execute_soa_method(
            method_name='updateChangeNoticeRelations',
            library='Internal-ChangeManagement',
            service_date='2015_03',
            service_name='ChangeManagement',
            params={'inputs': inputs},
            response_cls=UpdateChangeNoticeRelationsResp,
        )

    @classmethod
    def connectChangeNoticeToContext(cls, input: List[ConnectChangeNoticeToContextInElem]) -> ConnectChangeNoticeToContextResp:
        """
        This operation associates the given ChangeNoticeRevision to a context (currently, BOMWindow) for the purpose of
        tracking newly created revisions or revisions from revise operation in a session.
        """
        return cls.execute_soa_method(
            method_name='connectChangeNoticeToContext',
            library='Internal-ChangeManagement',
            service_date='2015_03',
            service_name='ChangeManagement',
            params={'input': input},
            response_cls=ConnectChangeNoticeToContextResp,
        )

    @classmethod
    def createOrUpdatePreviousEffectivity(cls, input: List[PreviousEffectivity]) -> CreateOrUpdatePreviousEffResp:
        """
        This operation creates a ConfigurationContext object with the provided previous effectivty parameters of
        endItem and one of unit or date. This ConfigurationContext is attached to the passed in ChangeNoticeRevision
        upon creation. If the ConfigurationContext is already present, the revision rule content is updated with the
        passed in previous effectivity parameters.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdatePreviousEffectivity',
            library='Internal-ChangeManagement',
            service_date='2015_03',
            service_name='ChangeManagement',
            params={'input': input},
            response_cls=CreateOrUpdatePreviousEffResp,
        )
