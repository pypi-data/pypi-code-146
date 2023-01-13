"""DP-FedAvg contractor.

Reference: https://arxiv.org/abs/1710.06963
"""


import secrets
from abc import ABC
from dataclasses import dataclass

from .contractor import (AutoFedAvgContractor, CheckinEvent, FedAvgContractor,
                         FedAvgEventFactory)


@dataclass
class DPCheckinEvent(CheckinEvent):
    """An event of checkin for a specific task."""

    TYPE = 'dp_check_in'

    n_k: int

    @classmethod
    def contract_to_event(cls, contract: dict) -> 'DPCheckinEvent':
        event_type = contract.get('type')
        peer_id = contract.get('peer_id')
        nonce = contract.get('nonce')
        n_k = contract.get('n_k')
        assert event_type == cls.TYPE, f'合约类型错误: {event_type}'
        assert peer_id and isinstance(peer_id, str), f'invalid peer_id: {peer_id}'
        assert nonce or isinstance(nonce, str), f'invalid nonce: {nonce}'
        assert n_k and isinstance(n_k, int) and n_k > 0, f'invalid n_k: {n_k}'
        return DPCheckinEvent(peer_id=peer_id, nonce=nonce, n_k=n_k)


class DPFedAvgEventFactory(FedAvgEventFactory):
    _CLASS_MAP = {
        DPCheckinEvent.TYPE: DPCheckinEvent,
        **FedAvgEventFactory._CLASS_MAP
    }


class DPFedAvgContractorMixin(ABC):

    def checkin(self, peer_id: str, n_k: int) -> str:
        """Checkin to the task.

        :return
            A nonce string used for identifying matched sync_state reply.
        """
        nonce = secrets.token_hex(16)
        event = DPCheckinEvent(peer_id=peer_id, nonce=nonce, n_k=n_k)
        self._new_contract(targets=self.EVERYONE, event=event)
        return nonce


class DPFedAvgContractor(DPFedAvgContractorMixin, FedAvgContractor):

    def __init__(self, task_id: str):
        super().__init__(task_id=task_id)
        self._event_factory = DPFedAvgEventFactory


class AutoDPFedAvgContractor(AutoFedAvgContractor, DPFedAvgContractorMixin):

    def __init__(self, task_id: str):
        super().__init__(task_id=task_id)
        self._event_factory = DPFedAvgEventFactory
