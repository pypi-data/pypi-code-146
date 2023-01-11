from __future__ import annotations

from tcsoa.gen.Ai._2012_09.Ai import FindRequestsResponse
from tcsoa.gen.Ai._2013_12.Ai import FindRequestsWithDependencyFilter
from tcsoa.base import TcService


class AiService(TcService):

    @classmethod
    def findRequestsWithDependencies(cls, filter: FindRequestsWithDependencyFilter) -> FindRequestsResponse:
        """
        This operation is based on dependency between the related  RequestObjects and on the input criteria provided to
        the operation input. The operation will return a list of RequestObjects to process. The returned RequestObjects
        are those whose property "type" is of value "Sync" and property "state" is of value "Pending". Further, this
        operation returns only those RequestObjects which are dependent on RequestObjects whose state is "Completed". 
        Dependency of RequestObject is determined by "fnd0pred_list" property. This property points to its preceding
        Request Object.
        """
        return cls.execute_soa_method(
            method_name='findRequestsWithDependencies',
            library='Ai',
            service_date='2013_12',
            service_name='Ai',
            params={'filter': filter},
            response_cls=FindRequestsResponse,
        )
