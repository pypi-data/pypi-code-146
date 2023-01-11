from __future__ import annotations

from tcsoa.gen.Internal.Core._2020_04.LogicalObject import AddMemAndPresentedPropsWriteInput
from tcsoa.gen.Internal.Core._2017_11.LogicalObject import AddMemberAndPresentedPropsResponse
from tcsoa.base import TcService


class LogicalObjectService(TcService):

    @classmethod
    def addMemAndPresentedPropsWithWrite(cls, addMembersAndPresentedProps: AddMemAndPresentedPropsWriteInput) -> AddMemberAndPresentedPropsResponse:
        """
        This operation adds a list of members and presented properties to an existing Logical Object Type based on the
        specified input with support to update the source property.  Presented properties are part of Logical Object
        Type which also composed d of root, and member objects and presented properties.  Logical Objects are used to
        represent logical views of complex data models in terms of a simplified structure of members and properties.
        
        This operation also adds presented properties from an existing Logical Object Type to the related Attribute
        Exchange Configuration object.
        
        Use cases:
        Use Case 1: 
        This operation is invoked to add members and presented properties to an existing Logical Object Type.
        
        Use Case 2: 
        This operation also adds presented properties from an existing Logical Object Type to the related Attribute
        Exchange Configuration object.
        """
        return cls.execute_soa_method(
            method_name='addMemAndPresentedPropsWithWrite',
            library='Internal-Core',
            service_date='2020_04',
            service_name='LogicalObject',
            params={'addMembersAndPresentedProps': addMembersAndPresentedProps},
            response_cls=AddMemberAndPresentedPropsResponse,
        )
