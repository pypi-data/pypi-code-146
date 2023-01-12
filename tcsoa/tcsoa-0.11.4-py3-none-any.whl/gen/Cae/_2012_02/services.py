from __future__ import annotations

from tcsoa.gen.Cae._2012_02.StructureManagement import ExecuteRuleResponse2
from tcsoa.gen.BusinessObjects import VariantRule, Snapshot, ItemRevision, RevisionRule, StructureMapRevision
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def executeDatamap(cls, rootIR: ItemRevision, snapshotFolder: Snapshot, revRule: RevisionRule, variantRule: VariantRule, domain: str) -> ExecuteRuleResponse2:
        """
        This operation creates an output BOM structure given the root ItemRevision of the root BOMLine of an input BOM
        structure along with its RevisionRule and the VariantRule. A Snapshot folder of the input BOM structure along
        with the VariantRule can also be provided as an input. The output BOM structure is determined by the XSLT-based
        Data Map rules executed against the input BOM structure. Data Map syntax is in compliance with the schema
        defined in tcsim_xslWithNode.xsd, located in TC_DATA.
        
        Data Map rules define the mapping between an input item type and its resulting output item type. Data Map rules
        are defined for an entire site and are stored in the datamapping.xml file located in TC_DATA. The name of the
        datampping file is defined by the site preference CAE_dataMapping_file.
        
        The Data Map rules can be configured for various domains defined as LOV objects under StructureMap Domains in
        BMIDE. To configure the domains, in the Extensions view in BMIDE, open LOV->StructureMap Domains and add
        additional domain values. The domain to be used for applying Data Map rules can also be provided as an input.
        
        To use this operation, a well-defined datamapping.xml is required in TC_DATA and the user should have either a
        simulation_author or rtt_author license.
        
        
        Use cases:
        Use Case 1: Create an output structure given a top BOMLine of the input structure along with its configuration
        Given an input root BOMLine of a BOM structure, along with its RevisionRule and VariantRule, the user can apply
        Data Map rule to the BOM structure and generate a corresponding output BOM structure. The output BOM structure
        would consist of BOMLine occurrences of ItemRevision objects as defined in the datamapping.xml file. The user
        can review the actions executed with the process log returned with the BOMViewRevision. An email notification
        containing the activity log would be sent to the current user if the session option for email notification is
        set to true.
        
        Use Case 2: Create an output structure given a Snapshot folder of the input structure along with the variant
        rule
        Given a Snapshot folder of the input BOM structure and its VariantRule, the user can apply Data Map rules to
        the BOM structure and generate a corresponding output BOM structure. The output BOM structure would consist of
        BOMLine occurrences of ItemRevision objects as defined in the datamapping.xml file. The user can review the
        actions executed with the process log returned with the BOMViewRevision. An email notification containing the
        activity log would be sent to the current user if the session option for email notification is set to true.
        """
        return cls.execute_soa_method(
            method_name='executeDatamap',
            library='Cae',
            service_date='2012_02',
            service_name='StructureManagement',
            params={'rootIR': rootIR, 'snapshotFolder': snapshotFolder, 'revRule': revRule, 'variantRule': variantRule, 'domain': domain},
            response_cls=ExecuteRuleResponse2,
        )

    @classmethod
    def executeStructureMap(cls, rootIR: ItemRevision, snapshotFolder: Snapshot, revRule: RevisionRule, variantRule: VariantRule, structureMapIR: StructureMapRevision) -> ExecuteRuleResponse2:
        """
        This operation creates an output BOM structure given the root ItemRevision of the root BOMLine of an input BOM
        structure along with its RevisionRule and the VariantRule. A Snapshot folder of the input BOM structure along
        with the VariantRule can also be provided as an input. The output BOM structure is determined by a combination
        of XSLT-based Data Map and StructureMap rules executed against the input BOM structure. Data Map/StructureMap
        syntax is in compliance with the schema defined in tcsim_xslWithNode.xsd, located in TC_DATA.
        
        Data Map rules define the mapping between an input item type and its resulting output item type. Data Map rules
        are defined for an entire site and are stored in the datamapping.xml file located in TC_DATA. The name of the
        data mapping file is defined by the site preference CAE_dataMapping_file.
        
        StructureMap rules tailor the output BOM Structure. There are several rule types:
        - Filter - Removes input BOM lines (and their children) from Data Map evaluation.
        - Include - Inserts item revisions in either the input or output BOM structure as required.
        - Reuse - Retrieve existing item revision to be used in the output structure.
        - Create Collector - Reorganization rule that creates "container" item revisions to move BOMLine objects and
        sub-assemblies around.
        - Move to Collector - Reorganizational rule that moves BOMLine objects and sub-assemblies to collector
        components.
        - Collapse Single Component Assembly - Identifying sub-assemblies with single child component, elevating the
        child component to the parent sub-assembly and removing the parent sub-assembly.
        - Remove Empty Assembly - Identifying sub-assemblies with no child components and removing the empty
        sub-assembly.
        - Skip - Skips the BOMLine but still process its children.
        
        
        
        StructureMap rules are stored an XML named reference in CAEStructureMap dataset attached to a
        StructureMapRevision. StructureMap rules are created with Simulation Process Management CAE Structure Designer.
        
        To use this operation, a well-defined datamapping.xml is required in TC_DATA and a StructureMapRevision with an
        attached CAEStructureMap dataset must exist and the user should have either a simulation_author or rtt_author
        license.
        
        Use cases:
        Use Case 1: 
        Given an input root BOMLine of a BOM structure, along with its RevisionRule and VariantRule, the user can apply
        a StructureMap rule to the BOM structure and generate a corresponding output BOM structure. The output BOM
        structure would consist of BOMLine occurrences of ItemRevision objects as defined in the datamapping.xml file
        and would be organized by the StructureMap rules defined in the CAEStructureMap dataset attached to the
        StructureMapRevision. The user can review the actions executed with the process log returned with the
        BOMViewRevision. An email notification containing the activity log would be sent to the current user if the
        session option for email notification is set to true.
        
        Use Case 2: 
        Given a Snapshot folder of the input BOM structure and its VariantRule, the user can apply a StructureMap rule
        to the BOM structure and generate a corresponding output BOM structure. The output BOM structure would consist
        of BOMLine occurrences of ItemRevision objects as defined in the datamapping.xml file and would be organized by
        the StructureMap rules defined in the CAEStructureMap dataset attached to the StructureMapRevision. The user
        can review the actions executed with the process log returned with the BOMViewRevision. An email notification
        containing the activity log would be sent to the current user if the session option for email notification is
        set to true.
        """
        return cls.execute_soa_method(
            method_name='executeStructureMap',
            library='Cae',
            service_date='2012_02',
            service_name='StructureManagement',
            params={'rootIR': rootIR, 'snapshotFolder': snapshotFolder, 'revRule': revRule, 'variantRule': variantRule, 'structureMapIR': structureMapIR},
            response_cls=ExecuteRuleResponse2,
        )
