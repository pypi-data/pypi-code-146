from __future__ import annotations

from tcsoa.gen.Internal.DebugMonitor._2014_06.JournalBasedTesting import PropertyData, InitializeJBTResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class JournalBasedTestingService(TcService):

    @classmethod
    def initializeJBT(cls) -> InitializeJBTResponse:
        """
        This operation sets up the system environment and returns the site database information before Journal Based
        Testing is used. It will be called right after the login SOA, during both recording and replay phases. It will
        set the system environment variable TC_JBT=on if it has not been set, and clear all preferences whose values
        are UIDs (e.g., HistoryIDList and MRU related preferences). The operation returns the last six characters of an
        UID which uniquely identifies the site database that the client is connecting to. This operation is only used
        by JBT.
        """
        return cls.execute_soa_method(
            method_name='initializeJBT',
            library='Internal-DebugMonitor',
            service_date='2014_06',
            service_name='JournalBasedTesting',
            params={},
            response_cls=InitializeJBTResponse,
        )

    @classmethod
    def validatePropertyValues(cls, expectedPropertyValues: List[PropertyData], userEnteredErrorMessage: str) -> ServiceData:
        """
        This operation compares the property values of a list of objects against their expected values and reports an
        exception when a mismatch is found.
        
        Use cases:
        In the context of Journal Based Testing, this operation is called during the recording when the user clicks the
        OK button on the Validate Property Values dialog or when the Validate Structure Hierarchy menu is clicked. It
        compares the expected values against the actual values of the properties on the input objects. If there is any
        difference between the expected value and actual value, the validation fails and the operation throws an
        exception.
        
        Exceptions:
        >The operation will throw an exception when it finds the first property whose expected value does not match the
        actual value.
        
        214652 (error) Parameterized error message, e.g., the property item_id for object TopItem contains an expected
        value of 000258, but its actual value is 000528.
        """
        return cls.execute_soa_method(
            method_name='validatePropertyValues',
            library='Internal-DebugMonitor',
            service_date='2014_06',
            service_name='JournalBasedTesting',
            params={'expectedPropertyValues': expectedPropertyValues, 'userEnteredErrorMessage': userEnteredErrorMessage},
            response_cls=ServiceData,
        )
