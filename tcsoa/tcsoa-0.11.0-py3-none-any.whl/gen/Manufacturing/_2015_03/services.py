from __future__ import annotations

from typing import List
from tcsoa.gen.Manufacturing._2015_03.StructureManagement import MoveAndResequenceParameter, MoveAndResequenceResponse
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def moveAndResequenceNodes(cls, inputList: List[MoveAndResequenceParameter]) -> MoveAndResequenceResponse:
        """
        This operation moves and/or re-sequences the nodes in the structure.
        
        Use cases:
        Use Case 1: Re-sequencin g nodes within parent in a structure.
        This operation can be used in M anufacturing Process Planning (MPP) application to resequence a node in a
        struct ure. For example, in a product structure an Item or  BOMLine can be reseqenced within the parent by
        dragging and dropping t he Item in between the siblings. Same could be done in proces s structure by dragging
        and dropping a process or operation BOMLine. As a result of drop, the find number of the node and its
        subsequent sibling are modified.
        Use Case 2: Re-parent and re-sequence of nodes.
        This operation can be used in MPP application to move the nodes from one parent to another and sequenced them
        among the siblings of new parent. For example, in a process structure a process or operation BOMLine objects
        can be dragged and dropped in between the child nodes of another process BOMLine. The dragged processes or
        operations are moved as children of the new process BOMLine and sequenced among the sibling as per dropped
        location. While drag and drop, UI presents an option whether to clone the nodes. If selected then the nodes are
        cloned instead of re-parent.
        Use Case 3: Moving the processes or operations to process resource in Plant Bill of Processes (BOP).
        This operation can be used to allocate the process or operation BOMLine of type Mfg0BvrProcess or
        Mfg0BvrOperation to a process resource of type Mfg0BvrProcessResource in a Plant BOP structure. The find number
        of dropped BOMLine objects could be calculated either in the context of the process station of type
        Mfg0BvrProcessStation to which process resource is a child object, or process resource is itself. If the
        context is process station of type Mfg0BvrProcessStation then the find numbers of the dropped BOMLine objects
        are calculated based on the existing processes or operations that are a child object of process station. If the
        context is process resource then the calculation is based on the processes or operations allocated to that
        process resource. In Teamcenter MPP application, the context is always a process station BOMLine.
        """
        return cls.execute_soa_method(
            method_name='moveAndResequenceNodes',
            library='Manufacturing',
            service_date='2015_03',
            service_name='StructureManagement',
            params={'inputList': inputList},
            response_cls=MoveAndResequenceResponse,
        )
