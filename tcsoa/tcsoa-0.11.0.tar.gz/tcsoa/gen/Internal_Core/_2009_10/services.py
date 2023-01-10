from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Internal.Core._2009_10.Thumbnail import ThumbnailFileTicketsResponse, UpdateThumbnailInputs, SearchOrders
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ThumbnailService(TcService):

    @classmethod
    def getThumbnailFileTickets(cls, businessObjects: List[BusinessObject], searchOrders: SearchOrders) -> ThumbnailFileTicketsResponse:
        """
        Given a list of business objects  and relation /dataset type search orders, gets the valid thumbnail file
        tickets for the list of business objects. These file tickets can be used later to download the thumbnail images
        using File Client Cache (FCC).
        
        Use cases:
        Display thumbnails in advanced search results
        """
        return cls.execute_soa_method(
            method_name='getThumbnailFileTickets',
            library='Internal-Core',
            service_date='2009_10',
            service_name='Thumbnail',
            params={'businessObjects': businessObjects, 'searchOrders': searchOrders},
            response_cls=ThumbnailFileTicketsResponse,
        )

    @classmethod
    def updateThumbnail(cls, businessObject: List[BusinessObject], updateThumbnailInputs: List[UpdateThumbnailInputs]) -> ServiceData:
        """
        This operation is to update thumbnail file for given business objects based on given user update thumbnail
        inputs. The user can specify either which source Dataset should be used to generate a thumbnail or let the
        system decide it based on thumbnail generation preferences.
        
        Use cases:
        -     Generate thumbnails at Item  create
        -     Update thumbnails for ItemRevision
        -     Generate thumbnails when Dataset is associated
        
        """
        return cls.execute_soa_method(
            method_name='updateThumbnail',
            library='Internal-Core',
            service_date='2009_10',
            service_name='Thumbnail',
            params={'businessObject': businessObject, 'updateThumbnailInputs': updateThumbnailInputs},
            response_cls=ServiceData,
        )
