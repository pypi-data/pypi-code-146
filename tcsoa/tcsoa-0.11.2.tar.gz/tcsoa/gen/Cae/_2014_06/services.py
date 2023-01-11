from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine
from tcsoa.gen.Cae._2014_06.StructureManagement import DerivativeRuleResponse
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def executeDeriveCAEStructure(cls, rootBOMLine: BOMLine, selectedRule: str, optionalRootName: str, optionalIndex: str) -> DerivativeRuleResponse:
        """
        This operation creates a cloned/variant structure from the root BOMLine of a BOM structure loaded in a model
        BOMWindow and a derivative rule name to be applied. The output BOM structure is determined by the XSLT-based
        clone rules executed against the input BOM structure. These clone rules are a part of the derivative rule
        configuration. Several clone rules are defined under a derivative rule. There can be several derivative rules
        defined in the database by Simulation Administrator. 
        
        Given an input BOM structure, the derivative rules is applied to the BOM structure and generate a corresponding
        output structure. The output is a clone/variant based on the clone rules defined in the derivative rule
        configuration.
        
        The output structure may optionally have a user defined name for the root, suffixed with a user defined
        numerical index. 
        
        This operation uses the existing Data Mapping functionality to apply the clone rules against input structure
        and generate the output structure. Data mapping defines the mapping between an input item type and its
        resulting output item type. The Derive CAE Structure operation specific data mapping rules will co-exist with
        existing configurations, stored in the datamapping.xml file. This file is maintained in the database. 
        
        To use Derive CAE Structure operation, well-defined CAEDerivativeRuleConfig.xml, datamapping.xml and
        NodeConfigXML.xml files are required in the database.
         CAEDerivativeRuleConfig.xml file contains the configurations and conditional clone rules pertaining to the
        Derivative Rule . Datamapping.xml contains mapping rules configured for mapping between input and output CAE
        Structures. NodeXMLconfig.xml is has configured item attributes, which are mapped between input and output CAE
        Structure. 
        Simulation Administrators or DBAs should assign the location for CAEDerivativesRuleConfig.xml using Derivative
        Rules user preferences. Derivative Rules view is used to create a Derivative Rule.
        Similarly, Datamapping.xml and NodeXMLConfig.xml  are also configured by an Administrator and stored at the
        location in database which is pointed by user preference CAE_datamap_files_location.
        
        
        Use cases:
        1: Create an output structure given a top BOMLine of the input structure, a Derivative Rule name.
        
        Given an input BOM structure, this operation will apply the clone rules contained within the specified
        Derivative Rule configuration to the BOM structure and generate a corresponding output structure. 
        The output structure would be an exact clone/variant based on the rules defined in the configuration.
        """
        return cls.execute_soa_method(
            method_name='executeDeriveCAEStructure',
            library='Cae',
            service_date='2014_06',
            service_name='StructureManagement',
            params={'rootBOMLine': rootBOMLine, 'selectedRule': selectedRule, 'optionalRootName': optionalRootName, 'optionalIndex': optionalIndex},
            response_cls=DerivativeRuleResponse,
        )
