from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, BidPackageRevision, BidPackage, Vendor, Part, VendorRevision, ItemRevision
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class BidPackageProps(TcBaseObj):
    """
    The information about each BidPackage to be processed is provided by way of the 'BidPackageProps' data structure.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify the Partial Errors associated
    with this 'BidPackageProps' input.
    :var itemId: Id to create BidPackage, generated if the string is empty.
    :var name: Name for the BidPackage. Default name generated if left empty.
    :var type: Object Type to be created. It is BidPackage.
    :var revId: Revision Id to create BidPackageRevision. Generated if left empty.
    :var description: Description of the object to be created.
    """
    clientId: str = ''
    itemId: str = ''
    name: str = ''
    type: str = ''
    revId: str = ''
    description: str = ''


@dataclass
class CreateVendorsOutput(TcBaseObj):
    """
    The information about each Vendor object output after creation is provided by way of the 'CreateVendorsOutput' data
    structure.
    
    :var clientId: A unique string supplied by the caller.
    :var vendor: Vendor Object created or updated.
    :var vendorRev: VendorRevision Object created or Updated.
    """
    clientId: str = ''
    vendor: Vendor = None
    vendorRev: VendorRevision = None


@dataclass
class CreateVendorsResponse(TcBaseObj):
    """
    The 'CreateVendorsResponse' structure represents the output vector 'CreateVendorsOutput' and the 'ServiceData'.
    
    :var output: A list of 'CreateVendorsOutput' structures. Each of them represents a Vendor created or updated.
    :var serviceData: Standard 'ServiceData' structure. It contains partial errors and failures along with the
    clientIds.
    """
    output: List[CreateVendorsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class LineItemProps(TcBaseObj):
    """
    The information about each BidPackageLineItem to be processed is provided by way of the 'LineItemProps' data
    structure.
    
    :var name: Name of the BidPackageLineItem to be created.
    :var description: Description of the BidPackageLineItem Object.
    :var quote: Model Object for Quote to be added to BidPackageLineItem.
    :var liccname: Name of the LineItemConfigContext to be created.
    :var liccdesc: Description for the 'LineItemConfigContext' object to be created.
    :var partid: Id of the part to be associated with BidPackageLineItem.
    :var viewtype: 'PSViewType' to be associated with LineItemConfigContext.
    :var quantity: Quantity to be created for BidPackageLineItem.
    :var revRule: Revision rule to be associated with LineItemConfigContext.
    :var varRule: Variant rule to be associated with LineItemConfigContext.
    :var closureRule: Closure rule to be associated with LineItemConfigContext.
    """
    name: str = ''
    description: str = ''
    quote: BusinessObject = None
    liccname: str = ''
    liccdesc: str = ''
    partid: str = ''
    viewtype: str = ''
    quantity: int = 0
    revRule: str = ''
    varRule: str = ''
    closureRule: str = ''


@dataclass
class VendorPartProperties(TcBaseObj):
    """
    The information about each VendorPart to be processed is provided by way of the 'VendorPartProperties' data
    structure.
    
    :var partId: Id for part to be created, mandatory for ManufacturerPart objects but generated for CommercialPart
    objects if the string is empty. Output PartId in case of ManufacturerPart will contain the provided partId and
    provided VendorId.
    :var name: Name of the Part object to be created.
    :var uom: Unit of Measure for Model Object.
    :var makebuy: Make Buy Value for Part. The value could be either Make or Buy.
    :var clientId: A unique string supplied by the caller. This ID is used to identify the Partial Errors associated
    with this 'VendorPartProperties' input.
    :var type: Object type to be created. Only ManufacturerPart and CommercialPart are valid.
    :var revId: Revision Id specified for create. Generated if the string is empty.
    :var description: Description of the VendorPart.
    :var vendorid: Vendor Id to be associated with Part. Vendor Id is optional for CommercialPart but mandatory for
    ManufacturerPart.
    :var commercialpartid: Id of CommercialPart to be associated with ManufacturerPart.
    :var commercialpartrevid: CommercialPartRevision Id to be associated with ManufacturerPart. If blank,
    ManufacturerPart is attached with the CommercialPart instead.
    :var isDesignReq: Flag to decide if the design is required.
    """
    partId: str = ''
    name: str = ''
    uom: BusinessObject = None
    makebuy: int = 0
    clientId: str = ''
    type: str = ''
    revId: str = ''
    description: str = ''
    vendorid: str = ''
    commercialpartid: str = ''
    commercialpartrevid: str = ''
    isDesignReq: bool = False


@dataclass
class VendorProperties(TcBaseObj):
    """
    The information about each Vendor to be processed is provided by way of the 'VendorProperties' data structure.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify the Partial Errors associated
    with this 'VendorProperties' input.
    :var itemId: Item Id of the Vendor. Generated if the string is empty.
    :var name: Name of the Vendor. Default name is generated if kept empty.
    :var type: Object type to be created.
    :var revId: VendorRevision Id specified for create. Generated if the string is empty.
    :var description: Description of the Vendor.
    :var roleType: Type of VendorRole. It can be Manufacturer,Supplier, Distributor or blank.
    :var certifiStatus: Vendor Certification status like Gold,Silver etc.
    :var vendorStatus: Vendor status like Preferred,Approved etc.
    """
    clientId: str = ''
    itemId: str = ''
    name: str = ''
    type: str = ''
    revId: str = ''
    description: str = ''
    roleType: str = ''
    certifiStatus: str = ''
    vendorStatus: str = ''


@dataclass
class CreateBidPacksOutput(TcBaseObj):
    """
    The information about each BidPackage object output after creation is provided by  way of the 'CreateVendorsOutput'
    data structure.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify the Partial Errors associated
    with input.
    :var bidPackage: Model Object pointing to the BidPackage created.
    :var bidPackageRev: Model Object poinitng to the BidPackageRevision created.
    """
    clientId: str = ''
    bidPackage: BidPackage = None
    bidPackageRev: BidPackageRevision = None


@dataclass
class CreateBidPacksResponse(TcBaseObj):
    """
    The 'CreateBidPacksResponse' structure represents the output vector 'CreateBidPacksOutput' and standard Teamcenter
    'ServiceData' structure instance.
    
    :var output: A list of 'CreateBidPacksOutput' structures. Each entry represents a BidPackage created or updated.
    :var serviceData: Standard 'ServiceData' structure. It contains typical potential errors as mentioned in throws and
    failures along with the clientIds.
    """
    output: List[CreateBidPacksOutput] = ()
    serviceData: ServiceData = None


@dataclass
class CreateVendorPartsOutput(TcBaseObj):
    """
    The information about each VendorPart object output after creation is provided by way of the
    'CreateVendorPartsOutput' data structure.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify the Partial Errors associated
    with input.
    :var vendorPart: Model Object pointing to the VendorPart created.
    :var vendorPartRev: Model Object poinitng to the VendorPart revision created.
    """
    clientId: str = ''
    vendorPart: Part = None
    vendorPartRev: ItemRevision = None


@dataclass
class CreateVendorPartsResponse(TcBaseObj):
    """
    The 'CreateVendorPartsResponse' structure represents the list of 'CreateVendorPartsOutput' and Standard Teamcenter
    'ServiceData'.
    
    :var output: Output is list of 'CreateVendorPartsOutput' data structures, each of them representing a new
    VendorPart created.
    :var serviceData: Standard 'ServiceData' structure. It contains partial errors and failures along with the
    clientIds.
    """
    output: List[CreateVendorPartsOutput] = ()
    serviceData: ServiceData = None
