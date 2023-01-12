from __future__ import annotations

from typing import List
from tcsoa.gen.Internal.Requirementsmanagement._2012_10.RequirementsManagement import MatchLineInputData, MatchedLineResponse, TraceabilityMatrixInfo1
from tcsoa.base import TcService
from tcsoa.gen.Internal.Requirementsmanagement._2012_02.RequirementsManagement import TraceabilityMatrixResponse


class RequirementsManagementService(TcService):

    @classmethod
    def getTraceabilityMatrix(cls, inputs: List[TraceabilityMatrixInfo1]) -> TraceabilityMatrixResponse:
        """
        This operation creates the traceability matrix between two BOM structures based on TraceLink relation by
        applying filter of selected trace link types. A matrix will be created according to the given TraceLink types
        instead of getting all TraceLink type relations. A matrix will be generated that shows the source structure
        objects as rows in the matrix and columns as target structure. In the trace matrix if there is a link between
        row (object from the source structure) and the column (object from the target structure) then link count will
        be shown in the respective cell for the TraceLink objects which are included in the filter types array. If
        filter is not applied then it will get the count of TraceLink objects. This operation can be performed between
        two different BOM structures or same structure. In this operation all children for selected source and target
        object will be loaded as rows and columns in the matrix and each cell defines the link between source row
        object and target column object. This matrix will show the results for TraceLink instances which are created
        from source object (object shown as rows) to target object (object shown as columns) and not vice versa.
        """
        return cls.execute_soa_method(
            method_name='getTraceabilityMatrix',
            library='Internal-Requirementsmanagement',
            service_date='2012_10',
            service_name='RequirementsManagement',
            params={'inputs': inputs},
            response_cls=TraceabilityMatrixResponse,
        )

    @classmethod
    def getMatchingLines(cls, inputs: List[MatchLineInputData]) -> MatchedLineResponse:
        """
        This operation searches for matching BOMLine instance(s) or GDELine instance(s) for a given ItemRevision in the
        given BOMWindow instances. For given ItemRevision, operation searches the matching BOMLine or GDELine in each
        BOM tree table, and returns matching BOMLine instances.
        """
        return cls.execute_soa_method(
            method_name='getMatchingLines',
            library='Internal-Requirementsmanagement',
            service_date='2012_10',
            service_name='RequirementsManagement',
            params={'inputs': inputs},
            response_cls=MatchedLineResponse,
        )
