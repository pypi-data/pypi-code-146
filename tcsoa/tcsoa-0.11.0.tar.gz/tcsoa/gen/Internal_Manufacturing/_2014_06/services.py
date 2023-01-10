from __future__ import annotations

from tcsoa.gen.Internal.Manufacturing._2014_06.DataManagement import AutomaticMFGFeaturesAssignmentInputInfo, AutomaticMFGFeaturesAssignmentResponse
from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.Manufacturing._2014_06.IPAManagement import GetDynamicIPALinesResponse, CleanDynamicIPALinesInfo
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class IPAManagementService(TcService):

    @classmethod
    def cleanDynamicIPALines(cls, input: CleanDynamicIPALinesInfo) -> ServiceData:
        """
        The operation clears the dynamic IPA lines generated using SOA getDynamicIPALines for the input BOP lines.
        """
        return cls.execute_soa_method(
            method_name='cleanDynamicIPALines',
            library='Internal-Manufacturing',
            service_date='2014_06',
            service_name='IPAManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def getDynamicIPALines(cls, inputBOPLines: List[BusinessObject]) -> GetDynamicIPALinesResponse:
        """
        This operation searches predecessors of the input BOP lines (i.e. one or more processes) in the process
        structure and returns aggregation of all incoming parts to these BOP lines. 
        The IPAs can be generated on the fly; for one or more processes in a process structure where the items are
        consumed from product structure.  The operation considers occurrence types defined in
        'MEDynamicIPAOccurrenceTypes' preference; to determine which occurrence types to aggregate from predecessors in
        the given process structure to generate the IPA. The default value for this preference will be 'MEConsumed'. 
        The dynamic IPA (DIPA) nodes created under the process will be added as 'MEDynamicWorkpiece' occurrence type.
        Map of input bop lines and their corresponding DIPA nodes will be returned.
        """
        return cls.execute_soa_method(
            method_name='getDynamicIPALines',
            library='Internal-Manufacturing',
            service_date='2014_06',
            service_name='IPAManagement',
            params={'inputBOPLines': inputBOPLines},
            response_cls=GetDynamicIPALinesResponse,
        )


class DataManagementService(TcService):

    @classmethod
    def automaticMFGFeaturesAssignment(cls, input: AutomaticMFGFeaturesAssignmentInputInfo) -> AutomaticMFGFeaturesAssignmentResponse:
        """
        This operation automatically assigns the manufacturing feature (ArcWeld, WeldPoint) objects from the source
        structure to the given target structure.
        """
        return cls.execute_soa_method(
            method_name='automaticMFGFeaturesAssignment',
            library='Internal-Manufacturing',
            service_date='2014_06',
            service_name='DataManagement',
            params={'input': input},
            response_cls=AutomaticMFGFeaturesAssignmentResponse,
        )
