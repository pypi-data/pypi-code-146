from __future__ import annotations

from tcsoa.gen.Internal.ActiveWorkspaceBom._2019_12.OccurrenceConfiguration import ConfigRuleResponse2, CreateOrUpdateClassicVariantRuleData, ClassicVariantsResp, ClassicVariantsData
from tcsoa.gen.Internal.ActiveWorkspaceBom._2017_06.OccurrenceConfiguration import ConfigRuleInput
from tcsoa.gen.Internal.ActiveWorkspaceBom._2019_12.OccurrenceManagement import FindMatchingFilterResponse2, RemoveInContextOverrides, SubsetResponse2, OccurrencesData3, DetachObjectsInputData, FindMatchingFilterInput2, InfoForAddElemData3, OccurrencesResp3
from tcsoa.gen.Internal.ActiveWorkspaceBom._2019_12.DataManagement import GetViewModelForCreateInfo, GetViewModelForCreateResponse
from tcsoa.gen.Internal.ActiveWorkspaceBom._2012_10.OccurrenceManagement import InfoForAddElemResp
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.gen.Internal.ActiveWorkspaceBom._2016_03.OccurrenceManagement import SubsetInput2
from tcsoa.base import TcService


class OccurrenceConfigurationService(TcService):

    @classmethod
    def createOrUpdateClassicVariantRule(cls, inputData: CreateOrUpdateClassicVariantRuleData) -> ClassicVariantsResp:
        """
        This operation sets options and values provided in the input for a given product context. It returns a
        VariantRule and list of option and associated list of value. When input contains VariantRule then the list of
        options and values provided in the input are merged with this input VariantRule.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateClassicVariantRule',
            library='Internal-ActiveWorkspaceBom',
            service_date='2019_12',
            service_name='OccurrenceConfiguration',
            params={'inputData': inputData},
            response_cls=ClassicVariantsResp,
        )

    @classmethod
    def getClassicVariants(cls, inputData: ClassicVariantsData) -> ClassicVariantsResp:
        """
        This operation returns list of option and associated list of value for given product context. When input
        contains VariantRule then the list of options and values are returned along with how set indication.
        """
        return cls.execute_soa_method(
            method_name='getClassicVariants',
            library='Internal-ActiveWorkspaceBom',
            service_date='2019_12',
            service_name='OccurrenceConfiguration',
            params={'inputData': inputData},
            response_cls=ClassicVariantsResp,
        )

    @classmethod
    def getConfigurationRules2(cls, input: ConfigRuleInput) -> ConfigRuleResponse2:
        """
        This operation returns a list of RevisionRule or VariantRule based on the input product context information.
        The number of RevisionRule or VariantRule in the response depends on the page size.
        """
        return cls.execute_soa_method(
            method_name='getConfigurationRules2',
            library='Internal-ActiveWorkspaceBom',
            service_date='2019_12',
            service_name='OccurrenceConfiguration',
            params={'input': input},
            response_cls=ConfigRuleResponse2,
        )


class OccurrenceManagementService(TcService):

    @classmethod
    def detachObjects(cls, input: List[DetachObjectsInputData]) -> ServiceData:
        """
        This operation detaches the secondary objects from the primary object.
        """
        return cls.execute_soa_method(
            method_name='detachObjects',
            library='Internal-ActiveWorkspaceBom',
            service_date='2019_12',
            service_name='OccurrenceManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def findMatchingFilters2(cls, input: List[FindMatchingFilterInput2]) -> FindMatchingFilterResponse2:
        """
        This operation retrieves filters matching input search string.
        """
        return cls.execute_soa_method(
            method_name='findMatchingFilters2',
            library='Internal-ActiveWorkspaceBom',
            service_date='2019_12',
            service_name='OccurrenceManagement',
            params={'input': input},
            response_cls=FindMatchingFilterResponse2,
        )

    @classmethod
    def getInfoForAddElement3(cls, getInfoForElementIn: InfoForAddElemData3) -> InfoForAddElemResp:
        """
        This operation retrieves information required for creating an Awb0Element under product specified in
        Awb0Element. Operation returns allowed child occurrence revision type name(s) for given parent type when
        "fetchAllowedOccRevTypes" is set to true. Otherwise operation returns allowed Item type name(s) for given
        parentElement. The operation also returns preferred type as parent type if that is specified as allowed child
        type in "TCAllowedChildTypes_<ParentItemType>" preference; otherwise preferred type is empty.
        """
        return cls.execute_soa_method(
            method_name='getInfoForAddElement3',
            library='Internal-ActiveWorkspaceBom',
            service_date='2019_12',
            service_name='OccurrenceManagement',
            params={'getInfoForElementIn': getInfoForElementIn},
            response_cls=InfoForAddElemResp,
        )

    @classmethod
    def getOccurrences3(cls, inputData: OccurrencesData3) -> OccurrencesResp3:
        """
        Retrieves the page of configured occurrences for given the top-level product and configuration parameters as
        input. The service provides the facility to optionally filter and sort the result by additional filters and
        sorting criteria that may be provided as input. The output also contains a cursor that defines the place to
        start the next page location. The cursor must be passed back in to any subsequent call to get the next page of
        occurrences.
        
        Exceptions:
        >Teamcenter::Soa::Server::ServiceException
        """
        return cls.execute_soa_method(
            method_name='getOccurrences3',
            library='Internal-ActiveWorkspaceBom',
            service_date='2019_12',
            service_name='OccurrenceManagement',
            params={'inputData': inputData},
            response_cls=OccurrencesResp3,
        )

    @classmethod
    def getSubsetInfo3(cls, subsetInputs: List[SubsetInput2]) -> SubsetResponse2:
        """
        This operation retrieves filters and recipes which are used to find matching Awb0Element objects for input
        Awb0ProductContextInfo.
        """
        return cls.execute_soa_method(
            method_name='getSubsetInfo3',
            library='Internal-ActiveWorkspaceBom',
            service_date='2019_12',
            service_name='OccurrenceManagement',
            params={'subsetInputs': subsetInputs},
            response_cls=SubsetResponse2,
        )

    @classmethod
    def removeInContextPropertyOverride(cls, removeInContextOverridesInfo: RemoveInContextOverrides) -> ServiceData:
        """
        The operation removes overridden property for the Awb0Element .
        
        Exceptions:
        >This operation may raise a ServiceException containing following 
        errors:
        
        126001 -  An internal error has occurred in the Occurrence Management Module.
        43021 -  The BOM View Revision cannot be modified. Please check your access rights.
        """
        return cls.execute_soa_method(
            method_name='removeInContextPropertyOverride',
            library='Internal-ActiveWorkspaceBom',
            service_date='2019_12',
            service_name='OccurrenceManagement',
            params={'removeInContextOverridesInfo': removeInContextOverridesInfo},
            response_cls=ServiceData,
        )


class DataManagementService(TcService):

    @classmethod
    def getViewModelForCreate(cls, input: GetViewModelForCreateInfo) -> GetViewModelForCreateResponse:
        """
        This operation retrieves view model definition to author WorkspaceObject. The response contains the definition
        of View Model information based on CreateInput object and client derives data to render the editable row UI
        element/widget to create the object. The editable row represents the ViewModelProperty for the CreateInput
        object. The editable cells represent the ViewModelProperty for the properties on CreateInput, cell value can
        have auto-assigned initial property value if any. This is like 'Add Panel' scenario, i.e. panel is based on
        'Form' view and this operation provides definition for 'Grid:Row' view display.
        
        Use cases:
        Use case 1: Create child under selected object.
        When user selects an object in Active Workspace to add new child, the operation getViewModelForCreate retrieves
        view model information to render widget to create an object.
        
        Use case 2: Create Sibling for a selected object.
        When user selects an object in Active Workspace to add new sibling, the operation getViewModelForCreate
        retrieves view model information to render widget to create an object.
        """
        return cls.execute_soa_method(
            method_name='getViewModelForCreate',
            library='Internal-ActiveWorkspaceBom',
            service_date='2019_12',
            service_name='DataManagement',
            params={'input': input},
            response_cls=GetViewModelForCreateResponse,
        )
