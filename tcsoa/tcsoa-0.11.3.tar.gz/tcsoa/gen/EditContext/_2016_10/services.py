from __future__ import annotations

from tcsoa.gen.EditContext._2016_10.DataManagement import SetChangeContextResponse2, ChangeContextMapIn
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def setChangeContext2(cls, inputs: ChangeContextMapIn) -> SetChangeContextResponse2:
        """
        This operation  configures business objects to allow the objects to be edited, queried or deleted in a context
        without changing the public versions of the objects. This operation can also configure business objects with no
        context in order to edit, query or delete the public versions of the objects.
        This operation does not have any effect on business objects that are not minor revisable and such objects will
        always be returned without being configured.
        The operation can be used to configure multiple sets of objects using different contexts. 
        
        Use Case:
        Use Case 1: User wants to edit the properties of a set of business objects in an isolated context with the
        intention to share the proposed changes with other users.
        
        - User creates a Fnd0MarkupSpace object that abstracts the context within which the edit needs to be performed.
        - The Fnd0MarkupSpace object is provided as input to the operation along with the business objects that need to
        be edited.
        - The configured business objects are returned in the response and can be used for performing edits in the
        context.
        
        
        
        Use Case 2: User wants to query the properties of a set of business objects in an isolated context that have
        been edited in the context of a ChangeNotice.
        
        - User creates a ChangeNotice object that abstracts the context within which the edit needs to be performed.
        - The ChangeNotice object is provided as input to the operation along with the business objects that need to be
        configured.
        - The configured business objects are returned in the response and can be used for performing edits in the
        context.
        
        
        
        
        Use Case 3: User wants to query a property belonging to the public version of a business object that is
        currently configured for editing in a collaborative space.
        
        - User passes a null value for the context along with the business object that needs to be inspected in public.
        - The unconfigured business objects are returned in the response and any queries performed on the objects will
        return public data.
        
        """
        return cls.execute_soa_method(
            method_name='setChangeContext2',
            library='EditContext',
            service_date='2016_10',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=SetChangeContextResponse2,
        )
