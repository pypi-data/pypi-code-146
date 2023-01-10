from __future__ import annotations

from tcsoa.gen.Vendormanagement._2008_06.VendorManagement import ChangeVendorInputInfo, GetVendorPartsWithSelRuleResponse, GetVendorPartsWithSelRuleInputInfo, ChangeVendorResponse
from typing import List
from tcsoa.base import TcService


class VendorManagementService(TcService):

    @classmethod
    def changeVendor(cls, input: List[ChangeVendorInputInfo]) -> ChangeVendorResponse:
        """
        This service operation can be called on either a VendorPart or a Vendor.
        
        For VendorPart: It creates a new copy of VendorPart with the new Vendor information. This newly created
        VendorPart is associated to the new revision of the CommercialPart of the old VendorPart.
        For Vendor: All VendorPart objects related with given Vendor are taken into consideration. Each of these
        VendorPart objects are then processed as mentioned above.
        
        This operation shows old and new part id with the information of the success or failure. 
        
        Typical Client Usage: 
        Typical usage involves two Vendor objects and a VendorPart created with either one of them.
        
        'VendorManagementService vmService = 
        VendorManagementService.getService(session);
        ChangeVendorInputInfo[]chanProps = new ChangeVendorInputInfo[1];
        ChangeVendorInputInfo changeProps = new ChangeVendorInputInfo();
        ChangeVendorResponse response = null;
        changeProps.newVendor = (TCComponentVendor)newVendor;
        changeProps.vendorParts=selectedParts;
        chanProps[0] = changeProps;
        
        response = vmService.changeVendor( chanProps );'
        """
        return cls.execute_soa_method(
            method_name='changeVendor',
            library='Vendormanagement',
            service_date='2008_06',
            service_name='VendorManagement',
            params={'input': input},
            response_cls=ChangeVendorResponse,
        )

    @classmethod
    def getVendorPartsWithSelRule(cls, input: List[GetVendorPartsWithSelRuleInputInfo]) -> GetVendorPartsWithSelRuleResponse:
        """
        This service operation returns VendorPart objects  associated with the given CommercialPartRevision  based on
        the selection rule set for the VendorPart objects in Structure Manager. If no value is given for the selection
        rule, it is read  from the preference VMS_vendor_part_selection_rule. Typical OOTB selection rules provided are
        showAllVendorParts and showPreferredVendorPartsOnly.  First selection rule is to show all related VendorPart
        objects and later is used to show the related VendorPart objects carrying preferred status.
        """
        return cls.execute_soa_method(
            method_name='getVendorPartsWithSelRule',
            library='Vendormanagement',
            service_date='2008_06',
            service_name='VendorManagement',
            params={'input': input},
            response_cls=GetVendorPartsWithSelRuleResponse,
        )
