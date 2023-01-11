from __future__ import annotations

from tcsoa.gen.Administration._2012_10.IRM import GetSessionValuesResponse, AMImpactedObjectsResponse
from tcsoa.base import TcService


class IRMService(TcService):

    @classmethod
    def getSessionValues(cls) -> GetSessionValuesResponse:
        """
        This operation gets all the session information in the form of key values map.  Each key corresponds to
        particular session attribute like user, roles, groups, project teams, and licenses.  For each entry in the keys
        array, the corresponding entry in the values array contains the values for that specific session attribute.
        Session information returned from this SOA operation is used during read expression evaluation in external
        clients to determine the READ privilege to the current logged in user on the indexed Teamcenter data.
        """
        return cls.execute_soa_method(
            method_name='getSessionValues',
            library='Administration',
            service_date='2012_10',
            service_name='IRM',
            params={},
            response_cls=GetSessionValuesResponse,
        )

    @classmethod
    def getAMImpactedObjects(cls, filterByIndexedStatus: bool) -> AMImpactedObjectsResponse:
        """
        This operation lists the business objects whose read access is impacted by the changes in Access Manager (AM)
        rule tree. The rule tree changes considered are limited to those made after the previous call to this operation.
        This operation is usually called periodically and the objects whose read access privilege is modified due to
        the changes to AM rule tree between the previous call and the current one are determined and returned.
        Optionally, this operation returns the set of objects which is the intersection of objects impacted by AM rule
        changes and objects previously indexed. Previously indexed objects are stored in ACCT_TABLE table.
        AM rule configuration changes need re-login to refresh the in memory rule registry cache. Hence, until re-login
        after the AM rule changes, this operation will return ZERO objects.
        """
        return cls.execute_soa_method(
            method_name='getAMImpactedObjects',
            library='Administration',
            service_date='2012_10',
            service_name='IRM',
            params={'filterByIndexedStatus': filterByIndexedStatus},
            response_cls=AMImpactedObjectsResponse,
        )
