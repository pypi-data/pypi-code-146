from __future__ import annotations

from tcsoa.gen.DocumentManagement._2008_06.DocumentControl import GetCheckinModeAndFilesOutputsResponse, GetAdditionalFilesForCheckinInputs, PostCreateResponse, PostCreateInputs, GetAdditionalFilesForCheckinOutputsResponse
from tcsoa.gen.BusinessObjects import ItemRevision
from typing import List
from tcsoa.base import TcService


class DocumentControlService(TcService):

    @classmethod
    def postCreate(cls, input: List[PostCreateInputs]) -> PostCreateResponse:
        """
        This operation is to be called by the client after the creation of the ItemRevision business object, if there
        are local files to be attached to the newly created ItemRevision. For ItemRevision under Item Revision
        Definition Control (IRDC) it will replace any datasets copied from a template with new datasets for the local
        files. The client will then need to import the local files in the volume based on the return information from
        the SOA.  For ItemRevision not under IRDC control, the commitInfos list field from the return 'PostCreateInfo'
        structure for this ItemRevision will be empty.
        
        Use cases:
        Create new item from the RAC
        During the new item create on RAC, if the ItemRevision business object is under IRDC control,  the Attach Files
        panel will be enabled in the create wizard dialog,  if user choose to attach local files in the Attach Files
        panel, the template files for the IRDC will be replaced for the newly created ItemRevision business object, and
        instead the new datasets will be created for the local files; if user choose not to attach any local files in
        the Attach Files panel, then the template files for the IRDC will be used for the newly created ItemRevision.
        """
        return cls.execute_soa_method(
            method_name='postCreate',
            library='DocumentManagement',
            service_date='2008_06',
            service_name='DocumentControl',
            params={'input': input},
            response_cls=PostCreateResponse,
        )

    @classmethod
    def getAdditionalFilesForCheckin(cls, inputs: List[GetAdditionalFilesForCheckinInputs]) -> GetAdditionalFilesForCheckinOutputsResponse:
        """
        This operation is used in conjunction with the getCheckinModeAndFiles operation during the Check In process.
        getCheckinModeAndFiles takes a list of ItemRevision objects that have been checked out, and returns the list of
        source files that have been downloaded to the client. This operation takes the list of downloaded files
        returned by getCheckinModeAndFiles, and returns the subset of those files that are eligible for Check In.
        
        Use cases:
        Check In
        
        This method is called after the getCheckinModeAndFiles operation, but before the files are checked in.
        """
        return cls.execute_soa_method(
            method_name='getAdditionalFilesForCheckin',
            library='DocumentManagement',
            service_date='2008_06',
            service_name='DocumentControl',
            params={'inputs': inputs},
            response_cls=GetAdditionalFilesForCheckinOutputsResponse,
        )

    @classmethod
    def getCheckinModeAndFiles(cls, inputs: List[ItemRevision]) -> GetCheckinModeAndFilesOutputsResponse:
        """
        Get the CheckIn mode and files for ItemRevision business objects.  This is called before CheckIn to get from
        the server the source files that are currently checked out and downloaded locally and how the system is going
        to search for translated files locally for CheckIn. The information here is going to be used to search
        additional files in the client.  If the ItemRevision business object is under Item Revision Definition
        Configuration (IRDC), the CheckIn mode value is retrieved from the IRDC object; otherwise it will be an empty
        string.
        CheckIn mode is used to check in translated files that are already in the directory with the source file or the
        first level subdirectory. 
        There are three CheckIn modes:
        - Same File Name: Attaches and checks in the derived files only if they have the same name as the source
        dataset.
        - Any File Name: Attaches and checks in the derived files no matter what names they have.
        - None: Does not attach and check in any derived files.
        
        
        Refers to Business Modeler IDE Guide > Creating data model objects to represent objects in Teamcenter > Working
        with document management > Create an Item Revision definition configuration (IRDC) for more information, the
        Checkin mode is defined by Derived Visualization Files to Checkin from the IRDC Checkin Page Info tab.
        
        Use cases:
        Check in ItemRevision under IRDC control
        When a user checks out an ItemRevision business object under IRDC control, the user has the option to download
        the source files into user local machine.  If the user then checks in the ItemRevision, the system will search
        for the translated files in the source file directory according to the specified CheckIn mode. This
        functionality supports client side rendering to provide the derived datasets.
        For example, there is case where some AutoCAD file cannot be converted to a certain format by the server; user
        can find the translated files in the local directory to check in instead.
        """
        return cls.execute_soa_method(
            method_name='getCheckinModeAndFiles',
            library='DocumentManagement',
            service_date='2008_06',
            service_name='DocumentControl',
            params={'inputs': inputs},
            response_cls=GetCheckinModeAndFilesOutputsResponse,
        )
