from __future__ import annotations

from tcsoa.gen.EditContext._2016_04.DataManagement import ChangeContextMap, SetChangeContextResponse
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def setChangeContext(cls, inputs: ChangeContextMap) -> SetChangeContextResponse:
        """
        This operation will configure business objects so that the objects can be edited or inspected in a context
        without changing the public versions of the objects. This operation can also be used to remove the
        configuration of business objects in order to edit or inspect the public versions of the objects.
        This operation does not have any effect on business objects that are not minor revisable and such objects will
        always be returned without being configured.
        The operation can be used to configure multiple sets of objects using different contexts.
        
        Use cases:
        Use Case 1: User wants to edit properties of a set of business objects in a context with the intention to 
        collaborate with other users.
        - User creates a Fnd0EditContext object that abstracts the context within which the edit needs to be performed.
        - The Fnd0EditContext object is provided as input to the operation along with the business objects that need to
        be edited.
        - The configured business objects are returned in the response and can be used for performing edits in the
        context.
        
        
        
        Use Case 2: User wants to edit properties of a set of business objects in a context provided by a ChangeNotice.
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
            method_name='setChangeContext',
            library='EditContext',
            service_date='2016_04',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=SetChangeContextResponse,
        )
