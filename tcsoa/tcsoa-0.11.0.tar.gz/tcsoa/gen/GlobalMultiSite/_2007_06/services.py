from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, TransferOptionSet
from tcsoa.gen.GlobalMultiSite._2007_06.ImportExport import GetAllTransferOptionSetsResponse, CreateOrUpdatePropertySetRuleResponse, GetPropertySetsResponse, CreateOrUpdatePropertySetInputData, GetTransferModesResponse, CreateOrUpdateTransferModeResponse, CreateOrUpdateClosureRuleInputData, CreateOrUpdateTransferModeInputData, CreateOrUpdateFilterRuleResponse, CreateOrUpdateActionRuleInputData, CreateOrUpdateActionRuleResponse, GetAvailableTransferOptionSetsInputData, GetAvailableTransferOptionSetsResponse, GetActionRulesResponse, CreateOrUpdateClosureRuleResponse, GetPLMXMLRuleInputData, NamesAndValue, CreateOrUpdateTransferOptionSetInputData, RequestImportFromOfflinePackageResponse, CreateOrUpdateTransferOptionSetResponse, GetFilterRulesResponse, CreateOrUpdateFilterRuleInputData, GetClosureRulesResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ImportExportService(TcService):

    @classmethod
    def getPropertySets(cls, inputs: GetPLMXMLRuleInputData) -> GetPropertySetsResponse:
        """
        This operation return a set of property set objects depending upon input query parameters.
        """
        return cls.execute_soa_method(
            method_name='getPropertySets',
            library='GlobalMultiSite',
            service_date='2007_06',
            service_name='ImportExport',
            params={'inputs': inputs},
            response_cls=GetPropertySetsResponse,
        )

    @classmethod
    def getTransferModes(cls, inputs: GetPLMXMLRuleInputData) -> GetTransferModesResponse:
        """
        This operation returns a set of transfer mode objects depending upon input query parameters.
        """
        return cls.execute_soa_method(
            method_name='getTransferModes',
            library='GlobalMultiSite',
            service_date='2007_06',
            service_name='ImportExport',
            params={'inputs': inputs},
            response_cls=GetTransferModesResponse,
        )

    @classmethod
    def requestImportFromOfflinePackage(cls, fmsTicket: str, optionSetTag: TransferOptionSet, optionNamesAndValues: List[NamesAndValue], sessionOptionAndValues: List[NamesAndValue]) -> RequestImportFromOfflinePackageResponse:
        """
        This operation imports the contents of the briefcase container into database by placing a request to the Global
        Services (GS) components. This operation is very much similar to importObjectsFromOfflinePackage with the
        exception that this operation is used in GS enabled environment whereas importObjectsFromOfflinePackage
        operation is used in Non GS environment. A packed briefcase contains a TC XML file which holds a serious of
        Teamcenter objects and related physical dataset files. After import, those objects will be replica in the
        importing site.
        
        Use cases:
        In data exchange, user may transfer a briefcase file from the source site to a remote site. In the importing
        site, user can use this operation to import the briefcase file into the Teamcenter. After import, the objects
        held in the TC XML file will be created or updated if they have been imported before, physical dataset files
        will uploaded and attached to the related datasets.
        The SOA needs the GS (Global Service) been configured for the importing site.
        """
        return cls.execute_soa_method(
            method_name='requestImportFromOfflinePackage',
            library='GlobalMultiSite',
            service_date='2007_06',
            service_name='ImportExport',
            params={'fmsTicket': fmsTicket, 'optionSetTag': optionSetTag, 'optionNamesAndValues': optionNamesAndValues, 'sessionOptionAndValues': sessionOptionAndValues},
            response_cls=RequestImportFromOfflinePackageResponse,
        )

    @classmethod
    def createOrUpdateActionRules(cls, inputs: List[CreateOrUpdateActionRuleInputData]) -> CreateOrUpdateActionRuleResponse:
        """
        Creates or updates an action rule based on input parameters. Action rule in the PLM XML framework is used to
        invoke additional actions before/during/after import/export. For more information on action rules, please refer
        to PLM XML Import Export Administration Guide.
        
        Use cases:
        Use Case 1: Modify an Action Rule
        The following types of modifications can be done on existing action rule using 'createOrUpdateActionRules'
        operation:
        - Change the rule description.
        - Change the action handler. This means that we can change the action rule's clause to invoke a different
        action than what was initially assigned.
        - Change the action location. This means we can change action location from pre-action to post-action etc.
        - Change the schema format. This means we can change the action rule from PLM XML schema based one to TC XML
        schema.
        - Change data transfer direction scope. This means we can change the direction from export to import and
        vice-versa.
        
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateActionRules',
            library='GlobalMultiSite',
            service_date='2007_06',
            service_name='ImportExport',
            params={'inputs': inputs},
            response_cls=CreateOrUpdateActionRuleResponse,
        )

    @classmethod
    def createOrUpdateClosureRules(cls, inputs: List[CreateOrUpdateClosureRuleInputData]) -> CreateOrUpdateClosureRuleResponse:
        """
        Creates or updates a closure rule based on input parameters. Closure rule specify how the data structure is
        traversed by specifying which relationships are of interest and what should be done when these relationships
        are encountered. For more information, please refer to PLM XML Import Export Administration Guide.
        
        Use cases:
        Use Case 1: Modify a Closure Rule
        The following types of modifications can be done on existing closure rule using 'createOrUpdateClosureRules'
        operation:
        - Change the closure rule description.
        - Change schema format. This means we can change the closure rule from PLM XML schema based one to TC XML
        schema.
        - Change transfer direction. This means we can change the direction from export to import and vice-versa.
        - Change clause contents, depth and comments for each clause. You can change detailed clauses in this closure
        rule. For more information to how to write clauses, please refer to PLM XML Import Export Administration Guide.
        
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateClosureRules',
            library='GlobalMultiSite',
            service_date='2007_06',
            service_name='ImportExport',
            params={'inputs': inputs},
            response_cls=CreateOrUpdateClosureRuleResponse,
        )

    @classmethod
    def createOrUpdateFilterRules(cls, inputs: List[CreateOrUpdateFilterRuleInputData]) -> CreateOrUpdateFilterRuleResponse:
        """
        Creates or updates a filter rule based on input parameters. Filter rules allow a finer level of control over
        the data that gets translated along with the primary objects by specifying that a user-written function is
        called to determine the operation applied against a given object. For more information, please refer to PLM XML
        Import Export Administration Guide.
        
        Use cases:
        Use Case 1: Modify a Filter Rule
        The following types of modifications can be done on existing filter rule using 'createOrUpdateFilterRules'
        operation:
        - Change the filter rule description.
        - Change clauses. For more information about how to write clause, please refer to PLM XML Import Export
        Administration Guide.
        - Change schema format. This means we can change the filter rule from PLM XML schema based one to TC XML schema.
        - Change data transfer direction scope. This means we can change the direction from export to import and
        vice-versa.
        
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateFilterRules',
            library='GlobalMultiSite',
            service_date='2007_06',
            service_name='ImportExport',
            params={'inputs': inputs},
            response_cls=CreateOrUpdateFilterRuleResponse,
        )

    @classmethod
    def createOrUpdatePropertySets(cls, inputs: List[CreateOrUpdatePropertySetInputData]) -> CreateOrUpdatePropertySetRuleResponse:
        """
        Creates or updates a property set based on input parameters. Property sets provide a non-programmatic way to
        control what is placed in the UserData element. For more information, please refer to PLM XML Import Export
        Administration Guide.
        
        Use cases:
        Use Case 1: Modify a Property Set
        The following types of modifications can be done on existing property set using 'createOrUpdatePropertySets'
        operation:
        - Change the property set description.
        - Change data transfer direction scope. This means we can change the direction from export to import and
        vice-versa.
        - Change clauses. For more information about how to write clause, please refer to PLM XML Import Export
        Administration Guide.
        
        """
        return cls.execute_soa_method(
            method_name='createOrUpdatePropertySets',
            library='GlobalMultiSite',
            service_date='2007_06',
            service_name='ImportExport',
            params={'inputs': inputs},
            response_cls=CreateOrUpdatePropertySetRuleResponse,
        )

    @classmethod
    def createOrUpdateTransferModes(cls, inputs: List[CreateOrUpdateTransferModeInputData]) -> CreateOrUpdateTransferModeResponse:
        """
        Creates or updates a transfer mode based on input parameters. Transfer modes are created in the PLMXML
        application. Transfer modes define how to import/export data between PLMXML file and sites. For more
        information, please refer to PLM XML Import Export Administration Guide.
        
        Use cases:
        Use Case 1: Modify a Transfer Mode
        The following types of modifications can be done on existing transfer mode using 'createOrUpdateTransferModes'
        operation. 
        - Change the transfer mode description
        - Change context string. Context string is used to map the transfer mode object to a customized processor for
        the given object type. For more information, please refer to PLM XML Import Export Administration Guide.
        - Change data transfer direction scope. This means we can change the direction from export to import and
        vice-versa.
        - Change schema format. This means we can change the closure rule from PLM XML schema based one to TC XML
        schema.
        - Change Incremental setting.  This option allows updates to existing data during PLM XML import. For example,
        if an item being imported from an .xml file already exists in the database and "support incremental" is
        selected, the PLM XML import updates the item. If "support incremental" is not selected, the updates from the
        .xml file are ignored.
        - Change closure rule, filter rule, property set, revision rule and action rule which are used by this transfer
        mode.
        
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateTransferModes',
            library='GlobalMultiSite',
            service_date='2007_06',
            service_name='ImportExport',
            params={'inputs': inputs},
            response_cls=CreateOrUpdateTransferModeResponse,
        )

    @classmethod
    def createOrUpdateTransferOptionSets(cls, inputs: List[CreateOrUpdateTransferOptionSetInputData]) -> CreateOrUpdateTransferOptionSetResponse:
        """
        Creates or update a list of transfer option sets based on the input properties structure. The transfer option
        set contains a set of variables which will control the export/import behavior. For more information, please
        refer to PLM XML Import Export Administration Guide.
        
        Use cases:
        Use Case 1: Modify a Transfer Option Set
        The following types of modifications can be done on existing transfer option set using
        createOrUpdateTransferOptionSets operation: 
        - Change the transfer option set description
        - Change referenced site id. It shows whether the transfer option set is for a remote site, thus an import. If
        so, its remote site ID is included. 
        - Change the attached transfer mode id.
        - Change the detail options for the transfer option set. For more information to the options, please refer to
        PLM XML Import Export Administration Guide.
        
        
        
        Exceptions:
        >203406    If the operation fails to create transfer option set.
        203407    If the operation fails to modify transfer option set.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateTransferOptionSets',
            library='GlobalMultiSite',
            service_date='2007_06',
            service_name='ImportExport',
            params={'inputs': inputs},
            response_cls=CreateOrUpdateTransferOptionSetResponse,
        )

    @classmethod
    def getActionRules(cls, inputs: GetPLMXMLRuleInputData) -> GetActionRulesResponse:
        """
        This operation return a set of action rule objects depending upon input query parameters.
        
        Exceptions:
        >203419    If schema input is incorrect.
        203420    If the scope input is incorrect.
        203424    If the query cannot find action rules.
        203414    If the query fails to execute to while fetching the action rules from database.
        """
        return cls.execute_soa_method(
            method_name='getActionRules',
            library='GlobalMultiSite',
            service_date='2007_06',
            service_name='ImportExport',
            params={'inputs': inputs},
            response_cls=GetActionRulesResponse,
        )

    @classmethod
    def getAllTransferOptionSets(cls) -> GetAllTransferOptionSetsResponse:
        """
        This operation return a set of transfer option set objects that were created with scope - public.
        
        Exceptions:
        >Other exception throwed by called API.
        """
        return cls.execute_soa_method(
            method_name='getAllTransferOptionSets',
            library='GlobalMultiSite',
            service_date='2007_06',
            service_name='ImportExport',
            params={},
            response_cls=GetAllTransferOptionSetsResponse,
        )

    @classmethod
    def getAvailableTransferOptionSets(cls, inputs: GetAvailableTransferOptionSetsInputData) -> GetAvailableTransferOptionSetsResponse:
        """
        This operation return a set of transfer option set object depending upon input query parameters.
        """
        return cls.execute_soa_method(
            method_name='getAvailableTransferOptionSets',
            library='GlobalMultiSite',
            service_date='2007_06',
            service_name='ImportExport',
            params={'inputs': inputs},
            response_cls=GetAvailableTransferOptionSetsResponse,
        )

    @classmethod
    def getClosureRules(cls, inputs: GetPLMXMLRuleInputData) -> GetClosureRulesResponse:
        """
        This operation return a set of closure rule objects depending upon input query parameters.
        """
        return cls.execute_soa_method(
            method_name='getClosureRules',
            library='GlobalMultiSite',
            service_date='2007_06',
            service_name='ImportExport',
            params={'inputs': inputs},
            response_cls=GetClosureRulesResponse,
        )

    @classmethod
    def getFilterRules(cls, inputs: GetPLMXMLRuleInputData) -> GetFilterRulesResponse:
        """
        This operation return a set of filter rule objects depending upon input query parameters.
        """
        return cls.execute_soa_method(
            method_name='getFilterRules',
            library='GlobalMultiSite',
            service_date='2007_06',
            service_name='ImportExport',
            params={'inputs': inputs},
            response_cls=GetFilterRulesResponse,
        )


class SiteReservationService(TcService):

    @classmethod
    def siteCheckIn(cls, objects: List[BusinessObject]) -> ServiceData:
        """
        This operation is used in offline GMS. It is used to check in objects that were checked out to another site and
        removes the reservation objects. If errors occur, they are returned in the ServiceData structure.
        
        Use cases:
        User can pass a list of objects which have been in site checked out status to do site check in. A series of
        related objects will be site checked in along with the input objects Item, ItemRevision or Dataset:
        - Item        Related Master Form(s)
        - ItemRevision    Related Master Form(s)
        - Dataset        All namedReference objects which are WorkspaceObject
        
        """
        return cls.execute_soa_method(
            method_name='siteCheckIn',
            library='GlobalMultiSite',
            service_date='2007_06',
            service_name='SiteReservation',
            params={'objects': objects},
            response_cls=ServiceData,
        )

    @classmethod
    def siteCheckOut(cls, objects: List[BusinessObject], siteId: int, comment: str, changeId: str) -> ServiceData:
        """
        This operation is used in offline GMS. It is used to checkout objects to another site, so that after the
        objects are imported into that site, they are modifiable. If errors occur, they are returned in the ServiceData
        structure.
        
        Use cases:
        User can pass a list of objects (only these six types and their sub types are supported: Item, ItemRevision,
        Form, Dataset, BOMView, BOMViewRevision) to do site check out. A series of related objects will be site checked
        out along with the input objects Item, ItemRevision or Dataset:
        - Item        Related Master Form(s)
        - ItemRevision    Related Master Form(s)
        - Dataset        All namedReference objects which are WorkspaceObject
        
        
        
        Exceptions:
        >.
        """
        return cls.execute_soa_method(
            method_name='siteCheckOut',
            library='GlobalMultiSite',
            service_date='2007_06',
            service_name='SiteReservation',
            params={'objects': objects, 'siteId': siteId, 'comment': comment, 'changeId': changeId},
            response_cls=ServiceData,
        )

    @classmethod
    def cancelSiteCheckOut(cls, objects: List[BusinessObject]) -> ServiceData:
        """
        This operation is used in offline GMS. It is used to cancel site check out objects which has been site checked
        out to another site and removes the reservation objects. If errors occur, they are returned in the ServiceData
        structure.
        
        Use cases:
        User can pass a list of objects which have been in site checked out status to do cancel site check in.
        """
        return cls.execute_soa_method(
            method_name='cancelSiteCheckOut',
            library='GlobalMultiSite',
            service_date='2007_06',
            service_name='SiteReservation',
            params={'objects': objects},
            response_cls=ServiceData,
        )
