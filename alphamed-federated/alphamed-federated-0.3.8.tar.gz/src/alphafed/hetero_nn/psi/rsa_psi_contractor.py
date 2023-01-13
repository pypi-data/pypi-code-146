"""RSA based PSI intersection contractor."""

from dataclasses import dataclass
from typing import Dict

from ...contractor import (ApplySharedFileSendingDataEvent, ContractEvent,
                           TaskMessageContractor, TaskMessageEventFactory)


@dataclass
class PSIInitEvent(ContractEvent):
    """An event to initiate a RSA based PSI session."""

    TYPE = 'rsa_psi_init'

    initiator: str

    @classmethod
    def contract_to_event(cls, contract: dict) -> 'PSIInitEvent':
        event_type = contract.get('type')
        initiator = contract.get('initiator')
        assert event_type == cls.TYPE, f'合约类型错误: {event_type}'
        assert initiator and isinstance(initiator, str), f'invalid initiator: {initiator}'
        return PSIInitEvent(initiator=initiator)


@dataclass
class PublicKeyEvent(ContractEvent):
    """An event to send the public key."""

    TYPE = 'public_key'

    collaborator: str
    n: int
    e: int

    def event_to_contract(self) -> dict:
        event_dict = super().event_to_contract()
        # n is a so big integer that it could be transfered to the format like 1.2e345
        event_dict['n'] = str(self.n)
        return event_dict

    @classmethod
    def contract_to_event(cls, contract: dict) -> 'PublicKeyEvent':
        event_type = contract.get('type')
        collaborator = contract.get('collaborator')
        n = contract.get('n')
        e = contract.get('e')
        assert event_type == cls.TYPE, f'合约类型错误: {event_type}'
        assert (
            collaborator and isinstance(collaborator, str)
        ), f'invalid collaborator: {collaborator}'
        assert n and isinstance(n, str) and n.isdecimal(), f'invalid public key: {n=}'
        n = int(n)
        assert n > 0, f'invalid public key: {n=}'
        assert e and isinstance(e, int) and n > 0, f'invalid public key: {e=}'
        return PublicKeyEvent(collaborator=collaborator, n=n, e=e)


@dataclass
class ReadyForSignedIdsEvent(ContractEvent):
    """An event to send the public key."""

    TYPE = 'ready_for_signed_ids'

    initiator: str

    @classmethod
    def contract_to_event(cls, contract: dict) -> 'ReadyForSignedIdsEvent':
        event_type = contract.get('type')
        initiator = contract.get('initiator')
        assert event_type == cls.TYPE, f'合约类型错误: {event_type}'
        assert initiator and isinstance(initiator, str), f'invalid initiator: {initiator}'
        return ReadyForSignedIdsEvent(initiator=initiator)


# define some more friendly alias
SendingBlindIdsEvent = ApplySharedFileSendingDataEvent
SendingSignedIdsEvent = ApplySharedFileSendingDataEvent
DistributingIntersectionEvent = ApplySharedFileSendingDataEvent


class RSAEventFactory(TaskMessageEventFactory):

    _CLASS_MAP: Dict[str, ContractEvent] = {
        PSIInitEvent.TYPE: PSIInitEvent,
        PublicKeyEvent.TYPE: PublicKeyEvent,
        ReadyForSignedIdsEvent.TYPE: ReadyForSignedIdsEvent,
        **TaskMessageEventFactory._CLASS_MAP
    }


class RSAContractor(TaskMessageContractor):

    def __init__(self, task_id: str) -> None:
        super().__init__(task_id=task_id)
        self._event_factory = RSAEventFactory

    def initiate(self, initiator: str, target: str):
        """Initiate a RSA based PSI session with the specified target."""
        event = PSIInitEvent(initiator=initiator)
        self._new_contract(targets=[target], event=event)

    def send_public_key(self, collaborator: str, n: int, e: int, target: str):
        """Respond the public key to the initiator."""
        event = PublicKeyEvent(collaborator=collaborator, n=n, e=e)
        self._new_contract(targets=[target], event=event)

    def notify_ready_for_signed_ids(self, initiator: str):
        """Notify all collaborators that the initiator is ready for receiving signed ids."""
        event = ReadyForSignedIdsEvent(initiator=initiator)
        self._new_contract(targets=self.EVERYONE, event=event)
