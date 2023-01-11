from __future__ import annotations

from tcsoa.gen.Internal.Core._2017_05.FileManagement import DatashareManagerReplaceInfo
from tcsoa.gen.Internal.Core._2014_10.FileManagement import GetPlmdFileTicketResponse
from tcsoa.gen.Internal.Core._2017_05.PresentationManagement import StylesheetPerPageInputData, GetStylesheetPerPageResponse, GetStylesheetPerPagePref
from typing import List
from tcsoa.base import TcService


class PresentationManagementService(TcService):

    @classmethod
    def getStylesheetPerPage(cls, pref: GetStylesheetPerPagePref, inputData: List[StylesheetPerPageInputData]) -> GetStylesheetPerPageResponse:
        """
        This operation gets the stylesheet data and list of names of the available visible pages for the input object.
        The stylesheet data will be returned only for the target page which is defined in the input structure. If
        target page is not specified, then it will return stylesheet data for first visible page. This helps to improve
        client performance by querying only for the information that will be displayed.
        The clients are expected to call the operation without a target page specified. And then, if the user selects a
        page to display, then make another call to the operation with the selected page name as the target page in the
        input. 
        
        If pref.processEntireXRT = true, this operation will process the data for the entire XRT stylesheet.  If false,
        this operation will only process the target page which is defined in the input structure.
        
        This operation also converts XRT stylesheets to HTML stylesheets and returns the stylesheet data to the client.
        If the Teamcenter preference "UsePropertyStylesheetPlatformRenderer" is set to "true", then only XRT is
        returned and no attempt to convert to/return HTML is made. This service accepts a "returnHTMLOnly" preference
        which indicates that the caller can only consume HTML, and overrides the
        "UsePropertyStylesheetsPlatformRenderer" preference, to enable conversion to HTML. This operation only returns
        XRT or HTML, never both values to the client.
        
        If the XRT to be presented in the UI contains objectSet elements, which display an object's children in the UI,
        then those children are returned in the output childrenMap container, and their thumbnail file tickets are
        added to the FileTicketMap, as required.
        
        Common uses for this operation would be to retrieve stylesheet data in either XRT or HTML format for a selected
        object in the UI, in order to present that object to the user.
        
        Use cases:
        Use case 1:
        1.    The user chooses the summary tab in the RichClient.
        2.    The user selects an object in the Navigator pane in RichClient.
        3.    The getStylesheetPerPage operation is invoked and the resulting stylesheet is presented in the UI.
        
        Use case 2:
        1. The user selects an object in the Navigator pane in RichClient.
        2.    The user chooses to view properties for that object.
        3.    The getStylesheetPerPage operation is invoked and the resulting stylesheet is presented in the UI.
        
        Use case 3:
        1. The user chooses the summary tab in the RichClient.
        2.    The user selects an object in the Navigator pane in the RichClient.
        3.    The getStylesheetPerPage operation is invoked and the resulting stylesheet is presented in the UI.
                3.1. The operation also returns the list of names of the visible pages, for example
                       "tc_xrt_Overview", "tc_xrt_AttachedFiles", "tc_xrt_RelatedLinks", "tc_xrt_AuditLogs" etc.
        4.    The use clicks on the "Audit Logs" page in the summary tab. The getStylesheetPerPage operation           
             
                is invoked, with the target page set to "Audit Logs".
        5.    The getStylesheetPerPage operation returns the stylesheet data for the audit log page and it is presented
        in the UI.
        """
        return cls.execute_soa_method(
            method_name='getStylesheetPerPage',
            library='Internal-Core',
            service_date='2017_05',
            service_name='PresentationManagement',
            params={'pref': pref, 'inputData': inputData},
            response_cls=GetStylesheetPerPageResponse,
        )


class FileManagementService(TcService):

    @classmethod
    def getPlmdFileTicketForReplace(cls, infos: List[DatashareManagerReplaceInfo]) -> GetPlmdFileTicketResponse:
        """
        This operation generates a File Management System (FMS) transient read ticket for Product Lifecycle Management
        Data (PLMD) file.
        The PLMD file is used by Datashare Manager Application to asynchronously replace one or more PLM files with
        files from a local client environment, which are uploaded into the Teamcenter volume. The PLMD file details
        like FMS Bootstrap URLs, dataset names, type, reference names, original file names, and absolute file paths and
        write tickets.
        
        Use cases:
        Active Workspace client initiates an asynchrouous file replace.
        """
        return cls.execute_soa_method(
            method_name='getPlmdFileTicketForReplace',
            library='Internal-Core',
            service_date='2017_05',
            service_name='FileManagement',
            params={'infos': infos},
            response_cls=GetPlmdFileTicketResponse,
        )
