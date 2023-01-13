"""Secure Aggregation FedAvg scheduler.

Reference: https://eprint.iacr.org/2017/281.pdf
"""


import base64
import io
import json
import secrets
from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
import torch
from numpy.random import Generator

from .. import logger
from ..scheduler import ConfigError, TaskComplete
from ..secure import aes
from ..secure.ecdhe import new_key_pair, new_shared_key
from ..secure.shamir import SecretShare
from .contractor import (CheckinEvent, FinishTaskEvent, ResetRoundEvent,
                         UploadTrainingResultsEvent)
from .fed_avg import AggregationError, FedAvgScheduler, ResetRound
from .secure_contractor import (AdvertiseKeysEvent, AdvertiseKeysResponseEvent,
                                DistributeUser1ListEvent,
                                DistributeUser2ListEvent,
                                SecureFedAvgContractor, ShareKeysEvent,
                                StartUnmaskingEvent, UploadSeedSharesEvent,
                                UploadSKSharesEvent)

__all__ = ['SecureFedAvgScheduler']


@dataclass
class _User1Info:

    peer_id: str
    c_pk: bytes
    s_pk: bytes
    comm_key: bytes = None

    def encode(self) -> str:
        """Encode user_1 information into a string in benefit of transmission."""
        base64_c_pk = base64.b64encode(self.c_pk).decode()
        base64_s_pk = base64.b64encode(self.s_pk).decode()
        return json.dumps({
            'peer_id': self.peer_id,
            'c_pk': base64_c_pk,
            's_pk': base64_s_pk
        })

    @classmethod
    def decode(cls, encoded: str) -> '_User1Info':
        """Decode data string into a _User1Info object."""
        assert (
            encoded and isinstance(encoded, str)
        ), f'invalid type of user_1 data: {type(encoded)}'
        user_json = json.loads(encoded)
        assert user_json and isinstance(user_json, dict), f'invalid user data: {encoded}'
        peer_id = user_json.get('peer_id')
        base64_c_pk = user_json.get('c_pk')
        base64_s_pk = user_json.get('s_pk')
        assert peer_id and isinstance(peer_id, str), f'invalid peer_id: {peer_id}'
        assert base64_c_pk and isinstance(base64_c_pk, str), f'invalid base64_c_pk: {base64_c_pk}'
        assert base64_s_pk and isinstance(base64_s_pk, str), f'invalid base64_s_pk: {base64_s_pk}'
        c_pk = base64.b64decode(base64_c_pk.encode())
        s_pk = base64.b64decode(base64_s_pk.encode())
        return _User1Info(peer_id=peer_id, c_pk=c_pk, s_pk=s_pk)


@dataclass
class _User2Info:

    source_id: str
    target_id: str
    seed_share: bytes
    sk_share: bytes
    comm_key: bytes = None
    s_pk: bytes = None
    PRG: Generator = None

    def encode(self) -> str:
        """Encode user_1 information into a string in benefit of transmission."""
        base64_seed_share = base64.b64encode(self.seed_share).decode()
        base64_sk_share = base64.b64encode(self.sk_share).decode()
        return json.dumps({
            'source_id': self.source_id,
            'target_id': self.target_id,
            'seed_share': base64_seed_share,
            'sk_share': base64_sk_share
        })

    @classmethod
    def decode(cls, encoded: str) -> '_User2Info':
        """Decode data string into a _User2Info object."""
        assert (
            encoded and isinstance(encoded, str)
        ), f'invalid type of user_2 data: {type(encoded)}'
        user_json = json.loads(encoded)
        assert user_json and isinstance(user_json, dict), f'invalid user data: {encoded}'
        source_id = user_json.get('source_id')
        target_id = user_json.get('target_id')
        base64_seed_share = user_json.get('seed_share')
        base64_sk_share = user_json.get('sk_share')
        assert source_id and isinstance(source_id, str), f'invalid source_id: {source_id}'
        assert target_id and isinstance(target_id, str), f'invalid target_id: {target_id}'
        assert (
            base64_seed_share and isinstance(base64_seed_share, str)
        ), f'invalid base64_seed_share: {base64_seed_share}'
        assert (
            base64_sk_share and isinstance(base64_sk_share, str)
        ), f'invalid base64_sk_share: {base64_sk_share}'
        seed_share = base64.b64decode(base64_seed_share.encode())
        sk_share = base64.b64decode(base64_sk_share.encode())
        return _User2Info(source_id=source_id,
                          target_id=target_id,
                          seed_share=seed_share,
                          sk_share=sk_share)


@dataclass
class _SeedShareInfo:

    peer_id: str
    seed_share: bytes

    def encode(self) -> str:
        """Encode user_1 information into a string in benefit of transmission."""
        base64_seed_share = base64.b64encode(self.seed_share).decode()
        return json.dumps({
            'peer_id': self.peer_id,
            'seed_share': base64_seed_share
        })

    @classmethod
    def decode(cls, encoded: str) -> '_SeedShareInfo':
        """Decode data string into a _User2Info object."""
        assert (
            encoded and isinstance(encoded, str)
        ), f'invalid type of user_2 data: {type(encoded)}'
        user_json = json.loads(encoded)
        assert user_json and isinstance(user_json, dict), f'invalid user data: {encoded}'
        peer_id = user_json.get('peer_id')
        base64_seed_share = user_json.get('seed_share')
        assert peer_id and isinstance(peer_id, str), f'invalid peer_id: {peer_id}'
        assert (
            base64_seed_share and isinstance(base64_seed_share, str)
        ), f'invalid base64_seed_share: {base64_seed_share}'
        seed_share = base64.b64decode(base64_seed_share.encode())
        return _SeedShareInfo(peer_id=peer_id, seed_share=seed_share)


@dataclass
class _SKShareInfo:

    peer_id: str
    sk_share: bytes

    def encode(self) -> str:
        """Encode user_1 information into a string in benefit of transmission."""
        base64_sk_share = base64.b64encode(self.sk_share).decode()
        return json.dumps({
            'peer_id': self.peer_id,
            'sk_share': base64_sk_share
        })

    @classmethod
    def decode(cls, encoded: str) -> '_SKShareInfo':
        """Decode data string into a _User2Info object."""
        assert (
            encoded and isinstance(encoded, str)
        ), f'invalid type of user_2 data: {type(encoded)}'
        user_json = json.loads(encoded)
        assert user_json and isinstance(user_json, dict), f'invalid user data: {encoded}'
        peer_id = user_json.get('peer_id')
        base64_sk_share = user_json.get('sk_share')
        assert peer_id and isinstance(peer_id, str), f'invalid peer_id: {peer_id}'
        assert (
            base64_sk_share and isinstance(base64_sk_share, str)
        ), f'invalid base64_sk_share: {base64_sk_share}'
        sk_share = base64.b64decode(base64_sk_share.encode())
        return _SKShareInfo(peer_id=peer_id, sk_share=sk_share)


class SecureFedAvgScheduler(FedAvgScheduler):
    """A FedAvg scheduler transmit parameters in a secure way."""

    _ADVERTISE_KEYS = 'advertise_keys'
    _SHARE_KEYS = 'share_keys'
    _MASKED_INPUT_COLLECTION = 'masked_input_collection'
    _UNMASKING = 'unmasking'

    def __init__(self,
                 min_clients: int,
                 max_clients: int,
                 t: int,
                 name: str = None,
                 max_rounds: int = 0,
                 merge_epochs: int = 1,
                 calculation_timeout: int = 300,
                 perf_bench_timeout: int = 30,
                 schedule_timeout: int = 30,
                 log_rounds: int = 0,
                 is_centralized: bool = True):
        """Init.

        Reference: https://eprint.iacr.org/2017/281.pdf

        Because of conflicting with this Privacy-Preserving protocol, `involve aggregator`
        mode is not supported.

        Args:
            participants:
                ID list of all participants registered on the task.
            min_clients:
                Minimal number of calculators for each round, at least 3.
            max_clients:
                Maximal number of calculators for each round.
            t:
                The threshold value t for restoring a shared secret.
            max_rounds:
                Maximal number of training rounds.
            merge_epochs:
                The number of epochs to run before aggregation is performed.
            calculation_timeout:
                Seconds to timeout for calculation in a round. Takeing off timeout
                by setting its value to 0.
            perf_bench_timeout:
                Seconds to timeout for performing performance benchmark. Takeing off timeout
                by setting its value to 0.
            schedule_timeout:
                Seconds to timeout for process scheduling. Takeing off timeout
                by setting its value to 0.
            log_rounds:
                The number of rounds to run testing and log the result. Skip it
                by setting its value to 0.
            is_centralized:
                If specify centralized, the aggregator will always be the initiator of the
                task, otherwize a new aggregator is elected for each round during training.
        """
        super().__init__(min_clients=min_clients,
                         max_clients=max_clients,
                         name=name,
                         max_rounds=max_rounds,
                         merge_epochs=merge_epochs,
                         calculation_timeout=calculation_timeout,
                         perf_bench_timeout=perf_bench_timeout,
                         schedule_timeout=schedule_timeout,
                         log_rounds=log_rounds,
                         is_centralized=is_centralized)
        self._users_1: List[_User1Info] = []
        self._users_2: List[_User2Info] = []
        self._users_3: List[str] = []

        self._c_sk: bytes = None
        self._c_pk: bytes = None
        self._s_sk: bytes = None
        self._s_pk: bytes = None
        self._seed: bytes = None

        self._seed_shares: Dict[str, List[bytes]] = {}
        self._sk_shares: Dict[str, List[bytes]] = {}

        self._t = t

        self._validate_secure_config()

    def _validate_secure_config(self):
        # if self.min_clients < 4:
        if self.min_clients < 3:  # TODO it should be 4
            raise ConfigError('secure mode works only with at least 4 participants')
        if self._t > self.min_clients - 1:
            raise ConfigError('threshold t must be equal or less than min_clients - 1')

    def _setup_context(self, id: str, task_id: str, is_initiator: bool = False):
        super()._setup_context(id, task_id, is_initiator)
        self.contractor = SecureFedAvgContractor(task_id=self.task_id)

    def _get_user_2_num(self):
        """Return the number of user_2.

        An aggregator saves a (n-1) * m matrix. A calculator saves a n-1 list.
        """
        if self.is_aggregator:
            return len(set(_user.source_id for _user in self._users_2))
        else:
            return len(self._users_2)

    def _process_aggregation(self):
        self._switch_status(self._ADVERTISE_KEYS)
        self.push_log('Initiate advertising keys.')
        self.contractor.advertise_keys(round=self.current_round, calculators=self._calculators)
        self._wait_for_responses_of_advertising_keys()
        self.push_log(f'Gathered user_1 list: {[_user.peer_id for _user in self._users_1]}')
        list_data = [_user.encode() for _user in self._users_1]
        self.contractor.distribute_user_1_list(round=self.current_round,
                                               list_data=list_data,
                                               targets=[_user.peer_id for _user in self._users_1])
        self.push_log('Distributed user_1 list.')

        self._switch_status(self._SHARE_KEYS)
        self._wait_for_sharing_keys()
        self.push_log(f'Gathered user_2 list: {[_user.source_id for _user in self._users_2]}')
        list_data = [_user.encode() for _user in self._users_2]
        self.contractor.distribute_user_2_list(
            round=self.current_round,
            list_data=list_data,
            targets=list(set(_user.source_id for _user in self._users_2))
        )
        self.push_log('Distributed user_2 list.')

        self._switch_status(self._MASKED_INPUT_COLLECTION)
        self.contractor.notify_ready_for_aggregation(round=self.current_round)
        self.push_log('Now waiting for executing calculation ...')
        accum_result, result_count = self._wait_for_calculation()
        self.push_log(f'Gathered user_3 list: {self._users_3}')

        self._switch_status(self._UNMASKING)
        self.push_log('Trying to unmask parameters ...')
        self.contractor.start_unmasking(round=self.current_round,
                                        list_data=self._users_3,
                                        targets=self._users_3)
        self._wait_for_collecting_shares()

        self._switch_status(self._AGGREGATING)
        self._aggregate_results(accum_result=accum_result, result_count=result_count)

    def _wait_for_responses_of_advertising_keys(self):
        """Wait for responses of advertising keys as an aggregator."""
        self.push_log('Waiting for receiving advertised keys ...')
        self._users_1.clear()
        advertised_ids = []
        for _event in self.contractor.contract_events(timeout=self.schedule_timeout):
            if isinstance(_event, AdvertiseKeysResponseEvent):
                if _event.round != self.current_round:
                    continue
                if _event.peer_id in advertised_ids:
                    continue
                self._users_1.append(_User1Info(peer_id=_event.peer_id,
                                                c_pk=_event.c_pk,
                                                s_pk=_event.s_pk))
                advertised_ids.append(_event.peer_id)
                self.push_log(f'Received advertised keys from ID: {_event.peer_id}.')
                if len(self._users_1) == len(self._calculators):
                    break

            elif isinstance(_event, CheckinEvent):
                self._handle_check_in(_event)

        if len(self._users_1) < self._t:
            self.push_log('Task failed because of too few users_1.')
            raise AggregationError(f'too few users_1: {len(self._users_1)}')

    def _wait_for_sharing_keys(self):
        """Wait for shared keys uploaded by calculators."""
        self.push_log('Waiting for receiving shared keys from users_1 ...')
        self._users_2.clear()
        shared_ids = []
        for _event in self.contractor.contract_events(timeout=self.schedule_timeout):
            if isinstance(_event, ShareKeysEvent):
                if _event.round != self.current_round:
                    continue
                if _event.peer_id in shared_ids:
                    continue
                self._users_2.extend(_User2Info.decode(_item) for _item in _event.list_data)
                shared_ids.append(_event.peer_id)
                self.push_log(f'Received shared keys from ID: {_event.peer_id}')
                if len(shared_ids) == len(self._users_1):
                    break

            elif isinstance(_event, CheckinEvent):
                self._handle_check_in(_event)

        if len(shared_ids) < self._t:
            self.push_log('Task failed because of too few users_1.')
            raise AggregationError(f'too few users_2: {len(shared_ids)}')

    def _wait_for_calculation(self) -> Tuple[Dict[str, torch.Tensor], int]:
        """Wait for every calculator finish its task or timeout."""
        self._users_3.clear()
        user_2_num = self._get_user_2_num()
        accum_result = self.state_dict()
        for _key, _param in accum_result.items():
            if isinstance(_param, torch.Tensor):
                accum_result[_key] = _param.cpu().zero_()
            else:
                logger.warn(f'not Tensor value: {_key=}; {_param=}; {type(_param)=}')

        self.push_log('Waiting for training results ...')
        for _event in self.contractor.contract_events(timeout=self.calculation_timeout):
            if isinstance(_event, UploadTrainingResultsEvent):
                if self.id not in _event.target:
                    continue
                training_result = self.data_channel.receive_stream(apply_event=_event,
                                                                   receiver=self.id)
                buffer = io.BytesIO(training_result)
                _new_state_dict = torch.load(buffer)
                for _key in accum_result.keys():
                    accum_result[_key].add_(_new_state_dict[_key])
                self._users_3.append(_event.source)
                self.push_log(f'Received calculation results from ID: {_event.source}')

                if len(self._users_3) >= user_2_num:
                    return accum_result, len(self._users_3)

            elif isinstance(_event, CheckinEvent):
                self._handle_check_in(_event)

        if len(self._users_3) < self._t:
            self.push_log('Task failed because of too few users_1.')
            raise AggregationError(f'too few user_3: {len(self._users_3)}')
        return accum_result, len(self._users_3)

    def _wait_for_collecting_shares(self):
        """Wait for alive calculators uploading seed shares and private key shares."""
        self._seed_shares.clear()
        self._sk_shares.clear()
        user_2_num = self._get_user_2_num()

        self.push_log('Waiting for collecting secret shares ...')
        for _event in self.contractor.contract_events(timeout=self.schedule_timeout):
            if isinstance(_event, UploadSeedSharesEvent):
                if _event.round != self.current_round:
                    continue

                share_info = [_SeedShareInfo.decode(_item) for _item in _event.list_data]
                for _info in share_info:
                    if _info.peer_id not in self._seed_shares:
                        self._seed_shares[_info.peer_id] = []
                    self._seed_shares[_info.peer_id].append(_info.seed_share)
                self.push_log('Received a copy of seed shares.')

                if (
                    len(self._seed_shares) + len(self._sk_shares) == user_2_num
                    and all(len(shares) == len(self._users_3) - 1  # except the one self
                            for shares in self._seed_shares.values())
                    and all(len(shares) == len(self._users_3)
                            for shares in self._sk_shares.values())
                ):
                    break

            if isinstance(_event, UploadSKSharesEvent):
                if _event.round != self.current_round:
                    continue

                share_info = [_SKShareInfo.decode(_item) for _item in _event.list_data]
                for _info in share_info:
                    if _info.peer_id not in self._sk_shares:
                        self._sk_shares[_info.peer_id] = []
                    self._sk_shares[_info.peer_id].append(_info.sk_share)
                self.push_log('Received a copy of SK shares.')

                if (
                    len(self._seed_shares) + len(self._sk_shares) == user_2_num
                    and all(len(shares) == len(self._users_3) - 1  # except the sender itself
                            for shares in self._seed_shares.values())
                    and all(len(shares) == len(self._users_3)
                            for shares in self._sk_shares.values())
                ):
                    break

            elif isinstance(_event, CheckinEvent):
                self._handle_check_in(_event)

    def _aggregate_results(self, accum_result: Dict[str, torch.Tensor], result_count: int):
        """Unmask and aggregate results."""
        self.push_log('Begin to aggregate and update parameters.')
        seed_map = self._decrypt_seeds()
        self.push_log(f'Decrypted {len(seed_map)} seeds.')
        sk_map = self._decrypt_sks()
        self.push_log(f'Decrypted {len(sk_map)} sks.')
        accum_result = self._unmask_state_dict(state_dict=accum_result,
                                               seed_map=seed_map,
                                               sk_map=sk_map)

        for _key in accum_result.keys():
            if accum_result[_key].dtype in (
                torch.uint8, torch.int8, torch.int16, torch.int32, torch.int64
            ):
                logger.warn(f'average a int value may lose precision: {_key=}')
                accum_result[_key].div_(result_count, rounding_mode='trunc')
            else:
                accum_result[_key].div_(result_count)
        self.load_state_dict(accum_result)
        self.push_log('Obtained a new version of parameters.')

    def _decrypt_seeds(self) -> Dict[str, bytes]:
        assert (
            self._users_3 and len(self._users_3) >= self._t
        ), f'too few user_3: {len(self._users_3)}'
        assert (
            self._seed_shares and len(self._seed_shares) == len(self._users_3)
        ), f'not enough seed shares for user_3s: {len(self._seed_shares)}/{len(self._users_3)}'

        seed_map: Dict[str, bytes] = {}
        secret_share = SecretShare(self._t)
        for _user in self._users_3:
            share_set = set(self._seed_shares.get(_user))
            if not share_set or len(share_set) < self._t:
                raise AggregationError(f'not enough seed shares for {_user}: {share_set}')
            seed_map[_user] = secret_share.resolve_shares(list(share_set))
        return seed_map

    def _decrypt_sks(self) -> Dict[str, bytes]:
        lost_ones = list(set(_user.source_id for _user in self._users_2)
                         - set(self._users_3))
        if not lost_ones:
            return {}

        assert (
            self._sk_shares and len(self._sk_shares) == len(lost_ones)
        ), f'not enough sk shares for lost users: {len(self._sk_shares)}/{len(lost_ones)}'

        sk_map: Dict[str, bytes] = {}
        secret_share = SecretShare(self._t)
        for _user in lost_ones:
            share_set = set(self._sk_shares.get(_user))
            if not share_set or len(share_set) < self._t:
                raise AggregationError(f'not enough sk shares for {_user}: {share_set}')
            logger.debug(f'{list(share_set)=}')
            sk_map[_user] = secret_share.resolve_shares(list(share_set))
        return sk_map

    def _unmask_state_dict(self,
                           state_dict: Dict[str, torch.Tensor],
                           seed_map: Dict[str, bytes],
                           sk_map: Dict[str, bytes]) -> Dict[str, torch.Tensor]:
        assert (
            state_dict and isinstance(state_dict, dict)
            and all(
                _key
                and _value is not None
                and isinstance(_key, str)
                and isinstance(_value, torch.Tensor)
                for _key, _value in state_dict.items()
            )
        ), f'invalid state_dict data: {state_dict}'

        self.push_log('Unmasking parameters ...')
        # in order to make every calculator's PRG generates masks in a same order
        sorted_keys = sorted(state_dict)
        seed_PRG_map: Dict[str, Generator] = {
            _user: np.random.default_rng(list(_seed))
            for _user, _seed in seed_map.items()
        }

        for _key in sorted_keys:
            _val = state_dict[_key]
            for _PRG in seed_PRG_map.values():
                seed_mask = _PRG.integers(0, 2**16, size=_val.shape, dtype=np.int64)
                state_dict[_key] -= seed_mask

        users_2 = list(set(_user.source_id for _user in self._users_2))
        pk_map: Dict[str, bytes] = {
            _user: [_user_1.s_pk for _user_1 in self._users_1
                    if _user_1.peer_id == _user].pop()
            for _user in users_2
        }

        lost_users = list(set(users_2) - set(self._users_3))

        for _lost in lost_users:
            sk_PRG_map: Dict[str, Generator] = {}
            for _participant in users_2:
                if _lost == _participant:
                    continue
                cipher_key = new_shared_key(sk_map[_lost], pk_map[_participant])
                sk_PRG_map[_participant] = np.random.default_rng(list(cipher_key))
            for _key in sorted_keys:
                _val = state_dict[_key]
                for _participant in users_2:
                    _user_mask = sk_PRG_map[_participant].integers(
                        0, 2**16, size=_val.shape, dtype=np.int64
                    )
                    if _participant > _lost:
                        state_dict[_key] += _user_mask
                    else:
                        state_dict[_key] -= _user_mask

        self.push_log('Successfully Unmasked parameters.')
        return state_dict

    def _run_as_data_owner(self):
        self._wait_for_starting_round()

        self._switch_status(self._UPDATING)
        self._wait_for_updating_model()

        self._switch_status(self._ADVERTISE_KEYS)
        self._wait_for_advertising_keys()
        self._wait_for_user_1_list()

        self._switch_status(self._SHARE_KEYS)
        shared_data = self._generate_shared_data()
        self.contractor.share_keys(round=self.current_round,
                                   peer_id=self.id,
                                   list_data=shared_data,
                                   aggregator=self._aggregator)
        self.push_log('Uploaded secret shares.')
        self._wait_for_user_2_list()

        self._switch_status(self._CALCULATING)
        self.push_log('Begin to run calculation ...')
        for _ in range(self.merge_epochs):
            self.train_an_epoch()

        self.push_log('Local calculation complete.')
        self._switch_status(self._MASKED_INPUT_COLLECTION)
        masked_result = self._mask_state_dict()

        self._wait_for_uploading_model()
        buffer = io.BytesIO()
        torch.save(masked_result, buffer)
        self.push_log('Pushing local update to the aggregator ...')
        self.data_channel.send_stream(source=self.id,
                                      target=[self._aggregator],
                                      data_stream=buffer.getvalue())
        self.push_log('Successfully pushed local update to the aggregator.')

        self._switch_status(self._UNMASKING)
        self._wait_for_unmasking()

        self._switch_status(self._CLOSING_ROUND)
        self._wait_for_closing_round()
        self.push_log(f'ID: {self.id} finished training task of round {self.current_round}.')

    def _wait_for_advertising_keys(self):
        """Wait for the start signal and then advertise keys as a calculator."""
        self.push_log('Waiting for the signal to advertise keys ...')
        for _event in self.contractor.contract_events():
            if isinstance(_event, AdvertiseKeysEvent):
                if _event.round != self.current_round or self.id not in _event.calculators:
                    continue
                self._c_sk, self._c_pk = new_key_pair()
                self._s_sk, self._s_pk = new_key_pair()
                self.contractor.respond_advertise_keys(round=self.current_round,
                                                       aggregator=self._aggregator,
                                                       peer_id=self.id,
                                                       c_pk=self._c_pk,
                                                       s_pk=self._s_pk)
                self.push_log(f'ID: {self.id} has advertised keys.')
                return
            elif isinstance(_event, FinishTaskEvent):
                raise TaskComplete()
            elif isinstance(_event, ResetRoundEvent):
                raise ResetRound()

    def _wait_for_user_1_list(self):
        """Wait for receiving the list of user_1."""
        self._users_1.clear()
        self.push_log('Waiting for receiving users_1 list ...')
        for _event in self.contractor.contract_events():
            if isinstance(_event, DistributeUser1ListEvent):
                if _event.round != self.current_round:
                    continue
                self._users_1 = [_User1Info.decode(_user)
                                 for _user in _event.list_data]
                self._users_1 = [_user for _user in self._users_1
                                 if _user.peer_id != self.id]
                self.push_log(f'Received {len(self._users_1)} users_1.')

                if len(self._users_1) < self._t - 1:
                    self.push_log('Task failed because of too few users_1.')
                    raise AggregationError(f'too few users_1: {len(self._users_1)}')
                if (
                    len(set(_user.c_pk for _user in self._users_1)) < len(self._users_1)
                    or len(set(_user.s_pk for _user in self._users_1)) < len(self._users_1)
                ):
                    self.push_log('Task failed because of duplicate public keys.')
                    raise AggregationError(f'find duplicate public keys: {_event.list_data}')
                return

            elif isinstance(_event, FinishTaskEvent):
                raise TaskComplete()
            elif isinstance(_event, ResetRoundEvent):
                raise ResetRound()

    def _generate_shared_data(self) -> List[str]:
        """Generate information for sharing depending on user_1 list."""
        self.push_log('Generating secret shares ...')
        self._seed = secrets.token_bytes(32)
        secret_share = SecretShare(self._t)
        seed_shares = secret_share.make_shares(self._seed, len(self._users_1))
        s_sk_shares = secret_share.make_shares(self._s_sk, len(self._users_1))

        shared_data = []
        for _user, _seed_share, _sk_share in zip(self._users_1, seed_shares, s_sk_shares):
            _user.comm_key = new_shared_key(self._c_sk, _user.c_pk)
            cipher_seed_share = aes.encrypt(_user.comm_key, _seed_share)
            cipher_sk_share = aes.encrypt(_user.comm_key, _sk_share)
            shared_data.append(
                _User2Info(source_id=self.id,
                           target_id=_user.peer_id,
                           seed_share=cipher_seed_share,
                           sk_share=cipher_sk_share).encode()
            )
        return shared_data

    def _wait_for_user_2_list(self):
        """Wait for receiving the list of user_2."""
        self._users_2.clear()
        self.push_log('Waiting for receiving users_2 list ...')
        for _event in self.contractor.contract_events():
            if isinstance(_event, DistributeUser2ListEvent):
                if _event.round != self.current_round:
                    continue
                self._users_2 = [_User2Info.decode(_user)
                                 for _user in _event.list_data]
                self._users_2 = [_user for _user in self._users_2
                                 if _user.target_id == self.id]
                self.push_log(f'Received {len(self._users_2)} users_2.')

                if self._get_user_2_num() < self._t - 1:
                    self.push_log('Task failed because of too few users_2.')
                    raise AggregationError(f'too few users_2: {len(self._users_1)}')

                for _user in self._users_2:
                    _user.comm_key, _user.s_pk = [(_user_1.comm_key, _user_1.s_pk)
                                                  for _user_1 in self._users_1
                                                  if _user_1.peer_id == _user.source_id].pop()
                    _user.seed_share = aes.decrypt(_user.comm_key, _user.seed_share)
                    _user.sk_share = aes.decrypt(_user.comm_key, _user.sk_share)
                return

            elif isinstance(_event, FinishTaskEvent):
                raise TaskComplete()
            elif isinstance(_event, ResetRoundEvent):
                raise ResetRound()

    def _mask_state_dict(self) -> Dict[str, torch.Tensor]:
        state_dict = deepcopy(self.state_dict())
        assert (
            state_dict and isinstance(state_dict, dict)
            and all(
                _key
                and _value is not None
                and isinstance(_key, str)
                and isinstance(_value, torch.Tensor)
                for _key, _value in state_dict.items()
            )
        ), f'invalid state_dict data: {state_dict}'

        # cuda tensor cannot operate with numpy tensor or cpu tensor
        state_dict = {_key: _tensor.cpu() for _key, _tensor in state_dict.items()}

        self.push_log('Masking parameters ...')
        # in order to make every calculator's PRG generates masks in a same order
        sorted_keys = sorted(state_dict)
        seed_PRG: Generator = np.random.default_rng(list(self._seed))
        for _user in self._users_2:
            cipher_key = new_shared_key(self._s_sk, _user.s_pk)
            _user.PRG = np.random.default_rng(list(cipher_key))

        for _key in sorted_keys:
            _val = state_dict[_key]
            seed_mask = seed_PRG.integers(0, 2**16, size=_val.shape, dtype=np.int64)
            state_dict[_key] += seed_mask
            for _user in self._users_2:
                _user_mask = _user.PRG.integers(0, 2**16, size=_val.shape, dtype=np.int64)
                if _user.source_id > self.id:
                    state_dict[_key] += _user_mask
                else:
                    state_dict[_key] -= _user_mask
        self.push_log('Successfully masked parameters.')
        return state_dict

    def _wait_for_unmasking(self):
        """Wait for unmasking updates."""
        self._users_3.clear()

        self.push_log('Waiting for unmasking signal ...')
        for _event in self.contractor.contract_events():
            if isinstance(_event, StartUnmaskingEvent):
                if _event.round != self.current_round:
                    continue
                self._users_3 = _event.list_data
                self._users_3.remove(self.id)
                lost_users = list(set(_user.source_id for _user in self._users_2)
                                  - set(self._users_3))

                seed_share_list = [_SeedShareInfo(peer_id=_user.source_id,
                                                  seed_share=_user.seed_share)
                                   for _user in self._users_2
                                   if _user.source_id in self._users_3]
                self.contractor.upload_seed_shares(
                    round=self.current_round,
                    list_data=[_info.encode() for _info in seed_share_list],
                    aggregator=self._aggregator
                )

                sk_share_list = [_SKShareInfo(peer_id=_user.source_id,
                                              sk_share=_user.sk_share)
                                 for _user in self._users_2
                                 if _user.source_id in lost_users]
                self.contractor.upload_sk_shares(
                    round=self.current_round,
                    list_data=[_info.encode() for _info in sk_share_list],
                    aggregator=self._aggregator
                )
                self.push_log('Secret shares uploaded.')

                return

            elif isinstance(_event, FinishTaskEvent):
                raise TaskComplete()
            elif isinstance(_event, ResetRoundEvent):
                raise ResetRound()
