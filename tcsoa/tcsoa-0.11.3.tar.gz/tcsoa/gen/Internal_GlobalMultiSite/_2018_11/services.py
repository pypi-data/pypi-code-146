from __future__ import annotations

from tcsoa.gen.Internal.GlobalMultiSite._2018_11.Briefcase import NamesAndValues, CheckBriefcaseLicenseResponse, GetBriefcaePreviewDataResponse
from typing import List
from tcsoa.base import TcService


class BriefcaseService(TcService):

    @classmethod
    def checkBriefcaseLicense(cls) -> CheckBriefcaseLicenseResponse:
        """
        Operation checks if the current site has licenses, "multisite_server" and "tc_briefcase" for all briefcase
        add-on features such as "preview briefcase", "compare briefcases", "diverse schema".
        
        Use cases:
        Briefcase add on license is required for below user actions-
        - A user chooses a briefcase file in Teamcenter and wants to open it for Meta-data preview.
        - A user chooses two briefcase files in Teamcenter and wants to preview and compare them.
        - A user chooses to Import/Export data to managed briefcase in Teamcenter and transformer is used for this
        Import/Export.
        
        """
        return cls.execute_soa_method(
            method_name='checkBriefcaseLicense',
            library='Internal-GlobalMultiSite',
            service_date='2018_11',
            service_name='Briefcase',
            params={},
            response_cls=CheckBriefcaseLicenseResponse,
        )

    @classmethod
    def getBriefcasePreviewData(cls, oldBriefcaseFMSTicket: str, oldBriefcaseUID: str, newBriefcaseFMSTicket: str, newBriefcaseUID: str, optionNamesAndValues: List[NamesAndValues]) -> GetBriefcaePreviewDataResponse:
        """
        This operation is used to provide the structures in briefcases for preview and compare purpose. A briefcase may
        contain a structure in Teamcenter XML format. This operation parses the Teamcenter XML files the input
        briefcases, get the structure information and convert them to the data which can be used for preview and
        compare on the client side.
        
        Use cases:
        &bull;    A user chooses a briefcase file in Teamcenter and wants to open it for preview. The selected
        briefcase UID is sent to this operation. The operation parses it to get the data structure and returns it to
        the client side.
        &bull;    A user opens a briefcase file at the client side for preview. The briefcase file at the client side
        should be uploaded to the server before calling this operation. The FMS ticket of the uploaded file should be
        sent to this operation. The operation parses the briefcase to get the data structure and returns it to the
        client side. 
        &bull;    A user chooses two briefcase files in Teamcenter and wants to preview and compare them. The selected
        briefcase UIDs are sent to this operation. The operation parses the briefcases to get their data structure and
        returns them to the client side. The operation can also provide the delta data for the difference between these
        two briefcase files.
        &bull;    A user opens two briefcase files at client side and wants to preview and compare. The files at the
        client side should be uploaded to the server before calling this operation. The FMS tickets of the uploaded
        files should be sent to this operation. The operation parses the briefcase files to get their data structures
        and returns them to the client side. The operation can also provide the delta data for the difference between
        these two briefcase files.
        """
        return cls.execute_soa_method(
            method_name='getBriefcasePreviewData',
            library='Internal-GlobalMultiSite',
            service_date='2018_11',
            service_name='Briefcase',
            params={'oldBriefcaseFMSTicket': oldBriefcaseFMSTicket, 'oldBriefcaseUID': oldBriefcaseUID, 'newBriefcaseFMSTicket': newBriefcaseFMSTicket, 'newBriefcaseUID': newBriefcaseUID, 'optionNamesAndValues': optionNamesAndValues},
            response_cls=GetBriefcaePreviewDataResponse,
        )
