from __future__ import annotations

from tcsoa.gen.AWS2._2018_12.RequirementsManagement import CreateTracelinksResponse, CreateTracelinksInputData
from typing import List
from tcsoa.base import TcService


class RequirementsManagementService(TcService):

    @classmethod
    def createTracelinks(cls, input: List[CreateTracelinksInputData]) -> CreateTracelinksResponse:
        """
        This operation creates a FND_TraceLink object between the primary and secondary business objects.
        
        Use cases:
        In ACE perspective, user select an Awb0Element element and clicks on the "Create TraceLink" button. The
        selected element will be in the Create Trace Link panel start section, user chooses another Awb0Element element
        in the Create Trace Link panel end section. 
        
        - If createTracelinkWithOccurrences mode is true, the trace link between the Occurrences will be created. 
        - If createDefiningTracelinkWithOccurrence is true, then the trace link between the defining Occurrence and the
        complying underlying workspace object will be created.
        - If createComplyingTracelinkWithOccurrence is true, then the trace link between the defining underlying
        workspace object and the complying Occurrence will be created.
        
        """
        return cls.execute_soa_method(
            method_name='createTracelinks',
            library='AWS2',
            service_date='2018_12',
            service_name='RequirementsManagement',
            params={'input': input},
            response_cls=CreateTracelinksResponse,
        )
