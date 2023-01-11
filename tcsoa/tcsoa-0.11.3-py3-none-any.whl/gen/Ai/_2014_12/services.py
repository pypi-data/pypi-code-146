from __future__ import annotations

from tcsoa.gen.Ai._2014_12.Ai import GetMappedAppRefsResponse, GetMappedAppRefsInput, CreateAppInterfaceRecordInput, CreateAppInterfaceRecordsResponse
from typing import List
from tcsoa.base import TcService


class AiService(TcService):

    @classmethod
    def createApplicationInterfaceRecords(cls, input: List[CreateAppInterfaceRecordInput]) -> CreateAppInterfaceRecordsResponse:
        """
        This operation creates RecordObjects for the specified labels in the MasterRecord associated with the input
        AppInterface object. Input labels are PLMXML style label strings of ApplicationRef element related to
        Application type "Teamcenter". 
        
        Use cases:
        Use Case 1: Creating RecordObjects for specified PLMXML labels.
        This operation should be used to create RecordObjects for  Teamcenter Application References which were not
        exported via PLMXML. Typical case would be Light Weight BOM APIs are used to get the data, but, later there is
        a need to do a PLMXML import using AppInterface object.
        
        """
        return cls.execute_soa_method(
            method_name='createApplicationInterfaceRecords',
            library='Ai',
            service_date='2014_12',
            service_name='Ai',
            params={'input': input},
            response_cls=CreateAppInterfaceRecordsResponse,
        )

    @classmethod
    def getMappedApplicationRefs(cls, appRefs: List[GetMappedAppRefsInput]) -> GetMappedAppRefsResponse:
        """
        This operation searches for objects with specified Application References and returns the matching Application
        References with specified Application names. Application Reference is a 3-tuple construct with name, label and
        version strings. This is used in PLMXML exchange between Teamcenter and target applications to uniquely
        identity Teamcenter entities like Item, ItemRevision, Form objects etc.
        
        Use cases:
        Use Case 1: Getting Teamcenter Application References for non Teamcenter Application References.
        This operation can be used to fetch the Application References of Teamcenter given non Teamcenter Application
        References. These are typically used in PLMXML interchange.
        Use Case 2: Getting non Teamcenter Application References for Teamcenter Application References.
        This operation can be used to fetch the Application References of non Teamcenter  Application References given
        Teamcenter Application References. These are typically used in PLMXML interchange.
        """
        return cls.execute_soa_method(
            method_name='getMappedApplicationRefs',
            library='Ai',
            service_date='2014_12',
            service_name='Ai',
            params={'appRefs': appRefs},
            response_cls=GetMappedAppRefsResponse,
        )
