from __future__ import annotations

from tcsoa.gen.StructureManagement._2012_09.Structure import AddParam, AddResponse, ParentChildPair
from tcsoa.gen.BusinessObjects import BOMLine, ItemRevision
from tcsoa.gen.StructureManagement._2012_09.VariantManagement import CreateAndSubsVIResponse, CreateAndSubsVIInput, CreateVIInput, CreateVIResponse
from typing import List
from tcsoa.gen.StructureManagement._2012_09.MassUpdate import MassUpdateExecuteECRresponse, MassUpdateAffectedResponse, MassUpdateExecuteECRinput, MassUpdateExecuteECNresponse, MassUpdateAffectedInput
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class MassUpdateService(TcService):

    @classmethod
    def massGetAffectedParents(cls, input: List[MassUpdateAffectedInput]) -> MassUpdateAffectedResponse:
        """
        This operation will call ITK PS__masschange_get_parents to get all the affected impacted parent parts and there
        selectablility for mass update.
        """
        return cls.execute_soa_method(
            method_name='massGetAffectedParents',
            library='StructureManagement',
            service_date='2012_09',
            service_name='MassUpdate',
            params={'input': input},
            response_cls=MassUpdateAffectedResponse,
        )

    @classmethod
    def massUpdateExecutionECN(cls, changeItemRevs: List[ItemRevision]) -> MassUpdateExecuteECNresponse:
        """
        This operation will call ITK PS__masschange_execute which will process all the change item revision markup
        changes recorded during the ECR CM process.
        """
        return cls.execute_soa_method(
            method_name='massUpdateExecutionECN',
            library='StructureManagement',
            service_date='2012_09',
            service_name='MassUpdate',
            params={'changeItemRevs': changeItemRevs},
            response_cls=MassUpdateExecuteECNresponse,
        )

    @classmethod
    def massUpdateExecutionECR(cls, input: List[MassUpdateExecuteECRinput]) -> MassUpdateExecuteECRresponse:
        """
        This operation will call one of three ITKs: execute mode=1 calls PS__PS__masschange_onetime, execute mode=2
        calls PS__masschange_authorize_add and execute mode=3 calls PS__masschange_authorize_remove.
        """
        return cls.execute_soa_method(
            method_name='massUpdateExecutionECR',
            library='StructureManagement',
            service_date='2012_09',
            service_name='MassUpdate',
            params={'input': input},
            response_cls=MassUpdateExecuteECRresponse,
        )


class VariantManagementService(TcService):

    @classmethod
    def createAndSubstituteVariantItem(cls, createAndSubstituteVIInput: List[CreateAndSubsVIInput]) -> CreateAndSubsVIResponse:
        """
        This operation will create new variant Item for given BOMLine (also called as 'Generic BOMLine') from a BOM
        structure (also called as 'Generic Structure') having variability using variants. Addition to creating new
        variant Item, this is operation will also replace or substitute newly created variant Item Revision in given
        target BOMLine (also called as 'VI BOMLine') in variant Structure which corresponding to fully configured
        structure by fixing variability in Generic BOM Structure.
        
        Operation also accepts 2 flags ''findVIBeforeCreate'' used to control if existing variant Item should be
        searched and used instead of creating new variant Item and ''linkVIToGenericItem'' to link newly created
        variant Item to source Item of generic BOMLine.
        
        The new variant Item can be created in 2 ways either creating new separate Item or doing "Save-As" operation on
        generic Item. In case of "Save-As" the parameter ''CreateOrSaveAsDescriptor'' will provide additional
        information about which all related objects are carried over to new Item from source generic Item.
        
        
        Use cases:
        This operation should be used when user has Generic Structure & corresponding created variant Structure and
        user wants to create Item which is variant for each child BOMLine object and replace in variant Structure.
        """
        return cls.execute_soa_method(
            method_name='createAndSubstituteVariantItem',
            library='StructureManagement',
            service_date='2012_09',
            service_name='VariantManagement',
            params={'createAndSubstituteVIInput': createAndSubstituteVIInput},
            response_cls=CreateAndSubsVIResponse,
        )

    @classmethod
    def createVariantItem(cls, createVIInputs: List[CreateVIInput]) -> CreateVIResponse:
        """
        This operation will create new variant Item for given BOMLine (also called as 'Generic BOMLine') from a BOM
        structure (also called as 'Generic Structure') having variability using variant Options.
        
        Operation also accepts a flag ''linkVIToGenericItem'' to link newly created variant Item to source Item of
        'generic BOMLine'.
        
        The new variant Item can be created in 2 ways either by creating new separate Item or doing "Save-As" operation
        on generic Item. In case of "Save-As" the parameter 
        ''CreateOrSaveAsDescriptor'' will provide additional information about which all related objects are carried
        over to new Item from source generic Item.
        
        
        Use cases:
        This operation should be used when user wants to create new variant Item using generic BOMLine from a generic
        BOM structure.
        """
        return cls.execute_soa_method(
            method_name='createVariantItem',
            library='StructureManagement',
            service_date='2012_09',
            service_name='VariantManagement',
            params={'createVIInputs': createVIInputs},
            response_cls=CreateVIResponse,
        )


class StructureService(TcService):

    @classmethod
    def validateOccurrenceConditions(cls, lines: List[BOMLine], flag: int) -> ServiceData:
        """
        The operation is to validate occurrences of specified lines and their substitutes against occurrence conditions
        with option to validate the whole substructure.
        
        Use cases:
        User imports a structure which has some substitutes and wants to validate the structure against occurrence
        conditions.  Invoke the operation by passing in the root line and the flag for recursive validation. Failed
        BOMLine validations are returned in the 'ServiceData' object.
        """
        return cls.execute_soa_method(
            method_name='validateOccurrenceConditions',
            library='StructureManagement',
            service_date='2012_09',
            service_name='Structure',
            params={'lines': lines, 'flag': flag},
            response_cls=ServiceData,
        )

    @classmethod
    def validateParentChildConditions(cls, input: List[ParentChildPair]) -> ServiceData:
        """
        The operation is to validate parent and child objects against occurrence conditions.
        
        Use cases:
        User invokes the operation to validate against occurrence conditions before creating two occurrences by using
        an ItemRevision as parent for the two occurrences and a General Design Element object as one child and another
        ItemRevision as another child.
        """
        return cls.execute_soa_method(
            method_name='validateParentChildConditions',
            library='StructureManagement',
            service_date='2012_09',
            service_name='Structure',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def add(cls, input: List[AddParam]) -> AddResponse:
        """
        The operation adds business objects as child lines or substitutes of the specified lines with option to
        propagate transform matrix.
        .  The business objects can be item, item revision, General Design Elements, ImanItemLines or GDELines
        . If the business object to be added is a pending cut line, then the pending cut line will be processed after
        it is added.
        . If the business object is a WorkArea object or a line of WorkArea object and the object is to be added to
        WorkArea structure, then it will be added with predecessor relation.
        . If the object to be added is a line that contains Incremental Change Elements, the elements will be carried
        over to the newly created line.
        . BOMLine property values can be specified for the new line.
        . Occurrence type can be specified for the newline as one BOMLine property but will be handled specially.
        
        Use cases:
        - User  wants to add an item to a line. He/she invokes the operation to add it with initial values for find 
        number, quantity, etc. The line will be created with the initial BOMLine properties.
        - User wants to add an item revision as a substitute of a precise line. He/she invokes the operation to add it.
        - User invokes the operation to copy and paste a line. The Incremental Change Elements are carried over to the
        new line.
        - User invokes the operation to cut and paste a GDE line.
        - User paste a WorkArea object to a WorkArea structure, the newly added line is also added with the predecessor
        relationship.
        
        """
        return cls.execute_soa_method(
            method_name='add',
            library='StructureManagement',
            service_date='2012_09',
            service_name='Structure',
            params={'input': input},
            response_cls=AddResponse,
        )


class PublishByLinkService(TcService):

    @classmethod
    def deleteLinksForSource2(cls, sourceBOMLines: List[BOMLine], dataToUnpublish: str) -> ServiceData:
        """
        Finds and deletes PublishLink for input source BOMLine objects. 
        
        The AbsOccXform of the target BOMLine objects will be deleted if 'dataToUnpublish' is TRANSFORM. All in context
        JTs of the target BOMLine objects will be unattached if 'dataToUnpublish' is SHAPE. If all data(as of now
        TRANSFORM and SHAPE only) needs to be removed then value of 'dataToUnpublish' should be ALL. None of the
        published data will be impacted when 'dataToPublish' is empty string.
        
        Use cases:
        Delete PublishLink and unpublish data from target BOMLine.
        """
        return cls.execute_soa_method(
            method_name='deleteLinksForSource2',
            library='StructureManagement',
            service_date='2012_09',
            service_name='PublishByLink',
            params={'sourceBOMLines': sourceBOMLines, 'dataToUnpublish': dataToUnpublish},
            response_cls=ServiceData,
        )
