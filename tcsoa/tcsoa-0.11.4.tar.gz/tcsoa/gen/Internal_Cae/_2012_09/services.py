from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, CAEItemRevision, ItemRevision
from tcsoa.gen.Internal.Cae._2011_06.StructureManagement import ExecuteRuleResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def updateModelAttsByDM(cls, productBOMLine: BOMLine, modelParentBOMLine: BOMLine, modelRevTag: ItemRevision, modelExistingBOMLine: BOMLine, domain: str, bomlineAttribsOnly: bool, doRevise: bool) -> ExecuteRuleResponse:
        """
        This internal operation will update the attributes of the given CAEModel Revision as per attributes of the
        given product BOMLine, after applying data mapping rules to it. The data mapping rules will be applied as per
        the given domain.
        """
        return cls.execute_soa_method(
            method_name='updateModelAttsByDM',
            library='Internal-Cae',
            service_date='2012_09',
            service_name='StructureManagement',
            params={'productBOMLine': productBOMLine, 'modelParentBOMLine': modelParentBOMLine, 'modelRevTag': modelRevTag, 'modelExistingBOMLine': modelExistingBOMLine, 'domain': domain, 'bomlineAttribsOnly': bomlineAttribsOnly, 'doRevise': doRevise},
            response_cls=ExecuteRuleResponse,
        )

    @classmethod
    def createNewModelByDM(cls, productBOMLine: BOMLine, modelParentBOMLine: BOMLine, modelExistingBOMLine: BOMLine, domain: str) -> ExecuteRuleResponse:
        """
        This internal operation will create a CAEModel Item Revision by applying Data Map rules to the given product
        bomline. The data mapping rules will be applied as per the given domain.
        """
        return cls.execute_soa_method(
            method_name='createNewModelByDM',
            library='Internal-Cae',
            service_date='2012_09',
            service_name='StructureManagement',
            params={'productBOMLine': productBOMLine, 'modelParentBOMLine': modelParentBOMLine, 'modelExistingBOMLine': modelExistingBOMLine, 'domain': domain},
            response_cls=ExecuteRuleResponse,
        )

    @classmethod
    def executeDatamap(cls, rootBOMLine: BOMLine, domain: str) -> ExecuteRuleResponse:
        """
        This internal operation creates an output BOM structure given the root BOMLine of an input BOM structure loaded
        in a BOMWindow. The output BOM structure is determined by the XSLT-based Data Map rules executed against the
        input BOM structure. Data Map syntax is in compliance with the schema defined in tcsim_xslWithNode.xsd, located
        in TC_DATA.
        Data Map rules define the mapping between an input item type and its resulting output item type. Data Map rules
        are defined for an entire site and are stored in the datamapping.xml file located in TC_DATA. The naming of the
        data mapping file is defined by the site preference CAE_dataMapping_file.
        The datamapping.xml file can be configured for various domains defined as LOV objects under StructureMap
        Domains in BMIDE. To configure the domains, in the Extensions view in BMIDE, open LOV->StructureMap Domains and
        add additional domain values. This operation assumes the value of the domain as CAE.
        To use this operation, a well-defined datamapping.xml is required in TC_DATA.
        """
        return cls.execute_soa_method(
            method_name='executeDatamap',
            library='Internal-Cae',
            service_date='2012_09',
            service_name='StructureManagement',
            params={'rootBOMLine': rootBOMLine, 'domain': domain},
            response_cls=ExecuteRuleResponse,
        )

    @classmethod
    def executeMarkUpToDate(cls, inputItemRevList: List[CAEItemRevision]) -> ServiceData:
        """
        This internal operation will check if there exists any status object associated with the input CAEItem
        Revisions. If it exists it will update the attributes of the status object. If no status object found to be
        associated with the CAEItem Revision, a new object will be created
        """
        return cls.execute_soa_method(
            method_name='executeMarkUpToDate',
            library='Internal-Cae',
            service_date='2012_09',
            service_name='StructureManagement',
            params={'inputItemRevList': inputItemRevList},
            response_cls=ServiceData,
        )
