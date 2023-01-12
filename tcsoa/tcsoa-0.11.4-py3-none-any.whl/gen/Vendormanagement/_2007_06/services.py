from __future__ import annotations

from tcsoa.gen.Vendormanagement._2007_06.VendorManagement import CreateVendorsResponse, CreateVendorPartsResponse, LineItemProps, VendorProperties, BidPackageProps, VendorPartProperties, CreateBidPacksResponse
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class VendorManagementService(TcService):

    @classmethod
    def deleteVendorRoles(cls, input: List[VendorProperties]) -> ServiceData:
        """
        This service operation deletes specified VendorRole objects attached with VendorRevision objects mentioned
        through 'VendorProperties'  data structure. VendorRevision is specified through vendor ID and Revision name in
        'VendorProperties'. The combination to be specified thus is 'vendorId + revId + roleType'. So, this combination
        denotes that there will be one instance of 'VendorProperties' per VendorRole to be deleted. In case of
        VendorRevision is not found based on the Id and Revision key, this operation will return an error.
        """
        return cls.execute_soa_method(
            method_name='deleteVendorRoles',
            library='Vendormanagement',
            service_date='2007_06',
            service_name='VendorManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def deleteVendors(cls, input: List[VendorProperties]) -> ServiceData:
        """
        This service operation deletes Vendor objects and associated VendorRevision objects and VendorRole objects.
        When provided with the input in the form of 'VendorProperties' structure, the operation finds the specified
        Vendor objects and deletes them. VendorRole objects  will also be deleted along with the associated
        VendorRevision objects and Vendor objects.
        """
        return cls.execute_soa_method(
            method_name='deleteVendors',
            library='Vendormanagement',
            service_date='2007_06',
            service_name='VendorManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def createOrUpdateBidPackages(cls, properties: List[BidPackageProps], container: BusinessObject, relationType: str) -> CreateBidPacksResponse:
        """
        This service operation creates or updates a group of BidPackage, BidPackageRevision objects. This operation
        allows the user to find or create a set of BidPackage objects based on the input data. The service first tries
        to find the existence of the specified BidPackage or BidPackageRevision. If the specified BidPackage objects
        exist and any of the input attribute values differ from those already set, the BidPackage objects will be
        updated.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateBidPackages',
            library='Vendormanagement',
            service_date='2007_06',
            service_name='VendorManagement',
            params={'properties': properties, 'container': container, 'relationType': relationType},
            response_cls=CreateBidPacksResponse,
        )

    @classmethod
    def createOrUpdateLineItems(cls, properties: List[LineItemProps], bidPackage: BusinessObject) -> ServiceData:
        """
        This service operation creates or updates a group of BidPackageLineItem objects in the context of the mentioned
        BidPackage. This operation allows the user to find or create a set of BidPackageLineItem objects based on the
        input data. It first tries to find the existence of the specified BidPackageLineItem for the specified
        BidPackage. If the specified BidPackageLineItem is found, then its corresponding data will be updated.
        Otherwise, it will create the specified BidPackageLineItem and associate it to the specified
        BidPackageRevision. If the specified BidPackageLineItem objects exist and any of the input attribute values
        differ from those already set, the BidPackageLineItem objects will be updated.
        
        The operation is now deprecated. It is now replaced by
        'Teamcenter::Soa::Vendormanagement::VendorManagement::createOrUpdateLineItemsWithType.'
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateLineItems',
            library='Vendormanagement',
            service_date='2007_06',
            service_name='VendorManagement',
            params={'properties': properties, 'bidPackage': bidPackage},
            response_cls=ServiceData,
        )

    @classmethod
    def createOrUpdateVendorParts(cls, properties: List[VendorPartProperties], container: BusinessObject, relationType: str) -> CreateVendorPartsResponse:
        """
        This service operation creates or updates a group of VendorPart objects or CommericialPart objects. The choice
        could be either CommercialPart or VendorPart only. This operation allows the user to update or create a set of
        CommercialPart objects or VendorPart objects based on the input data. It first tries to find the existence of
        the specified VendorPart or VendorPartRevision. If the specified parts are found, those parts will be updated
        with the specified values. Otherwise new parts will be created. 
        The choice for type of part is given through data member type of 'VendorPartProperties' structure. Only
        'ManufacturerPart' and 'CommercialPart' are valid types. 
        Behavior for CommercialPart:  The service will create the CommercialPart and CommercialPartRevision and it will
        associate the created CommercialPart to the specified parent (container). It also associates the part to the
        specified Vendor object if given. 
        Behavior for ManufacturerPart:  The service will create the ManufacturerPart and ManufacturerPartRevision and
        will associate the part to the specified Vendor object. It also associates the created ManufacturerPart to the
        CommercialPart if specified.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateVendorParts',
            library='Vendormanagement',
            service_date='2007_06',
            service_name='VendorManagement',
            params={'properties': properties, 'container': container, 'relationType': relationType},
            response_cls=CreateVendorPartsResponse,
        )

    @classmethod
    def createOrUpdateVendors(cls, properties: List[VendorProperties], container: BusinessObject, relationType: str) -> CreateVendorsResponse:
        """
        This service operation creates or updates a group of Vendor, VendorRevision Objects and VendorRole objects. It
        allows the user to update or create a set of Vendor objects based on the input data. The service first tries to
        find the existence of the specified Vendor or VendorRevision or VendorRole. If the service is able to find any
        of those objects, then those objects will be updated. If the service is not able to find those objects, then
        those objects will be created. If the Vendor exists, but VendorRevision does not, then VendorRevision and
        VendorRole (and VendorRole form) will be created. If the specified Vendor object and its associated objects
        exist and any of the input attribute values differ from those already set, the Vendor and its associated
        objects will be updated.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateVendors',
            library='Vendormanagement',
            service_date='2007_06',
            service_name='VendorManagement',
            params={'properties': properties, 'container': container, 'relationType': relationType},
            response_cls=CreateVendorsResponse,
        )

    @classmethod
    def deleteLineItems(cls, input: List[LineItemProps], bidPackage: BidPackageProps) -> ServiceData:
        """
        This service operation deletes the BidPackageLineItem objects associated with a specific BidPackageRevision.
        The BidPackageLineItem objects to be deleted are searched with their names provided through the input data
        structures 'LineItemProps'. Hence there will be one entry in the input vector 'input' per BidPackageLineItem to
        be deleted. There will be one call each for every BidPackageRevision for which BidPackageLineItem objects are
        to be deleted.
        """
        return cls.execute_soa_method(
            method_name='deleteLineItems',
            library='Vendormanagement',
            service_date='2007_06',
            service_name='VendorManagement',
            params={'input': input, 'bidPackage': bidPackage},
            response_cls=ServiceData,
        )
