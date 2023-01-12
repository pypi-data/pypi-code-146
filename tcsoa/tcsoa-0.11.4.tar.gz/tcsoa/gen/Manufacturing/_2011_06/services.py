from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Manufacturing._2011_06.DataManagement import OpenViewsResponse, OpenContextInput, OpenContextsResponse
from tcsoa.gen.Manufacturing._2011_06.StructureManagement import ReferencedContextsResponse, ReferencedContexts
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def getReferenceContexts(cls, contexts: List[BusinessObject]) -> ReferencedContextsResponse:
        """
        return referenced contexts of input context
        """
        return cls.execute_soa_method(
            method_name='getReferenceContexts',
            library='Manufacturing',
            service_date='2011_06',
            service_name='StructureManagement',
            params={'contexts': contexts},
            response_cls=ReferencedContextsResponse,
        )

    @classmethod
    def setReferenceContexts(cls, input: List[ReferencedContexts]) -> ServiceData:
        """
        set Reference context according to user choice
        """
        return cls.execute_soa_method(
            method_name='setReferenceContexts',
            library='Manufacturing',
            service_date='2011_06',
            service_name='StructureManagement',
            params={'input': input},
            response_cls=ServiceData,
        )


class DataManagementService(TcService):

    @classmethod
    def closeContexts(cls, contexts: List[BusinessObject]) -> ServiceData:
        """
        This method is used to close contexts (base view windows). For each context, this method closes the base view
        window and all the open views (OG windows) associated to it
        """
        return cls.execute_soa_method(
            method_name='closeContexts',
            library='Manufacturing',
            service_date='2011_06',
            service_name='DataManagement',
            params={'contexts': contexts},
            response_cls=ServiceData,
        )

    @classmethod
    def closeViews(cls, structureContext: BusinessObject, views: List[BusinessObject]) -> ServiceData:
        """
        This method is used to close opened views (OG windows)
        """
        return cls.execute_soa_method(
            method_name='closeViews',
            library='Manufacturing',
            service_date='2011_06',
            service_name='DataManagement',
            params={'structureContext': structureContext, 'views': views},
            response_cls=ServiceData,
        )

    @classmethod
    def openContexts(cls, input: List[OpenContextInput]) -> OpenContextsResponse:
        """
        This method is used to open existing objects in new base view windows
        """
        return cls.execute_soa_method(
            method_name='openContexts',
            library='Manufacturing',
            service_date='2011_06',
            service_name='DataManagement',
            params={'input': input},
            response_cls=OpenContextsResponse,
        )

    @classmethod
    def openViews(cls, context: BusinessObject, structureContext: BusinessObject, views: List[BusinessObject]) -> OpenViewsResponse:
        """
        This method is used to open views (OG windows) for an already opened context (base view window).
        """
        return cls.execute_soa_method(
            method_name='openViews',
            library='Manufacturing',
            service_date='2011_06',
            service_name='DataManagement',
            params={'context': context, 'structureContext': structureContext, 'views': views},
            response_cls=OpenViewsResponse,
        )
