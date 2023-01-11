from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.Core._2007_06.ProjectLevelSecurity import GetFilteredProjectDataInputData
from tcsoa.gen.Internal.Core._2013_05.ProjectLevelSecurity import GetFilteredProjectObjectsResponse
from tcsoa.gen.Internal.Core._2013_05.Licensing import GetLicenseBundlesResponse
from tcsoa.gen.Internal.Core._2013_05.PresentationManagement import GetStylesheetPref, GetSharedCommonClientFilesResponse, StylesheetInputData, GetStylesheetResponse
from typing import List
from tcsoa.gen.Internal.Core._2009_10.Thumbnail import SearchOrders
from tcsoa.base import TcService
from tcsoa.gen.Internal.Core._2013_05.Thumbnail import ThumbnailFileTicketsResponse2


class PresentationManagementService(TcService):

    @classmethod
    def getSharedCommonClientFiles(cls, prefNames: List[str]) -> GetSharedCommonClientFilesResponse:
        """
        This service returns the dataset names, last modified dates, and file tickets to download for Zip datasets as
        defined by the input list of preference names, or if empty input, the HTMLStylesheetSharedLibs preference is
        used.   The preference indicates the list of Zip datasets by dataset name, and there must exist only one
        dataset of that type and name in the system which is owned by a "dba" user.  If this criteria isn't met for a
        dataset defined in the preference, then a partial error is added to the service data.
        
        Use cases:
        1.    The user chooses the summary tab in RichClient.
        2.    Richclient detects that the shared common client files which are required in order to render HTML are not
        downloaded.
        3.    RichClient invokes the getSharedCommonClientFiles operation and downloads the list of file tickets to a
        folder, and caches the dataset names and last modified dates.
        4.    RichClient invokes the getStylesheet operation, receives HTML stylesheet and renders it to the User.
        5.    On a subsequent close/reopen of the Summary View, RichClient reinvokes the getSharedCommonClientFiles
        operation, and receives the list of file tickets, dataset names, and last modified dates.   The RichClient
        downloads any new datasets and any datasets which have a newer timestamp than what was cached.
        6.    Rich client invokes the getStylesheet operation, reccieves new HTML stylesheet output, and renders it to
        the User.
        """
        return cls.execute_soa_method(
            method_name='getSharedCommonClientFiles',
            library='Internal-Core',
            service_date='2013_05',
            service_name='PresentationManagement',
            params={'prefNames': prefNames},
            response_cls=GetSharedCommonClientFilesResponse,
        )

    @classmethod
    def getStylesheet(cls, pref: GetStylesheetPref, inputData: List[StylesheetInputData]) -> GetStylesheetResponse:
        """
        This service converts XRT stylesheets to HTML stylesheets and returns the stylesheet data to the client.   If
        the Teamcenter preference "UsePropertyStylesheetPlatformRenderer" is set to "true", then only XRT is returned
        and no attempt to convert/return HTML is made.    This service accepts a "returnHTMLOnly" preference which
        indicates that the caller can only consume HTML, and overrides the "UsePropertyStylesheetsPlatformRenderer"
        preference, to enable conversion to HTML.  This operation only returns XRT or HTML, never both values to the
        client.
        
        If the XRT to be presented in UI contains objectSet elements, which display an object's children in UI, then
        those children are returned in the output childrenMap container, and those child thumbnail file tickets are
        added to the FileTicketMap, as required.
        
        Common uses for this operation would be to retrieve stylesheet data in either XRT or HTML format for a selected
        object in the UI, in order to present that object to the user.   
        
        Use cases:
        Use case 1:
        1.    The user chooses the summary tab in RichClient.
        2.    The user selects an object in the TCComponent navigator
        3.    The getStylesheet operation is invoked and the resulting stylesheet is presented in the UI.
        
        Use case 2:
        1.    The user selects an object in the TCComponent navigator in the UI.
        2.    The user chooses to view properties for that object.
        3.    The getStylesheet operation is invoked and the resulting stylesheet is presented in the UI.
        """
        return cls.execute_soa_method(
            method_name='getStylesheet',
            library='Internal-Core',
            service_date='2013_05',
            service_name='PresentationManagement',
            params={'pref': pref, 'inputData': inputData},
            response_cls=GetStylesheetResponse,
        )


class ThumbnailService(TcService):

    @classmethod
    def getThumbnailFileTickets2(cls, businessObjects: List[BusinessObject], searchOrders: SearchOrders) -> ThumbnailFileTicketsResponse2:
        """
        Given a list of business objects and relation/dataset type search orders, gets the valid thumbnail file tickets
        for the list of business objects. These file tickets can be used later to download the thumbnail images using
        File Client Cache (FCC). For each business object, it will get a list of valid thumbnail file tickets.
        """
        return cls.execute_soa_method(
            method_name='getThumbnailFileTickets2',
            library='Internal-Core',
            service_date='2013_05',
            service_name='Thumbnail',
            params={'businessObjects': businessObjects, 'searchOrders': searchOrders},
            response_cls=ThumbnailFileTicketsResponse2,
        )


class ProjectLevelSecurityService(TcService):

    @classmethod
    def getFilteredObjectsInProject(cls, input: List[GetFilteredProjectDataInputData]) -> GetFilteredProjectObjectsResponse:
        """
        This operation returns the UIDs that match the requested filter criteria for the requested projects. If no
        objects are found matching a given filter criteria or if project ID is invalid, then project's ID along with
        empty list will be returned.
        """
        return cls.execute_soa_method(
            method_name='getFilteredObjectsInProject',
            library='Internal-Core',
            service_date='2013_05',
            service_name='ProjectLevelSecurity',
            params={'input': input},
            response_cls=GetFilteredProjectObjectsResponse,
        )


class LicensingService(TcService):

    @classmethod
    def getLicenseBundles(cls, licenseServerNames: List[str]) -> GetLicenseBundlesResponse:
        """
        This operation retrieves information about the license bundles from the license file associated with each
        license server specified by the input parameter licenseServerNames. The information for a license bundle
        includes the bundle name, the associated base license feature key, the count of purchased licenses and its
        expiry date. If a license server does not exist with the specified name or if the license server is not online,
        a partial error is returned for that license server.
        """
        return cls.execute_soa_method(
            method_name='getLicenseBundles',
            library='Internal-Core',
            service_date='2013_05',
            service_name='Licensing',
            params={'licenseServerNames': licenseServerNames},
            response_cls=GetLicenseBundlesResponse,
        )
