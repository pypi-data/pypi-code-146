from __future__ import annotations

from tcsoa.gen.Manufacturing._2013_05.ImportExport import AdvancedImportResponse, AdvancedImportInput
from tcsoa.gen.BusinessObjects import BusinessObject, WorkspaceObject
from tcsoa.gen.Manufacturing._2013_05.IPAManagement import IPATreeInput, GenerateIPATreeResponse, IPAExistResponse, CleanIPATreeResponse, LocalUpdateIPATreeResponse
from tcsoa.gen.Manufacturing._2009_10.DataManagement import CreateResponse, CreateIn
from tcsoa.gen.Manufacturing._2013_05.StructureManagement import FindAffectedCCsResponse
from tcsoa.gen.Manufacturing._2013_05.Core import MatchObjectsAgainstVariantRulesArg, MatchObjectsAgainstVariantRulesResponse, FindNodeInContextInputInfo
from tcsoa.gen.Manufacturing._2010_09.Core import FindNodeInContextResponse
from tcsoa.gen.Manufacturing._2013_05.StructureSearch import FindStudiesResponse
from typing import List
from tcsoa.gen.Manufacturing._2013_05.DataManagement import ObjectAttributesInput, SyncStudyResponse, SyncStudyInput
from tcsoa.gen.Manufacturing._2013_05.TimeWayPlan import TwpInfoInput, ProductImageInfo, TwpResponse
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class TimeWayPlanService(TcService):

    @classmethod
    def getTWPInformation(cls, input: TwpInfoInput) -> TwpResponse:
        """
        This service operation fetches the Time Way Plan (TWP) information. The operation takes objects from the plant
        Bill of Processes (BOP) for which TWP information is required, the list of strings specifying what information
        is required and the context product BOP. The object can be process station(s), process line(s), process
        area(s), or plant BOP. The list of string will have values "OperationDetails", "ExecutionPositions",
        "ProductDiagram", and "PlantCarpet" based on which response will contain the information. These values will be
        applicable to all the objects for which TWP information is required.
        
        This information is used to display the Time Way Plan view.
        """
        return cls.execute_soa_method(
            method_name='getTWPInformation',
            library='Manufacturing',
            service_date='2013_05',
            service_name='TimeWayPlan',
            params={'input': input},
            response_cls=TwpResponse,
        )

    @classmethod
    def setProductImage(cls, input: List[ProductImageInfo]) -> ServiceData:
        """
        This service operation sets a product image for the given input object. The operation takes objects from the
        plant Bill Of Processes (BOP) for which the product image is to be set, the business object of the context
        product BOP, and the business object of the dataset representing the product image. The object   from the plant
        BOP for which product image is to be set can be process station(s), process line(s), process area(s), or plant
        BOP. 
        This operation will create a relation between the object from the plant BOP input object and  the dataset
        business object in context of the input product BOP.
        The specified product image is displayed on the station in the Time Way Plan (TWP) view.
        """
        return cls.execute_soa_method(
            method_name='setProductImage',
            library='Manufacturing',
            service_date='2013_05',
            service_name='TimeWayPlan',
            params={'input': input},
            response_cls=ServiceData,
        )


class IPAManagementService(TcService):

    @classmethod
    def cleanIPATree(cls, processWindow: BusinessObject, forceCleanAll: bool) -> CleanIPATreeResponse:
        """
        This operation removes the In-Process Assembly (IPA) occurrences from the process structure and deletes the IPA
        occurrence group from product structure. This operation cleans only the IPA which has been configured by
        current configuration rule and configuring structure.
        """
        return cls.execute_soa_method(
            method_name='cleanIPATree',
            library='Manufacturing',
            service_date='2013_05',
            service_name='IPAManagement',
            params={'processWindow': processWindow, 'forceCleanAll': forceCleanAll},
            response_cls=CleanIPATreeResponse,
        )

    @classmethod
    def localUpdateIPATree(cls, processLines: List[BusinessObject]) -> LocalUpdateIPATreeResponse:
        """
        This operation is used to perform a local update on an In-Process Assembly (IPA) tree. Local update changes the
        IPA on which the operation is invoked. If necessary, it also updates the occurrence pointing to this in-process
        assembly in the process structure.
        
        If the IPA has not been created and attached to the matching process, Teamcenter also changes the matching
        process and adds the incoming IPA as MEWorkpiece. This happens only if a process whose type is in the process
        types list of the configuration details during the initial IPA generation.
        """
        return cls.execute_soa_method(
            method_name='localUpdateIPATree',
            library='Manufacturing',
            service_date='2013_05',
            service_name='IPAManagement',
            params={'processLines': processLines},
            response_cls=LocalUpdateIPATreeResponse,
        )

    @classmethod
    def updateIPATree(cls, ipaInput: IPATreeInput) -> GenerateIPATreeResponse:
        """
        This operation is used to update an In-Process Assembly (IPA) tree that already exists, when a process
        structure is changed. The options set at creation of the assembly tree may be changed for example process
        types, consumed occurrence types, name of the report on errors and problems, e-mail notification configuration.
        """
        return cls.execute_soa_method(
            method_name='updateIPATree',
            library='Manufacturing',
            service_date='2013_05',
            service_name='IPAManagement',
            params={'ipaInput': ipaInput},
            response_cls=GenerateIPATreeResponse,
        )

    @classmethod
    def doesIPAExist(cls, processWindow: BusinessObject) -> IPAExistResponse:
        """
        This operation checks if an In-Process Assembly tree exists for a process structure.
        """
        return cls.execute_soa_method(
            method_name='doesIPAExist',
            library='Manufacturing',
            service_date='2013_05',
            service_name='IPAManagement',
            params={'processWindow': processWindow},
            response_cls=IPAExistResponse,
        )

    @classmethod
    def generateIPATree(cls, ipaInput: IPATreeInput) -> GenerateIPATreeResponse:
        """
        An In-Process Assembly (IPA) is an aggregation of incoming parts into stations. IPA is generated based on
        consumed item(s) from a product structure in a process structure. Teamcenter creates a tree structure
        representing the IPA by traversing the process structure and collecting IPAs from previous process elements and
        adding the selected line's consumed objects. 
        
        The IPA is stored as an occurrence group and is displayed in a separate tab beside the base view of the root
        product.
        
        When the assembly tree is created by the operation, it places a configuration file as an attachment on the
        process for which the IPA is generated. 
        
        Teamcenter sends an e-mail notification to the recipients specified in the input after completion of the
        operation. This e-mail contains information about the IPA creation, as well as log files that are created
        during generation of the IPA.
        """
        return cls.execute_soa_method(
            method_name='generateIPATree',
            library='Manufacturing',
            service_date='2013_05',
            service_name='IPAManagement',
            params={'ipaInput': ipaInput},
            response_cls=GenerateIPATreeResponse,
        )


class ImportExportService(TcService):

    @classmethod
    def importManufacturingFeatures(cls, input: AdvancedImportInput) -> AdvancedImportResponse:
        """
        This service operation imports the discrete manufacturing features (MFGs) from a PLMXML file into a target
        product structure in Teamcenter.        This operation takes a scope line (container) as additional input and
        imports the MFGs under the container.        Moreover, it takes the import mode as input which allows deciding
        whether MFGs already present under the chosen container should be deleted or not.
        """
        return cls.execute_soa_method(
            method_name='importManufacturingFeatures',
            library='Manufacturing',
            service_date='2013_05',
            service_name='ImportExport',
            params={'input': input},
            response_cls=AdvancedImportResponse,
        )


class CoreService(TcService):

    @classmethod
    def matchObjectsAgainstVariantRules(cls, args: List[MatchObjectsAgainstVariantRulesArg]) -> MatchObjectsAgainstVariantRulesResponse:
        """
        This operation takes a list of pairs of runtime object and variant rule lists and determines for each
        object/variant rule combination of each pair whether the object is configured-in for the specified variant
        rule. Thereby it takes all aspects of an object into account that determine the visibility of the object, such
        as the variant conditions of the object itself and of all its parent objects as well as the conditions of any
        assigned object and that of its respective parent objects. The results will depend on the configuration state
        for IC, revision rule, effectivity etc of the implied windows, including reference windows.
        If a variant rule supplied in the arguments list is not matched by the variant configuration of any involved
        window a warning message will be added to the response structure, which indicates that the visibility check
        regarding the specific variant rule cannot be reliably performed because the configuration of the window
        contradicts the variant rule. 
        This operation currently does not support modular variants. Only saved variant rules (business object
        VariantRule) for the classic variant model are accepted or alternatively,  product variants (type
        Mfg0BvrProductVariant) which are linked to VariantRule objects. 
        """
        return cls.execute_soa_method(
            method_name='matchObjectsAgainstVariantRules',
            library='Manufacturing',
            service_date='2013_05',
            service_name='Core',
            params={'args': args},
            response_cls=MatchObjectsAgainstVariantRulesResponse,
        )

    @classmethod
    def findNodeInContext(cls, input: List[FindNodeInContextInputInfo]) -> FindNodeInContextResponse:
        """
        Getting the related objects of the selected object from the target contexts according to the input information.
        """
        return cls.execute_soa_method(
            method_name='findNodeInContext',
            library='Manufacturing',
            service_date='2013_05',
            service_name='Core',
            params={'input': input},
            response_cls=FindNodeInContextResponse,
        )


class DataManagementService(TcService):

    @classmethod
    def setAttributes(cls, input: List[ObjectAttributesInput]) -> ServiceData:
        """
        This service operation sets the attributes of objects attached to the business object(s). For example, if some
        attributes of a Form attached to an Item needs to be edited, this operation can be used. 
        The operation considers the Incremental Change applied on the window of the object whose attachment is to be
        edited.
        The operation takes the business objects of the BOMLine and its attached object which is to be edited. Along
        with that, it takes the name(s) of attributes  and their corresponding values to be set.
        This operation can set multiple attributes of multiple attached objects.
        """
        return cls.execute_soa_method(
            method_name='setAttributes',
            library='Manufacturing',
            service_date='2013_05',
            service_name='DataManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def syncStudyAndSource(cls, input: List[SyncStudyInput]) -> SyncStudyResponse:
        """
        This operation synchronizes a Simulation Study with the source BOP structure it is associated with.
        """
        return cls.execute_soa_method(
            method_name='syncStudyAndSource',
            library='Manufacturing',
            service_date='2013_05',
            service_name='DataManagement',
            params={'input': input},
            response_cls=SyncStudyResponse,
        )

    @classmethod
    def createAttachments(cls, input: List[CreateIn]) -> CreateResponse:
        """
        This service operation creates the attachment objects for a business object(s). 
        The operation considers the Incremental Change applied on the window of the object for which attachment is to
        be created.
        The operation takes following inputs.
        - clientId - Unique client Identifier.
        - context - The business objects of the BOM Line. The IC applied on the window of this line is considered while
        creating the attachment. 
        - target - The business object which is used as primary object to connect the newly created object. 
        - relation name - The name of the relation used to connect the target. 
        - data - Input data for create operation.
        
        """
        return cls.execute_soa_method(
            method_name='createAttachments',
            library='Manufacturing',
            service_date='2013_05',
            service_name='DataManagement',
            params={'input': input},
            response_cls=CreateResponse,
        )


class StructureManagementService(TcService):

    @classmethod
    def findAffectedCCs(cls, objects: List[WorkspaceObject]) -> FindAffectedCCsResponse:
        """
        This operation finds all of the Collaboration Contexts which contain a process structure, which contains the
        input objects (e.g. Item, MEWorkArea, METool, MEProcess or MEOperation). The input objects must be of type Item
        or ItemRevision (BOMLine objects are not valid input objects).
        
        Exceptions:
        >Throws:
        NotSupportedObjectType: If the input object isn't one of the supported types (it's not a subtype of an item or
        an item_revision).
        """
        return cls.execute_soa_method(
            method_name='findAffectedCCs',
            library='Manufacturing',
            service_date='2013_05',
            service_name='StructureManagement',
            params={'objects': objects},
            response_cls=FindAffectedCCsResponse,
        )


class StructureSearchService(TcService):

    @classmethod
    def findStudies(cls, inputNodes: List[BusinessObject]) -> FindStudiesResponse:
        """
        This operation finds all study objects that reference a given process/operation business object.
        """
        return cls.execute_soa_method(
            method_name='findStudies',
            library='Manufacturing',
            service_date='2013_05',
            service_name='StructureSearch',
            params={'inputNodes': inputNodes},
            response_cls=FindStudiesResponse,
        )
