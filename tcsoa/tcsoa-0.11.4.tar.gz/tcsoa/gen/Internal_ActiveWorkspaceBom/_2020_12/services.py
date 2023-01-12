from __future__ import annotations

from tcsoa.gen.Internal.ActiveWorkspaceBom._2020_12.OccurrenceManagement import OccTypesInputData, RemoveLevelInputData, RemoveLevelResponse, InfoForInsertLevelData, ResetWorkingContextResp, InfoForInsertLevelResp, ResetWorkingContextInputData, InsertLevelResponse2, OccTypesResp, InsertLevelInputData2
from tcsoa.base import TcService


class OccurrenceManagementService(TcService):

    @classmethod
    def getAllowedOccurrenceTypes(cls, inputData: OccTypesInputData) -> OccTypesResp:
        """
        This operation retrieves a list of allowed occurrence type names. The operation also supports filtering of
        allowed occurrence types based on Teamcenter preference MEDisplayOccurrenceType.
        
        Use cases:
        Use case 1: You want to set an occurrence type on Awb0Element or BOMLine from Active Workspace. You can
        retrieve a list of valid occurrence types using this operation before setting a specific occurrence type.
        
        Use case 2: You want to copy Awb0Element or BOMLine and paste on other Awb0Element or BOMLine using paste
        sub-menu having allowed occurrence types. This operation can be used to create list of the sub-menu options.
        
        Use case 3: You want to assign a Resource (Item/Item Revision) from classification to an Operation (Item/Item
        Revision). This operation can be used to get list of allowed occurrence types.
        """
        return cls.execute_soa_method(
            method_name='getAllowedOccurrenceTypes',
            library='Internal-ActiveWorkspaceBom',
            service_date='2020_12',
            service_name='OccurrenceManagement',
            params={'inputData': inputData},
            response_cls=OccTypesResp,
        )

    @classmethod
    def getInfoForInsertLevel(cls, getInfoForInsertLevelIn: InfoForInsertLevelData) -> InfoForInsertLevelResp:
        """
        This operation retrieves valid parent type name(s) for given selectedElements based on preferences
        "TCAllowedParentTypes_<ChildItemType>" and "TCAllowedChildTypes_<ParentItemType>". Response contains preferred
        type as first value in preference "TCAllowedChildTypes_<ParentItemType>". When preference does not exist then
        parent of selectedElements is preferred parent type. 
        The operation returns allowed parent occurrence revision type name(s) for selectedElements when input has
        fetchAllowedOccRevTypes set to true.
        If fetchAllowedOccRevTypes is set and TCAllowedParentOccRevTypes_<ChildItemType> do not exists, then the
        operation returns preferred type as parent occurrence type of selectedElements; otherwise preferred type is the
        first type specified in TCAllowedParentOccRevTypes_<ChildItemType> preference.
        """
        return cls.execute_soa_method(
            method_name='getInfoForInsertLevel',
            library='Internal-ActiveWorkspaceBom',
            service_date='2020_12',
            service_name='OccurrenceManagement',
            params={'getInfoForInsertLevelIn': getInfoForInsertLevelIn},
            response_cls=InfoForInsertLevelResp,
        )

    @classmethod
    def insertLevel2(cls, insertLevelInput: InsertLevelInputData2) -> InsertLevelResponse2:
        """
        This operation removes elements from existing parent and adds them under a new parent for given
        objectToBeInserted . The content is saved as part of this operation.
        """
        return cls.execute_soa_method(
            method_name='insertLevel2',
            library='Internal-ActiveWorkspaceBom',
            service_date='2020_12',
            service_name='OccurrenceManagement',
            params={'insertLevelInput': insertLevelInput},
            response_cls=InsertLevelResponse2,
        )

    @classmethod
    def removeLevel(cls, inputData: RemoveLevelInputData) -> RemoveLevelResponse:
        """
        This operation removes the input Awb0Element objects from content and adds its children to the parent of input
        Awb0Element object.
        """
        return cls.execute_soa_method(
            method_name='removeLevel',
            library='Internal-ActiveWorkspaceBom',
            service_date='2020_12',
            service_name='OccurrenceManagement',
            params={'inputData': inputData},
            response_cls=RemoveLevelResponse,
        )

    @classmethod
    def resetUserWorkingContextState(cls, inputData: ResetWorkingContextInputData) -> ResetWorkingContextResp:
        """
        This operation reset the user's working state. User working state includes configuration and application data
        such as diagram layout and visualization aspects. If user working state does not exist then a new user working
        state with default configuration specified in Awb0ProductContextInfo is created.
        """
        return cls.execute_soa_method(
            method_name='resetUserWorkingContextState',
            library='Internal-ActiveWorkspaceBom',
            service_date='2020_12',
            service_name='OccurrenceManagement',
            params={'inputData': inputData},
            response_cls=ResetWorkingContextResp,
        )
