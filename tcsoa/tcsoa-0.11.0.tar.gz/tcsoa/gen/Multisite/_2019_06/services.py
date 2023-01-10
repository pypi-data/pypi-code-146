from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Multisite._2019_06.ImportExportTCXML import RemoteCheckinResponse, StringVectorMap, RemoteCheckoutResponse
from tcsoa.gen.Multisite._2019_06.Search import StringVectorMap1, SearchResponse
from tcsoa.base import TcService


class SearchService(TcService):

    @classmethod
    def publish(cls, objects: List[BusinessObject], targetSites: List[str], options: StringVectorMap1) -> SearchResponse:
        """
        The publish operation applies the Multi-Site publish to the Object Directory Server (ODS) operation to the
        business objects in the objects parameter.
        
        Use cases:
        In the Multi-Site federation, a user can share the business objects among the participating sites, the client
        shares business object(s) using the remote import or remote export functionality. Sites can publish objects to
        the ODS which allows a remote site to search for candidates to remote import.
        """
        return cls.execute_soa_method(
            method_name='publish',
            library='Multisite',
            service_date='2019_06',
            service_name='Search',
            params={'objects': objects, 'targetSites': targetSites, 'options': options},
            response_cls=SearchResponse,
        )

    @classmethod
    def unpublish(cls, objects: List[BusinessObject], targetSites: List[str], options: StringVectorMap1) -> SearchResponse:
        """
        The unpublish operation applies the Multi-Site unpublish to the Object Directory Server (ODS) operation to the
        business objects in the objects input list.
        
        Use cases:
        In the Multi-Site federation, a user can share the business objects among the participating sites, the client
        shares business object(s) using the remote import or remote export functionality. Sites can publish objects to
        the ODS which allows a remote site to search for candidates to remote import. These same objects can be later
        unpublished.
        """
        return cls.execute_soa_method(
            method_name='unpublish',
            library='Multisite',
            service_date='2019_06',
            service_name='Search',
            params={'objects': objects, 'targetSites': targetSites, 'options': options},
            response_cls=SearchResponse,
        )


class ImportExportTCXMLService(TcService):

    @classmethod
    def remoteCheckin(cls, objects: List[BusinessObject], optionSetName: str, sessionOptions: StringVectorMap, overrideOptions: StringVectorMap) -> RemoteCheckinResponse:
        """
        The remoteCheckin operation applies the Multi-Site checkin operation to the business objects in the objects
        parameter. The Multi-Site TCXML payload is used.
        
        Use cases:
        In the Multi-Site federation, a user can share the business objects among the participating sites, the client
        shares business object(s) using the remote import or remote export functionality. This allows the creation of
        replica objects which are read-only copies of the master object. Multi-site supports a Remote Check-in
        Check-out feature which allows edits to replica objects. This operation supports the following use case. 
        
        * The remote checkin of checked-out replica business objects.  Changes made to the replica object will be sent
        back to the master site and the checked-out status will be removed at both the master and replica objects.
        """
        return cls.execute_soa_method(
            method_name='remoteCheckin',
            library='Multisite',
            service_date='2019_06',
            service_name='ImportExportTCXML',
            params={'objects': objects, 'optionSetName': optionSetName, 'sessionOptions': sessionOptions, 'overrideOptions': overrideOptions},
            response_cls=RemoteCheckinResponse,
        )

    @classmethod
    def remoteCheckout(cls, objects: List[BusinessObject], optionSetName: str, sessionOptions: StringVectorMap, overrideOptions: StringVectorMap) -> RemoteCheckoutResponse:
        """
        The RemoteCheckout operation applies the Multi-Site check out operation to the business objects in the objects
        parameter.
        
        Use cases:
        In the Multi-Site federation, a user can share the business objects among the participating sites, the client
        shares business object(s) using the remote import or remote export functionality. This allows the creation of
        replica objects which are read-only copies of the master object. Multi-site supports a Remote Check-in
        Check-out feature which allows edits to replica objects. This operation supports the following use case.
        
        - The remote check out of replica business objects.  This allows edits to the replica objects. These changes
        are later saved to the owning site with the remote check in operation.
        
        """
        return cls.execute_soa_method(
            method_name='remoteCheckout',
            library='Multisite',
            service_date='2019_06',
            service_name='ImportExportTCXML',
            params={'objects': objects, 'optionSetName': optionSetName, 'sessionOptions': sessionOptions, 'overrideOptions': overrideOptions},
            response_cls=RemoteCheckoutResponse,
        )
