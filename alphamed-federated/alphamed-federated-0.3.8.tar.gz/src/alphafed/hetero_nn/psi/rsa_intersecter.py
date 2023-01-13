"""A implementation of RSA intersection protocol."""

import hashlib
import json
import random
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Set

import gmpy2
from Crypto.PublicKey import RSA
from Cryptodome import Random

from ... import logger
from ...data_channel import SharedFileDataChannel
from . import PSICollaboratorScheduler, PSIInitiatorScheduler
from .rsa_psi_contractor import (DistributingIntersectionEvent, PSIInitEvent,
                                 PublicKeyEvent, ReadyForSignedIdsEvent,
                                 RSAContractor, SendingBlindIdsEvent,
                                 SendingSignedIdsEvent)

__all__ = ['RSAPSIInitiatorScheduler', 'RSAPSICollaboratorScheduler']

hexstr = str

_ENCODING = 'utf-8'


@dataclass
class _IDInfo:

    id: str
    r: int
    blind_id: hexstr


class _PSIRole:

    _RSA_BIT = 1024

    def __init__(self) -> None:
        random_generator = Random.new().read
        self.rsa = RSA.generate(self._RSA_BIT, random_generator)
        self.e = self.rsa.e
        self.d = self.rsa.d
        self.n = self.rsa.n
        self.p = self.rsa.p
        self.q = self.rsa.q
        self.crt_p = gmpy2.invert(self.p, self.q) * self.q
        self.crt_q = gmpy2.invert(self.q, self.p) * self.p

    def _hash_1(self, data: str) -> hexstr:
        return hashlib.sha256(data.encode(_ENCODING)).hexdigest()

    def _hash_2(self, data: str) -> hexstr:
        return hashlib.sha256(data.encode(_ENCODING)).hexdigest()

    def _crt_powmod(self, data: int) -> int:
        """Use CRT(Chinese Remainder Theorem) to speed up calculation."""
        mp = gmpy2.powmod(data, self.d % (self.p - 1), self.p)
        mq = gmpy2.powmod(data, self.d % (self.q - 1), self.q)
        return int((self.crt_p * mp + self.crt_q * mq) % self.n)


class _PSIInitiator(_PSIRole):
    """The initiator who applies a PSI using RSA protocole."""

    _RANDOM_BIT = 128

    def __init__(self) -> None:
        super().__init__()
        self.blind_id_map: Dict[int, _IDInfo] = {}
        self.hashed_id_map: Dict[hexstr, _IDInfo] = {}

    def set_peer_keys(self, n: int, e: int):
        """Record the public key of a specified peer."""
        self.mate_n = n
        self.mate_e = e

    def blind_self_ids(self, plain_ids: List[str]) -> List[hexstr]:
        for _id in plain_ids:
            r = random.getrandbits(self._RANDOM_BIT)
            hashed = self._hash_1(_id)
            int_hashed = int(hashed, base=16)
            blind_id = int(gmpy2.powmod(r, self.mate_e, self.mate_n) * int_hashed % self.mate_n)
            self.blind_id_map[blind_id] = _IDInfo(id=_id, r=r, blind_id=blind_id)
        return list(hex(info.blind_id) for info in self.blind_id_map.values())

    def append_sign(self, signed_ids: Dict[hexstr, hexstr]) -> List[hexstr]:
        """Append signature to signed ids from the collaborator."""
        for _signed_id, _blind_id in signed_ids.items():
            int_signed = int(_signed_id, base=16)
            int_blind = int(_blind_id, base=16)
            r = self.blind_id_map[int_blind].r
            appended = int(gmpy2.powmod(r, -1, self.mate_n) * int_signed % self.mate_n)
            hashed = self._hash_2(hex(appended))
            self.hashed_id_map[hashed] = self.blind_id_map[int_blind]
        return list(self.hashed_id_map.keys())

    def signed_to_raw(self, signed_id: hexstr) -> Optional[str]:
        """Map the final signed value to its original value."""
        id_info = self.hashed_id_map.get(signed_id)
        return id_info.id if id_info else None


class _PSICollaborator(_PSIRole):
    """The collaborator who responds a PSI application using RSA protocole."""

    def __init__(self) -> None:
        super().__init__()
        self.signed_id_map: Dict[str, str] = {}  # self signed id => raw_id

    def sign_self_ids(self, plain_ids: List[str]) -> List[hexstr]:
        for _id in plain_ids:
            hex_id = self._hash_1(_id)
            int_id = int(hex_id, base=16)
            signed = int(self._crt_powmod(int_id))
            hashed = self._hash_2(hex(signed))
            self.signed_id_map[hashed] = _id
        return list(self.signed_id_map.keys())

    def sign_blind_ids(self, blind_ids: List[hexstr]) -> Dict[hexstr, hexstr]:
        """Sign blind ids from the initiator.

        :return
            signed_id => blind_id map
        """
        signed_id_map = {}
        for _id in blind_ids:
            int_id = int(_id, base=16)
            signed_id = self._crt_powmod(int_id)
            signed_id_map[hex(signed_id)] = _id
        return signed_id_map

    def signed_to_raw(self, signed_id: hexstr) -> Optional[str]:
        """Map the final signed value to its original value."""
        return self.signed_id_map.get(signed_id, None)


@dataclass
class _SignedIdsInfo:

    signed_blind_ids: Dict[hexstr, hexstr]
    signed_collaborator_ids: List[hexstr]

    def to_bytes(self) -> bytes:
        json_data = asdict(self)
        str_data = json.dumps(json_data)
        return str_data.encode(encoding=_ENCODING)

    @classmethod
    def from_bytes(cls, stream: bytes) -> '_SignedIdsInfo':
        try:
            json_data: dict = json.loads(stream.decode(encoding=_ENCODING))
        except (UnicodeDecodeError, json.JSONDecodeError) as err:
            logger.error('Failed to construct signed ids data.')
            logger.exception(err)
        signed_blind_ids = json_data.get('signed_blind_ids')
        signed_collaborator_ids = json_data.get('signed_collaborator_ids')
        assert (
            signed_blind_ids and signed_collaborator_ids
        ), 'Failed to construct signed ids data. Missing required keys.'
        return _SignedIdsInfo(signed_blind_ids=signed_blind_ids,
                              signed_collaborator_ids=signed_collaborator_ids)


class RSAPSIInitiatorScheduler(PSIInitiatorScheduler):

    _INIT = 'init'
    _KICKING_OFF = 'kicking_off'
    _COLLECTING_PUB_KEY = 'collecting_pub_key'
    _SENDING_BLIND_IDS = 'sending_blind_ids'
    _COLLECTING_SIGNED_IDS = 'collecting_signed_ids'
    _INTERSECTING = 'intersecting'
    _DISTRIBUTING_INTERSECTION = 'distributing_intersection'

    def __init__(self,
                 task_id: str,
                 initiator_id: str,
                 ids: List[str],
                 collaborator_ids: List[str],
                 contractor: RSAContractor = None) -> None:
        super().__init__(task_id=task_id,
                         initiator_id=initiator_id,
                         ids=ids,
                         collaborator_ids=collaborator_ids)
        self._switch_status(self._INIT)
        self._contractor = contractor or RSAContractor(task_id=task_id)
        self._data_channel = SharedFileDataChannel(contractor=self._contractor)

        self.coll_init_map: Dict[str, _PSIInitiator] = {}
        self.coll_signed_ids_map: Dict[str, _SignedIdsInfo] = {}
        self.intersection: Set[str] = {}

    def make_intersection(self) -> Set[str]:
        self._switch_status(self._KICKING_OFF)
        self._initiate_procedure()

        self._switch_status(self._COLLECTING_PUB_KEY)
        self._collect_public_keys()

        self._switch_status(self._SENDING_BLIND_IDS)
        self._send_blind_ids()

        self._switch_status(self._COLLECTING_SIGNED_IDS)
        self._wait_for_signed_ids()

        self._switch_status(self._INTERSECTING)
        self._obtain_intersection()

        self._switch_status(self._DISTRIBUTING_INTERSECTION)
        self._distribute_intersection()

        return self.intersection

    def _initiate_procedure(self):
        """Initiate the PSI procedure."""
        for _coll in self.collaborator_ids:
            self._contractor.initiate(initiator=self.initiator_id, target=_coll)

    def _collect_public_keys(self) -> Dict[str, _PSIInitiator]:
        """Collect public key and initialize initiator context for each collaborator."""
        for _event in self._contractor.contract_events():
            if isinstance(_event, PublicKeyEvent):
                if _event.collaborator not in self.collaborator_ids:
                    continue
                _init = _PSIInitiator()
                _init.set_peer_keys(n=_event.n, e=_event.e)
                self.coll_init_map[_event.collaborator] = _init

                if len(self.coll_init_map) == len(self.collaborator_ids):
                    return

    def _send_blind_ids(self):
        """Calculate and send blind ids for each collaborator."""
        for _coll, _init in self.coll_init_map.items():
            blind_ids = _init.blind_self_ids(plain_ids=self.ids)
            blind_ids_stream = json.dumps(list(blind_ids)).encode(encoding=_ENCODING)
            self._data_channel.send_stream(source=self.initiator_id,
                                           target=_coll,
                                           data_stream=blind_ids_stream)

    def _wait_for_signed_ids(self):
        self._contractor.notify_ready_for_signed_ids(initiator=self.initiator_id)
        for _event in self._contractor.contract_events():
            if isinstance(_event, SendingSignedIdsEvent):
                signed_ids_stream = self._data_channel.receive_stream(
                    apply_event=_event, receiver=self.initiator_id)
                signed_ids = _SignedIdsInfo.from_bytes(signed_ids_stream)
                self.coll_signed_ids_map[_event.source] = signed_ids
            if len(self.coll_signed_ids_map) == len(self.collaborator_ids):
                return

    def _obtain_intersection(self):
        self.intersection = set(self.ids)
        for _coll, _signed_ids in self.coll_signed_ids_map.items():
            _init = self.coll_init_map[_coll]
            signed_init_ids = _init.append_sign(_signed_ids.signed_blind_ids)
            signed_coll_ids = _signed_ids.signed_collaborator_ids
            intersection_signed = set(signed_init_ids).intersection(signed_coll_ids)
            intersection_coll = set(_init.signed_to_raw(_signed_id)
                                    for _signed_id in intersection_signed)
            self.intersection = self.intersection.intersection(intersection_coll)

    def _distribute_intersection(self):
        for _coll, _signed_ids in self.coll_signed_ids_map.items():
            _init = self.coll_init_map[_coll]
            intersection_coll = set(_signed_id
                                    for _signed_id in _signed_ids.signed_collaborator_ids
                                    if _init.signed_to_raw(_signed_id) in self.intersection)
            intersection_stream = json.dumps(list(intersection_coll)).encode(encoding=_ENCODING)
            self._data_channel.send_stream(source=self.initiator_id,
                                           target=_coll,
                                           data_stream=intersection_stream)


class RSAPSICollaboratorScheduler(PSICollaboratorScheduler):

    _INIT = 'init'
    _READY = 'ready'
    _RECEIVING_BLIND_IDS = 'receiving_blind_ids'
    _SIGNING = 'signing'
    _SENDING_SIGNED_IDS = 'sending_signed_ids'
    _RECEIVING_INTERSECTION = 'receiving_intersection'

    def __init__(self,
                 task_id: str,
                 collaborator_id: str,
                 ids: List[str],
                 contractor: RSAContractor = None) -> None:
        super().__init__(task_id=task_id,
                         collaborator_id=collaborator_id,
                         ids=ids)
        self._switch_status(self._INIT)
        self._contractor = contractor or RSAContractor(task_id=task_id)
        self._data_channel = SharedFileDataChannel(contractor=self._contractor)
        self._coll = None

        self.intersection: Set[str] = {}

    def collaborate_intersection(self) -> Set[str]:
        self._switch_status(self._READY)
        self._wait_for_launch()

        self._switch_status(self._RECEIVING_BLIND_IDS)
        blind_ids = self._wait_for_blind_ids()

        self._switch_status(self._SIGNING)
        signed_blind_ids = self._coll.sign_blind_ids(blind_ids=blind_ids)
        signed_collaborator_ids = self._coll.sign_self_ids(plain_ids=self.ids)

        self._switch_status(self._SENDING_SIGNED_IDS)
        self._send_signed_ids(signed_blind_ids=signed_blind_ids,
                              signed_collaborator_ids=signed_collaborator_ids)

        self._switch_status(self._RECEIVING_INTERSECTION)
        self._wait_for_intersection()
        return self.intersection

    def _wait_for_launch(self) -> _PSICollaborator:
        """Wait for kicking off of the PSI procedure and initialize collaborator context."""
        for _event in self._contractor.contract_events():
            if isinstance(_event, PSIInitEvent):
                self._coll = _PSICollaborator()
                self._contractor.send_public_key(collaborator=self.collaborator_id,
                                                 n=self._coll.n,
                                                 e=self._coll.e,
                                                 target=_event.initiator)
                return

    def _wait_for_blind_ids(self) -> List[hexstr]:
        """Wait for blind ids to sign."""
        for _event in self._contractor.contract_events():
            if isinstance(_event, SendingBlindIdsEvent):
                data_stream = self._data_channel.receive_stream(
                    apply_event=_event, receiver=self.collaborator_id
                )
                blind_ids = json.loads(data_stream.decode(encoding=_ENCODING))
                return blind_ids

    def _send_signed_ids(self,
                         signed_blind_ids: Dict[hexstr, hexstr],
                         signed_collaborator_ids: List[hexstr]):
        """Send signed blind ids and self ids to the initiator."""
        for _event in self._contractor.contract_events():
            if isinstance(_event, ReadyForSignedIdsEvent):
                signed_ids = _SignedIdsInfo(signed_blind_ids=signed_blind_ids,
                                            signed_collaborator_ids=signed_collaborator_ids)
                self._data_channel.send_stream(source=self.collaborator_id,
                                               target=_event.initiator,
                                               data_stream=signed_ids.to_bytes())
                return

    def _wait_for_intersection(self):
        """Wait for receiving intersection result."""
        for _event in self._contractor.contract_events():
            if isinstance(_event, DistributingIntersectionEvent):
                intersection_stream = self._data_channel.receive_stream(
                    apply_event=_event, receiver=self.collaborator_id
                )
                _intersection = json.loads(intersection_stream.decode(encoding=_ENCODING))
                self.intersection = set(self._coll.signed_to_raw(_signed_id)
                                        for _signed_id in _intersection)
                return
