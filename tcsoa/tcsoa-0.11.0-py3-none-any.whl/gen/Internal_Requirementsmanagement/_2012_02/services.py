from __future__ import annotations

from typing import List
from tcsoa.base import TcService
from tcsoa.gen.Internal.Requirementsmanagement._2012_02.RequirementsManagement import TraceabilityMatrixInfo, TraceabilityMatrixResponse


class RequirementsManagementService(TcService):

    @classmethod
    def getTraceabilityMatrix(cls, inputs: List[TraceabilityMatrixInfo]) -> TraceabilityMatrixResponse:
        """
        This operation creates the traceability matrix between two BOM structures based on TraceLink  relation. A
        matrix will be generated that shows the source structure objects as rows in the matrix and columns as target
        structure. In the trace matrix if there is a link between row (object from the source structure) and the column
        (object from the target structure) then link count will be shown in the respective cell.  This operation can be
        performed between two different BOM structures or same structure. In this operation all children for selected
        source and target object will be loaded as rows and columns in the matrix and each cell defines the link
        between source row object and target column object. This matrix will show the results for TraceLink which are
        created from source object (object shown as rows) to target object( object shown as columns) and not include
        the link which created from object shown as column to object shown as rows.
        
        Use cases:
        You can create traceability matrix between source and target structure based on TraceLink relation. Source and
        target can be different structure or same structure.
        """
        return cls.execute_soa_method(
            method_name='getTraceabilityMatrix',
            library='Internal-Requirementsmanagement',
            service_date='2012_02',
            service_name='RequirementsManagement',
            params={'inputs': inputs},
            response_cls=TraceabilityMatrixResponse,
        )
