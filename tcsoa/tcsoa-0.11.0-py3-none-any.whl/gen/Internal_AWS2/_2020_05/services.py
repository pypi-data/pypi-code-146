from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.AWS2._2020_05.UiConfig import StringMap, NamedColumnConfigInput, GetNamedColumnConfigsResponse, ColumnDefInfo
from tcsoa.gen.Internal.AWS2._2020_05.FileMgmt import GetFilesAndTicketsInfoResponse
from tcsoa.gen.Internal.AWS2._2020_05.DataManagement import GetRelatedObjectsResponse, RelatedObjectsInfo
from tcsoa.gen.Internal.AWS2._2020_05.FullTextSearch import GetSearchSettingsResponse, GetSearchSettingsInput
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def getRelatedObjsForConfiguredRevision(cls, input: List[RelatedObjectsInfo]) -> GetRelatedObjectsResponse:
        """
        This operation retrieves the underlying Item or ItemRevision related to source business object.
        
        Use Case:
        
        If Item is attached to Folder in database, Active Workspace client displays the Item as configured
        ItemRevision. The displayed ItemRevision will be as per the revision rule set by the user. If specific
        ItemRevision is attached to Folder in database, that specific ItemRevision is always displayed, irrespective of
        revision rule set by user.
        
        In such cases, underlying object in database is different from the object displayed on client.  When user
        performs a operation on displayed ItemRevision, the actual operation happens on the object related in
        Teamcenter database. 
        For example, if a configured ItemRevision is cut, and its related Item is in database, the Item is likewise cut
        (from database). Similarly, when a specific ItemRevision is cut and the ItemRevision is in the database, only
        the ItemRevision is cut (from database). For business objects other than ItemRevision, if the object displayed
        is identical to object in database, the object in database is cut.
        
        This operation returns actual objects in database for given list of displayed objects on client.
        """
        return cls.execute_soa_method(
            method_name='getRelatedObjsForConfiguredRevision',
            library='Internal-AWS2',
            service_date='2020_05',
            service_name='DataManagement',
            params={'input': input},
            response_cls=GetRelatedObjectsResponse,
        )


class FullTextSearchService(TcService):

    @classmethod
    def getSearchSettings(cls, searchSettingInput: GetSearchSettingsInput) -> GetSearchSettingsResponse:
        """
        This operation is used to get the search setting values from the server. These search settings are displayed at
        the client side to make search more configurable and convenient for user. Client needs to render these setting
        in user undersandable formate so that users can customize search based on their requirement.
        
        Use cases:
        Search setting has one of the attributes which is used to configure the category names for which the filters
        are expanded by default after every search.
        Right now these values are configured using preference AWC_Limited_Filter_Categories_Expanded this preference
        takes <typename>.<property name> as input. For example, user needs to set value as WorkspaceObject.object_type
        if only object_type filter category needs to be expanded.
        
        When we are giving an option to configure this value from client, we want user to use display names instead of
        internal names of the type and property to make it more user understandable. Display values in this case will
        be fetched by this new service.
        """
        return cls.execute_soa_method(
            method_name='getSearchSettings',
            library='Internal-AWS2',
            service_date='2020_05',
            service_name='FullTextSearch',
            params={'searchSettingInput': searchSettingInput},
            response_cls=GetSearchSettingsResponse,
        )


class UiConfigService(TcService):

    @classmethod
    def loadNamedColumnConfig(cls, uid: str) -> GetNamedColumnConfigsResponse:
        """
        This service operation will load the given named column configuration for a given user.
        
        Use cases:
        Load a Named Column Configuration:
        This service operation will be called which will get the detailed columns information from the selected named
        column configuration.
        """
        return cls.execute_soa_method(
            method_name='loadNamedColumnConfig',
            library='Internal-AWS2',
            service_date='2020_05',
            service_name='UiConfig',
            params={'uid': uid},
            response_cls=GetNamedColumnConfigsResponse,
        )

    @classmethod
    def saveNamedColumnConfig(cls, uid: str, columns: List[ColumnDefInfo], namedColumnConfigCriteria: StringMap) -> ServiceData:
        """
        This service operation saves the named column configuration information to the Teamcenter database. Active
        Workspace client may use this information to populate columns of tables in various sublocations as the user
        navigates.
        
        Use cases:
        Save Named Column Configuration:
        A user wants to modify an existing named column configuration for a given table by adding or removing columns.
        The modified named column configuration will become the active column configuration for that user.
        """
        return cls.execute_soa_method(
            method_name='saveNamedColumnConfig',
            library='Internal-AWS2',
            service_date='2020_05',
            service_name='UiConfig',
            params={'uid': uid, 'columns': columns, 'namedColumnConfigCriteria': namedColumnConfigCriteria},
            response_cls=ServiceData,
        )

    @classmethod
    def createNamedColumnConfig(cls, namedColumnConfigInput: NamedColumnConfigInput, columns: List[ColumnDefInfo], namedColumnConfigCriteria: StringMap) -> ServiceData:
        """
        This service operation creates the named column configuration information in the Teamcenter database. Active
        Workspace client may use this information to populate columns of tables in various sublocations as the user
        navigates. Default named column configurations can be initially created by a utility during install.
        
        Use cases:
        Create Named Column Configuration:
        A user wants to create a named column configuration for a given table when he/she is logged into the client.
        The named column configuration will become the active column configuration for that user on the given table.
        """
        return cls.execute_soa_method(
            method_name='createNamedColumnConfig',
            library='Internal-AWS2',
            service_date='2020_05',
            service_name='UiConfig',
            params={'namedColumnConfigInput': namedColumnConfigInput, 'columns': columns, 'namedColumnConfigCriteria': namedColumnConfigCriteria},
            response_cls=ServiceData,
        )

    @classmethod
    def deleteNamedColumnConfig(cls, uid: str) -> ServiceData:
        """
        This service operation deletes the given named column configuration object from the Teamcenter database.
        
        Use cases:
        Delete Named Column Configuration:
        A user wants to delete an existing named column configuration for a given table. The named column configuration
        will be deleted.
        """
        return cls.execute_soa_method(
            method_name='deleteNamedColumnConfig',
            library='Internal-AWS2',
            service_date='2020_05',
            service_name='UiConfig',
            params={'uid': uid},
            response_cls=ServiceData,
        )

    @classmethod
    def getNamedColumnConfigs(cls, namedColumnConfigInput: NamedColumnConfigInput, namedColumnConfigCriteria: StringMap) -> GetNamedColumnConfigsResponse:
        """
        This service operation gets named column configuration information from the Teamcenter database.
        
        Use cases:
        Get a list of Named Column Configurations:
        This service operation will be called to get all available named column configurations for the logged in user.
        """
        return cls.execute_soa_method(
            method_name='getNamedColumnConfigs',
            library='Internal-AWS2',
            service_date='2020_05',
            service_name='UiConfig',
            params={'namedColumnConfigInput': namedColumnConfigInput, 'namedColumnConfigCriteria': namedColumnConfigCriteria},
            response_cls=GetNamedColumnConfigsResponse,
        )


class FileMgmtService(TcService):

    @classmethod
    def getFileNamesWithTicketInfo(cls, businessObjectsIn: List[BusinessObject]) -> GetFilesAndTicketsInfoResponse:
        """
        This operation fetches the name and the Teamcenter File Management System (FMS) ticket of the file, related to
        the input business objects of type Dataset, as the primary named reference. In case multiple files are related
        to the Dataset as primary named reference , this operation fetches the first file and its corresponding FMS
        ticket.
        
        This operation can be invoked by the Active Workspace client with at least one of the input objects of type
        Dataset, this means Active Workspace client enables the Download command when at least one of the selected
        object is of type Dataset. This operation handles types other than Dataset gracefully and warns the user for
        the invalid selection.
        
        The primary named reference of the Dataset is defined through its definition using the BMIDE tool of
        Teamcenter. This operation finds the primary named reference using the Tool Actions and the Reference
        definitions of the type Dataset. Tool Actions of the type Dataset defines the mapping of the operation on the
        Dataset with the named reference and the Reference definition of the Dataset maps the named reference and the
        extension of the file. Citing an example , if there are multiple files associated with the named reference i.e
        &lsquo;Text&rsquo; , the first file associated with this named reference is selected. In case , the first file
        is deleted , the second file associated with this named reference takes precedence.
        
        Use cases:
        Use Case 1:
        &#61656;    In Active Workspace client, when user selects  Dataset objects and clicks on the "Download" command
        then the client starts downloading the file directly from the FMS with the help of the FMS ticket information.
        
        Use Case 2:
        &#61656;    In Active Workspace client, user selects the Dataset objects and clicks on the "Copy File Download
        Link" command to copy the URL of the file on the Teamcenter and OS clipboards. When the copied file download
        link is hit by the user on a different page then the client starts downloading the file directly from the FMS
        with the help of the FMS ticket information.
        """
        return cls.execute_soa_method(
            method_name='getFileNamesWithTicketInfo',
            library='Internal-AWS2',
            service_date='2020_05',
            service_name='FileMgmt',
            params={'businessObjectsIn': businessObjectsIn},
            response_cls=GetFilesAndTicketsInfoResponse,
        )
