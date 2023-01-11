from __future__ import annotations

from typing import List
from tcsoa.gen.Internal.Cad._2010_04.DataManagement import ReviseResponse, SaveAsNewItemResponse, SaveAsNewItemInfo, ReviseInfo
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def revise(cls, info: List[ReviseInfo]) -> ReviseResponse:
        """
        Revises all the ItemRevision  objects given in the input vector and propagation of their relations via deep
        copy input. The client has the option to supply a set of deep copy rules. Default deep copy rules reside in the
        system. The client may retrieve them using the 'getDeepCopyInfo'  operation and change or add to the list for
        input to this operation as desired. If the client does not supply any deep copy rules then the default ones
        will be used. If the client supplies deep copy rules, then none of the default rules will be used. If the
        client provides new property values for the master form in the input then these will be applied to the newly
        created ItemRevision objects master form.
        
        Use cases:
        User has an iitem revision that is moving from the design phase to the production phase. The final design needs
        to be maintained unaltered so a new revision of the item revision is made that can be updated per production.
        When revising the item revision, the client can also specify deep copy behavior to determine what is done with
        attached objects (such as datasets and forms  ). The client can reference the original objects, make new copies
        of the objects, or not have a reference at all.  The client can also specify new attributes for the attached
        object.
        """
        return cls.execute_soa_method(
            method_name='revise',
            library='Internal-Cad',
            service_date='2010_04',
            service_name='DataManagement',
            params={'info': info},
            response_cls=ReviseResponse,
        )

    @classmethod
    def saveAsNewItem(cls, info: List[SaveAsNewItemInfo]) -> SaveAsNewItemResponse:
        """
        This service will create a new item that is based on the original input item.  The client has the option to
        supply a set of deep copy rules.  Default deep copy rules reside in the system, the client may retrieve them
        using 'getDeepCopyInfo' operation and change or add to the list for input to this operation as desired. If the
        client does not supply any deep copy rules then the default ones will be used. If the client supplies deep copy
        rules, then none of the default rules will be used. If the client provides new property values for the master
        form in the input then these will be applied to the newly created item and  item revision master forms.
        
        Use cases:
        The client has an existing item that they want to preserve yet continue making improvements. The client can
        specify a new item type when doing the save and save the new item as a different item type than the original.
        The client can also specify deep copy behavior to determine what is done with attached objects (such as
        datasets and forms ). The client can reference the original objects, make new copies of the objects or not have
        a reference at all.  The client can also specify new attributes for the attached forms.
        """
        return cls.execute_soa_method(
            method_name='saveAsNewItem',
            library='Internal-Cad',
            service_date='2010_04',
            service_name='DataManagement',
            params={'info': info},
            response_cls=SaveAsNewItemResponse,
        )
