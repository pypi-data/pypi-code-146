from __future__ import annotations

from tcsoa.base import TcService
from tcsoa.gen.Internal.Structure._2020_12.WhereUsed import WhereUsedInput, WhereUsedOutput


class WhereUsedService(TcService):

    @classmethod
    def getWhereUsedInfo(cls, whereUsedInput: WhereUsedInput) -> WhereUsedOutput:
        """
        This operation returns the parent ItemRevision object under which input ItemRevision is created as a child
        component. The parent objects are configured based on input RevisionRule. It also returns column configuration
        information for input ClientScopeURI.
        
        Use Case:
        User wants to perform impact analysis by selecting ItemRevision to know under which parent assemblies
        ItemRevision is created as child component.
        """
        return cls.execute_soa_method(
            method_name='getWhereUsedInfo',
            library='Internal-Structure',
            service_date='2020_12',
            service_name='WhereUsed',
            params={'whereUsedInput': whereUsedInput},
            response_cls=WhereUsedOutput,
        )
