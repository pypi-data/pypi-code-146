"""Secure Aggregation FedAvg contractor.

Reference: https://eprint.iacr.org/2017/281.pdf
"""


import base64
from abc import ABC, ABCMeta
from dataclasses import dataclass
from typing import List, Tuple

from ..contractor import ContractEvent
from .contractor import (AutoFedAvgContractor, FedAvgContractor,
                         FedAvgEventFactory)


@dataclass
class AdvertiseKeysEvent(ContractEvent):
    """An event of noticing calculators to advertise keys."""

    TYPE = 'advertise_keys'

    round: int
    calculators: List[str]

    @classmethod
    def contract_to_event(cls, contract: dict) -> 'AdvertiseKeysEvent':
        event_type = contract.get('type')
        round = contract.get('round')
        calculators = contract.get('calculators')
        assert event_type == cls.TYPE, f'合约类型错误: {event_type}'
        assert isinstance(round, int) and round > 0, f'invalid round: {round}'
        assert (
            calculators and isinstance(calculators, list)
            and all(_peer_id and isinstance(_peer_id, str) for _peer_id in calculators)
        ), f'invalid participants: {calculators}'
        return AdvertiseKeysEvent(round=round, calculators=calculators)


@dataclass
class AdvertiseKeysResponseEvent(ContractEvent):
    """An event of responding of advertise keys."""

    TYPE = 'advertise_keys_response'

    round: int
    peer_id: str
    c_pk: bytes
    s_pk: bytes

    @classmethod
    def contract_to_event(cls, contract: dict) -> 'AdvertiseKeysResponseEvent':
        event_type = contract.get('type')
        round = contract.get('round')
        peer_id = contract.get('peer_id')
        base64_c_pk = contract.get('c_pk')
        base64_s_pk = contract.get('s_pk')
        assert event_type == cls.TYPE, f'合约类型错误: {event_type}'
        assert isinstance(round, int) and round > 0, f'invalid round: {round}'
        assert peer_id and isinstance(peer_id, str), f'invalid peer_id: {peer_id}'
        assert base64_c_pk and isinstance(base64_c_pk, str), f'invalid c_pk: {base64_c_pk}'
        assert base64_s_pk and isinstance(base64_s_pk, str), f'invalid s_pk: {base64_s_pk}'
        c_pk = base64.b64decode(base64_c_pk.encode())
        s_pk = base64.b64decode(base64_s_pk.encode())
        return AdvertiseKeysResponseEvent(round=round, peer_id=peer_id, c_pk=c_pk, s_pk=s_pk)


@dataclass
class ListDataInRoundEvent(ContractEvent, metaclass=ABCMeta):
    """An abstract base of an event to exchange a list of string data in a round."""

    round: int
    list_data: List[str]

    @classmethod
    def _decode_contract(cls, contract: dict) -> Tuple[int, List[str]]:
        event_type = contract.get('type')
        round = contract.get('round')
        list_data = contract.get('list_data')
        assert event_type == cls.TYPE, f'合约类型错误: {event_type}'
        assert isinstance(round, int) and round > 0, f'invalid round: {round}'
        assert (
            isinstance(list_data, list)
            and all(_item and isinstance(_item, str) for _item in list_data)
        ), f'invalid list_data: {list_data}'
        return round, list_data


@dataclass
class DistributeUser1ListEvent(ListDataInRoundEvent):
    """An event of distributing the data of user_1 list to calculators."""

    TYPE = 'distribute_user_1_list'

    @classmethod
    def contract_to_event(cls, contract: dict) -> 'DistributeUser1ListEvent':
        round, list_data = cls._decode_contract(contract=contract)
        return DistributeUser1ListEvent(round=round, list_data=list_data)


@dataclass
class ShareKeysEvent(ListDataInRoundEvent):
    """An event of sharing keys with other calculators."""

    TYPE = 'share_keys'

    peer_id: str

    @classmethod
    def contract_to_event(cls, contract: dict) -> 'ShareKeysEvent':
        round, list_data = cls._decode_contract(contract=contract)
        peer_id = contract.get('peer_id')
        assert peer_id and isinstance(peer_id, str), f'invalid peer_id: {peer_id}'
        return ShareKeysEvent(round=round, peer_id=peer_id, list_data=list_data)


@dataclass
class DistributeUser2ListEvent(ListDataInRoundEvent):
    """An event of distributing the data of user_2 list to calculators."""

    TYPE = 'distribute_user_2_list'

    @classmethod
    def contract_to_event(cls, contract: dict) -> 'DistributeUser2ListEvent':
        round, list_data = cls._decode_contract(contract=contract)
        return DistributeUser2ListEvent(round=round, list_data=list_data)


@dataclass
class StartUnmaskingEvent(ListDataInRoundEvent):
    """An event of asking for help to do unmasking to calculators."""

    TYPE = 'unmasking'

    @classmethod
    def contract_to_event(cls, contract: dict) -> 'StartUnmaskingEvent':
        round, list_data = cls._decode_contract(contract=contract)
        return StartUnmaskingEvent(round=round, list_data=list_data)


@dataclass
class UploadSeedSharesEvent(ListDataInRoundEvent):
    """An event of uploading seed shares."""

    TYPE = 'upload_seed_shares'

    @classmethod
    def contract_to_event(cls, contract: dict) -> 'UploadSeedSharesEvent':
        round, list_data = cls._decode_contract(contract=contract)
        return UploadSeedSharesEvent(round=round, list_data=list_data)


@dataclass
class UploadSKSharesEvent(ListDataInRoundEvent):
    """An event of uploading private key shares."""

    TYPE = 'upload_sk_shares'

    @classmethod
    def contract_to_event(cls, contract: dict) -> 'UploadSKSharesEvent':
        round, list_data = cls._decode_contract(contract=contract)
        return UploadSKSharesEvent(round=round, list_data=list_data)


class SecureFedAvgEventFactory(FedAvgEventFactory):
    """A secure FedAvg event factory inherit from the vanilla one."""

    _CLASS_MAP = {
        AdvertiseKeysEvent.TYPE: AdvertiseKeysEvent,
        AdvertiseKeysResponseEvent.TYPE: AdvertiseKeysResponseEvent,
        DistributeUser1ListEvent.TYPE: DistributeUser1ListEvent,
        ShareKeysEvent.TYPE: ShareKeysEvent,
        DistributeUser2ListEvent.TYPE: DistributeUser2ListEvent,
        StartUnmaskingEvent.TYPE: StartUnmaskingEvent,
        UploadSeedSharesEvent.TYPE: UploadSeedSharesEvent,
        UploadSKSharesEvent.TYPE: UploadSKSharesEvent,
        **FedAvgEventFactory._CLASS_MAP
    }


class SecureFedAvgContractorMixin(ABC):

    def advertise_keys(self, round: int, calculators: List[str]):
        """Start to advertise keys."""
        assert (
            calculators and isinstance(calculators, list)
            and all(_target and isinstance(_target, str) for _target in calculators)
        ), f'invalid target list: {calculators}'
        event = AdvertiseKeysEvent(round=round, calculators=calculators)
        self._new_contract(targets=calculators, event=event)

    def respond_advertise_keys(self,
                               round: int,
                               peer_id: str,
                               c_pk: bytes,
                               s_pk: bytes,
                               aggregator: str):
        """Respond to advertise keys."""
        assert aggregator and isinstance(aggregator, str), f'invalid target: {aggregator}'
        event = AdvertiseKeysResponseEvent(round=round, peer_id=peer_id, c_pk=c_pk, s_pk=s_pk)
        self._new_contract(targets=[aggregator], event=event)

    def distribute_user_1_list(self, round: int, list_data: List[str], targets: List[str]):
        """Distribute the data of user_1 list to all user_1s."""
        assert (
            targets and isinstance(targets, list)
            and all(_target and isinstance(_target, str) for _target in targets)
        ), f'invalid target list: {targets}'
        event = DistributeUser1ListEvent(round=round, list_data=list_data)
        self._new_contract(targets=targets, event=event)

    def share_keys(self, round: int, list_data: List[str], peer_id: str, aggregator: str):
        """Send the information of shared keys to the aggregator in the form of user_2."""
        assert aggregator and isinstance(aggregator, str), f'invalid target: {aggregator}'
        event = ShareKeysEvent(round=round, peer_id=peer_id, list_data=list_data)
        self._new_contract(targets=[aggregator], event=event)

    def distribute_user_2_list(self, round: int, list_data: List[str], targets: List[str]):
        """Distribute the data of user_2 list to all user_2s."""
        assert (
            targets and isinstance(targets, list)
            and all(_target and isinstance(_target, str) for _target in targets)
        ), f'invalid target list: {targets}'
        event = DistributeUser2ListEvent(round=round, list_data=list_data)
        self._new_contract(targets=targets, event=event)

    def start_unmasking(self, round: int, list_data: List[str], targets: List[str]):
        """Ask for help to do unmasking."""
        assert (
            targets and isinstance(targets, list)
            and all(_target and isinstance(_target, str) for _target in targets)
        ), f'invalid target list: {targets}'
        event = StartUnmaskingEvent(round=round, list_data=list_data)
        self._new_contract(targets=targets, event=event)

    def upload_seed_shares(self, round: int, list_data: List[str], aggregator: str):
        """Upload seed shares to the aggregator."""
        assert aggregator and isinstance(aggregator, str), f'invalid target: {aggregator}'
        event = UploadSeedSharesEvent(round=round, list_data=list_data)
        self._new_contract(targets=[aggregator], event=event)

    def upload_sk_shares(self, round: int, list_data: List[str], aggregator: str):
        """Upload private key shares to the aggregator."""
        assert aggregator and isinstance(aggregator, str), f'invalid target: {aggregator}'
        event = UploadSKSharesEvent(round=round, list_data=list_data)
        self._new_contract(targets=[aggregator], event=event)


class SecureFedAvgContractor(FedAvgContractor, SecureFedAvgContractorMixin):
    """A secure FedAvg contractor inherit from the vanilla one."""

    def __init__(self, task_id: str):
        super().__init__(task_id=task_id)
        self._event_factory = SecureFedAvgEventFactory


class AutoSecureFedAvgContractor(AutoFedAvgContractor, SecureFedAvgContractorMixin):
    """A secure FedAvg contractor inherit from the vanilla one."""

    def __init__(self, task_id: str):
        super().__init__(task_id=task_id)
        self._event_factory = SecureFedAvgEventFactory
