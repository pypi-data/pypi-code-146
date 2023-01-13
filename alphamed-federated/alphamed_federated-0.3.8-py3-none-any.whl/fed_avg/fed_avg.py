"""FedAvg scheduler."""

import io
import json
import os
import random
import shutil
import sys
import traceback
from abc import ABCMeta, abstractmethod
from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict, List, Tuple
from zipfile import ZipFile

import torch
from torch.nn import Module
from torch.optim import Optimizer
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

from .. import get_result_dir, get_runtime_dir, logger
from ..data_channel import SharedFileDataChannel
from ..perf_bench import SimplePerfBench, SimplePerfBenchResult
from ..scheduler import ConfigError, Scheduler, TaskComplete, TaskFailed
from .contractor import (BenchmarkDoneEvent, CheckinEvent,
                         CheckinResponseEvent, CloseAggregatorElectionEvent,
                         CloseRoundEvent, DistributeParametersEvent,
                         FedAvgContractor, FinishTaskEvent,
                         ReadyForAggregationEvent, ResetRoundEvent,
                         StartAggregatorElectionEvent, StartRoundEvent,
                         SynchronizeAggregatorContextEvent, SyncStateEvent,
                         SyncStateResponseEvent, UploadTrainingResultsEvent)

__all__ = [
    'FedAvgScheduler',
    'FedSGDScheduler'
]


class AggregationError(Exception):
    ...


class SkipRound(Exception):
    ...


class ResetRound(Exception):
    ...


LEN_BYTES = 4
INT_BYTES_ORDER = 'big'


@dataclass
class AggregatorSyncData:

    state_dict: bytes
    participants: List[str]

    def to_bytes(self) -> bytes:
        assert self.state_dict, f'must specify state_dict: {self.state_dict}'
        assert self.participants, f'must specify participants: {self.participants}'

        data_stream = b''
        state_dict_len = len(self.state_dict)
        data_stream += state_dict_len.to_bytes(LEN_BYTES, INT_BYTES_ORDER)
        data_stream += self.state_dict
        data_stream += json.dumps(self.participants).encode()
        return data_stream

    @classmethod
    def from_bytes(self, data: bytes) -> 'AggregatorSyncData':
        assert data and isinstance(data, bytes), f'invalid data: {data}'

        archor = 0
        state_dict_len = int.from_bytes(data[archor:(archor + LEN_BYTES)],
                                        INT_BYTES_ORDER)
        archor += LEN_BYTES
        state_dict = data[archor:(archor + state_dict_len)]
        archor += state_dict_len
        participants_bytes = data[archor:]
        participants = json.loads(participants_bytes.decode())
        return AggregatorSyncData(state_dict=state_dict, participants=participants)


class FedAvgScheduler(Scheduler, metaclass=ABCMeta):
    """Implementation of FedAvg."""

    _INIT = 'init'
    _GETHORING = 'gethering'
    _READY = 'ready'
    _SYNCHRONIZING = 'synchronizing'
    _ELECTING = 'electing'
    _BENCHMARKING = 'benchmarking'
    _SELECTING = 'selecting'
    _IN_A_ROUND = 'in_a_round'
    _UPDATING = 'updating'
    _CALCULATING = 'calculating'
    _WAIT_FOR_AGGR = 'wait_4_aggr'
    _AGGREGATING = 'aggregating'
    _PERSISTING = 'persisting'
    _CLOSING_ROUND = 'closing_round'
    _FINISHING = 'finishing'

    def __init__(self,
                 min_clients: int,
                 max_clients: int,
                 name: str = None,
                 max_rounds: int = 0,
                 merge_epochs: int = 1,
                 calculation_timeout: int = 300,
                 perf_bench_timeout: int = 30,
                 schedule_timeout: int = 30,
                 log_rounds: int = 0,
                 is_centralized: bool = True,
                 involve_aggregator: bool = False):
        """Init.

        Args:
            min_clients:
                Minimal number of calculators for each round.
            max_clients:
                Maximal number of calculators for each round.
            name:
                Default to the task ID.
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
            involve_aggregator:
                If set true, the aggregator should have its local data and conduct
                training other than merely schedule and aggregate.
        """
        super().__init__()
        self._switch_status(self._INIT)

        self.name = name
        self.min_clients = min_clients
        self.max_clients = max_clients
        self.max_rounds = max_rounds
        self.merge_epochs = merge_epochs
        self.calculation_timeout = calculation_timeout
        self.perf_bench_timeout = perf_bench_timeout
        self.schedule_timeout = schedule_timeout
        self.log_rounds = log_rounds
        self.is_centralized = is_centralized
        self.involve_aggregator = involve_aggregator

        self._validate_config()
        self.current_round = 1

        self._participants: List[str] = []
        self._calculators: List[str] = []
        self._perf_benchmarks: List[SimplePerfBenchResult] = []
        self._latest_aggregators: Deque[str] = deque()
        self._is_gathering_complete = False

        self._example_inputs = None

    def _validate_config(self):
        if self.min_clients > self.max_clients:
            raise ConfigError('min_clients must not exceed max_clients')
        if self.merge_epochs <= 0:
            raise ConfigError('merge_epochs must be a positive integer')

    @abstractmethod
    def build_model(self) -> Module:
        """Return a model object which will be used for training."""

    @property
    def model(self) -> Module:
        """Get the model object which is used for training."""
        if not hasattr(self, '_model'):
            self._model = self.build_model()
        return self._model

    @abstractmethod
    def build_optimizer(self, model: Module) -> Optimizer:
        """Return a optimizer object which will be used for training.

        Args:
            model:
                The model object which is used for training.
        """

    @property
    def optimizer(self) -> Optimizer:
        """Get the optimizer object which is used for training."""
        if not hasattr(self, '_optimizer'):
            self._optimizer = self.build_optimizer(model=self.model)
        return self._optimizer

    @abstractmethod
    def build_train_dataloader(self) -> DataLoader:
        """Define the training dataloader.

        You can transform the dataset, do some preprocess to the dataset.

        Return:
            training dataloader
        """

    @property
    def train_loader(self) -> DataLoader:
        """Get the training dataloader object."""
        if not hasattr(self, '_train_loader'):
            self._train_loader = self.build_train_dataloader()
        return self._train_loader

    def build_validation_dataloader(self) -> DataLoader:
        """Define the validation dataloader if needed.

        You can transform the dataset, do some preprocess to the dataset.

        Return:
            validation dataloader
        """
        raise NotImplementedError()

    @property
    def validation_loader(self) -> DataLoader:
        """Get the validation dataloader object if needed."""
        if not hasattr(self, '_validation_loader'):
            self._validation_loader = self.build_validation_dataloader()
        return self._validation_loader

    @abstractmethod
    def build_test_dataloader(self) -> DataLoader:
        """Define the testing dataloader.

        You can transform the dataset, do some preprocess to the dataset. If you do not
        want to do testing after training, simply make it return None.

        Args:
            dataset:
                training dataset
        Return:
            testing dataloader
        """

    @property
    def test_loader(self) -> DataLoader:
        """Get the testing dataloader object."""
        if not hasattr(self, '_test_loader'):
            self._test_loader = self.build_test_dataloader()
        return self._test_loader

    @abstractmethod
    def state_dict(self) -> Dict[str, torch.Tensor]:
        """Get the params that need to train and update.

        Only the params returned by this function will be updated and saved during aggregation.

        Return:
            List[torch.Tensor], The list of model params.
        """

    @abstractmethod
    def load_state_dict(self, state_dict: Dict[str, torch.Tensor]):
        """Load the params that trained and updated.

        Only the params returned by state_dict() should be loaded by this function.
        """

    def validate_context(self):
        """Validate if the local running context is ready.

        For example: check if train and test dataset could be loaded successfully.
        """
        if self.model is None:
            raise ConfigError('Must specify a model to train')
        if not isinstance(self.model, Module):
            raise ConfigError('Support torch.Module only')
        if self.optimizer is None:
            raise ConfigError('Must specify an optimizer to train')
        if not isinstance(self.optimizer, Optimizer):
            raise ConfigError('Support torch.optim.Optimizer only')

    @abstractmethod
    def train_an_epoch(self):
        """Define the training steps in an epoch."""

    @abstractmethod
    def test(self):
        """Define the testing steps.

        If you do not want to do testing after training, simply make it pass.
        """

    def is_task_finished(self) -> bool:
        """By default true if reach the max rounds configured."""
        return self._is_reach_max_rounds()

    def _run(self, id: str, task_id: str, is_initiator: bool = False, recover: bool = False):
        self._setup_context(id=id, task_id=task_id, is_initiator=is_initiator)
        self.push_log(message='Local context is ready.')
        try:
            if self.is_aggregator and recover:
                self._recover_progress()
            else:
                self._clean_progress()
            self._launch_process()
        except Exception:
            err_stack = ''.join(traceback.format_exception(*sys.exc_info()))
            self.push_log(err_stack)

    def _setup_context(self, id: str, task_id: str, is_initiator: bool = False):
        assert id, 'must specify a unique id for every participant'
        assert task_id, 'must specify a task_id for every participant'

        self.id = id
        self.task_id = task_id
        if not self.name:
            self.name = self.task_id
        self._runtime_dir = get_runtime_dir(self.task_id)
        self._context_file = os.path.join(self._runtime_dir, ".context.json")
        self._checkpoint_dir = os.path.join(self._runtime_dir, 'checkpoint')
        self._ckpt_file = os.path.join(self._checkpoint_dir, "model_ckpt.pt")
        self._result_dir = get_result_dir(self.task_id)
        self._log_dir = os.path.join(self._result_dir, 'tb_logs')
        self.tb_writer = SummaryWriter(log_dir=self._log_dir)

        self.is_initiator = is_initiator
        self.is_aggregator = self.is_initiator
        if self.involve_aggregator:
            self._participants.append(self.id)

        self.contractor = FedAvgContractor(task_id=task_id)
        self.data_channel = SharedFileDataChannel(self.contractor)
        self.model
        self.optimizer

        self.push_log(message='Begin to validate local context.')
        self.validate_context()

        def save_example_inputs(module, input, output):
            if self._example_inputs is None:
                self._example_inputs = input
        self.model.register_forward_hook(save_example_inputs)

    def _recover_progress(self):
        """Try to recover and continue from last running."""
        if not os.path.isfile(self._context_file):
            raise TaskFailed('Failed to recover progress: missing cached context.')

        with open(self._context_file, 'r') as f:
            context_info = json.load(f)
        round = context_info.get('round')
        ckpt_file = context_info.get('ckpt_file')
        assert round and isinstance(round, int) and round > 0, f'Invalid round: {round} .'
        assert ckpt_file and isinstance(ckpt_file, str), f'Invalid ckpt_file: {ckpt_file} .'
        if not os.path.isfile(ckpt_file):
            raise TaskFailed('Failed to recover progress: missing checkpoint parameters.')

        self.current_round = round
        with open(ckpt_file, 'rb') as f:
            state_dict = torch.load(f)
            self.load_state_dict(state_dict)

    def _clean_progress(self):
        """Clean existing progress data."""
        shutil.rmtree(self._runtime_dir, ignore_errors=True)
        shutil.rmtree(self._result_dir, ignore_errors=True)
        os.makedirs(self._runtime_dir, exist_ok=True)
        os.makedirs(self._checkpoint_dir, exist_ok=True)
        os.makedirs(self._result_dir, exist_ok=True)
        os.makedirs(self._log_dir, exist_ok=True)

    def push_log(self, message: str):
        """Push a running log message to the task manager."""
        super().push_log(message=message)
        logger.info(message)

    def _launch_process(self):
        try:
            assert self.status == self._INIT, 'must begin from initial status'
            self.push_log(f'Node {self.id} is up.')

            self._switch_status(self._GETHORING)
            self._check_in()

            self._switch_status(self._READY)
            while self.status == self._READY:
                try:
                    self._switch_status(self._SYNCHRONIZING)
                    self._sync_state()

                    if not self.is_centralized:
                        # elect an aggregator for this round
                        self._switch_status(self._ELECTING)
                        self._elect_aggregator()

                    self._switch_status(self._IN_A_ROUND)
                    self._run_a_round()
                    self._switch_status(self._READY)
                except ResetRound:
                    self.push_log('WARNING: Reset runtime context, there might be an error raised.')
                    self._switch_status(self._READY)
                    continue

                if self.is_aggregator:
                    is_finished = self.is_task_finished()
                    self._persistent_running_context()
                    self._switch_status(self._READY)
                    self.current_round += 1
                    if is_finished:
                        self.push_log(f'Obtained the final results of task {self.task_id}')
                        self._switch_status(self._FINISHING)
                        self._close_task()

        except TaskComplete:
            logger.info('training task complete')

    def _check_in(self):
        """Check in task and get ready.

        As an initiator (and default the first aggregator), records each participants
        and launches election or training process accordingly.
        As a participant, checkins and gets ready for election or training.
        """
        if self.is_initiator:
            self.push_log('Waiting for participants taking part in ...')
            self._wait_for_gathering()
            self._is_gathering_complete = True
        else:
            is_checked_in = False
            # the aggregator may be in special state so can not response
            # correctly nor in time, then retry periodically
            self.push_log('Checking in the task ...')
            while not is_checked_in:
                is_checked_in = self._check_in_task()
            self.push_log(f'Node {self.id} have taken part in the task.')

    def _sync_state(self):
        """Synchronize state before each round, so it's easier to manage the process.

        As an aggregator, iterates round, broadcasts and resets context of the new round.
        As a participant, synchronizes state and gives a response.
        """
        self.push_log('Synchronizing round state ...')
        if self.is_aggregator:
            self._calculators.clear()
            if self.involve_aggregator:
                self._calculators.append(self.id)
            self.push_log(f'Initiate state synchronization of round {self.current_round}.')
            self.contractor.sync_state(round=self.current_round, aggregator=self.id)
            self._wait_for_sync_response()
            if len(self._calculators) < self.min_clients:
                self.push_log('Task failed because of too few participants.')
                raise AggregationError(f'too few participants: {len(self._calculators)}')
        else:
            self._wait_for_sync_state()
        self.push_log(f'Successfully synchronized state in round {self.current_round}')

    def _elect_aggregator(self):
        """Elect a new aggregator for a round.

        As an aggregator, initiates election and selects an appropriate one as
        the new aggregator depending on benchmark result, then transfers context
        data to the new aggregator.
        As a participant, performes benchmark and reports the result. If is selected
        as the new aggregator, receives context data and takes over management.
        """
        self.push_log('Electing a new aggregator.')
        if self.is_aggregator:
            self.contractor.start_aggregator_election(round=self.current_round)
            new_aggregator = self._wait_for_benchmark()
            self.contractor.close_aggregator_election(round=self.current_round)
            # it's possible the all benchmark failed
            self.is_aggregator = new_aggregator == self.id
        else:
            self.push_log('Waiting for aggregator election begin ...')
            self._wait_for_electing()
            self.push_log('Waiting for aggregator election result ...')
            self._wait_for_election_result()
        self.push_log('Aggregator election complete.')

    def _run_a_round(self):
        """Perform a round of FedAvg calculation.

        As an aggregator, selects a part of participants as actual calculators
        in the round, distributes latest parameters to them, collects update and
        makes aggregation.
        As a participant, if is selected as a calculator, calculates and uploads
        parameter update.
        """
        if self.is_aggregator:
            try:
                self._run_as_aggregator()
            except AggregationError as err:
                err_stack = ''.join(traceback.format_exception(*sys.exc_info()))
                self.push_log(err_stack)
                self.contractor.reset_round()
                raise ResetRound(err)
        else:
            self._run_as_data_owner()

    def _close_task(self, is_succ: bool = True):
        """Close the FedAvg calculation.

        As an aggregator, broadcasts the finish task event to all participants,
        uploads the final parameters and tells L1 task manager the task is complete.
        As a participant, do nothing.
        """
        self.push_log(f'Closing task {self.task_id} ...')
        if self.is_aggregator:
            self._switch_status(self._FINISHING)
            self.contractor.finish_task()
            report_file_path, model_file_path = self._prepare_task_output()
            self.contractor.upload_task_achivement(aggregator=self.contractor.EVERYONE[0],
                                                   report_file=report_file_path,
                                                   model_file=model_file_path)
            self.contractor.notify_task_completion(result=True)
        self.push_log(f'Task {self.task_id} closed. Byebye!')

    def _wait_for_gathering(self):
        """Wait for participants gethering."""
        logger.debug('_wait_for_gathering ...')
        for _event in self.contractor.contract_events():
            if isinstance(_event, CheckinEvent):
                self._handle_check_in(_event)
                if len(self._participants) >= self.min_clients:
                    break
        # it takes seconds to send a response and to consume it in the remote side,
        # meanwhile, more check in events may arrive soonly. So keep looking for a while.
        countdown = 10
        for _event in self.contractor.contract_events(timeout=countdown):
            if isinstance(_event, CheckinEvent):
                self._handle_check_in(_event)

    def _handle_check_in(self, _event: CheckinEvent):
        if _event.peer_id not in self._participants:
            self._participants.append(_event.peer_id)
            self.push_log(f'Welcome a new participant ID: {_event.peer_id}.')
            self.push_log(f'There are {len(self._participants)} participants now.')
        self.contractor.respond_check_in(round=self.current_round,
                                         aggregator=self.id,
                                         nonce=_event.nonce,
                                         requester_id=_event.peer_id)
        if self._is_gathering_complete:
            self.contractor.sync_state(round=self.current_round, aggregator=self.id)

    def _wait_for_sync_response(self):
        """Wait for participants' synchronizing state response."""
        self.push_log('Waiting for synchronization responses ...')
        for _event in self.contractor.contract_events(timeout=0):
            if isinstance(_event, SyncStateResponseEvent):
                if _event.round != self.current_round:
                    continue
                self._calculators.append(_event.peer_id)
                self.push_log(f'Successfully synchronized state with ID: {_event.peer_id}.')
                self.push_log(f'Successfully synchronized with {len(self._calculators)} participants.')
                if len(self._calculators) == len(self._participants):
                    return

            elif isinstance(_event, CheckinEvent):
                self._handle_check_in(_event)

    def _check_in_task(self) -> bool:
        """Try to check in the task."""
        nonce = self.contractor.checkin(peer_id=self.id)
        return self._wait_for_check_in_response(nonce=nonce,
                                                timeout=self.schedule_timeout)

    def _wait_for_check_in_response(self, nonce: str, timeout: int = 0) -> bool:
        """Wait for checkin response.

        Return True if received response successfully otherwise False.
        """
        logger.debug('_wait_for_check_in_response ...')
        for _event in self.contractor.contract_events(timeout=timeout):
            if isinstance(_event, CheckinResponseEvent):
                if _event.nonce != nonce:
                    continue
                self.current_round = _event.round
                return True
            elif isinstance(_event, FinishTaskEvent):
                raise TaskComplete()
        return False

    def _wait_for_sync_state(self, timeout: int = 0) -> bool:
        """Wait for synchronising latest task state.

        Return True if synchronising successfully otherwise False.
        """
        self.push_log('Waiting for synchronizing state with the aggregator ...')
        for _event in self.contractor.contract_events(timeout=timeout):
            if isinstance(_event, SyncStateEvent):
                self.current_round = _event.round
                self.contractor.respond_sync_state(round=self.current_round,
                                                   peer_id=self.id,
                                                   aggregator=_event.aggregator)
                self.push_log('Successfully synchronized state with the aggregator.')
                return
            elif isinstance(_event, FinishTaskEvent):
                raise TaskComplete()

    def _wait_for_benchmark(self) -> str:
        """Wait for someone complete benchmark task.

        Return:
            the ID of the newly selected aggregator
        """
        self.push_log('Waiting for benchmark results ...')
        new_aggregator = self.id
        self._calculators.clear()
        if self.involve_aggregator:
            self._calculators.append(self.id)
        for _event in self.contractor.contract_events(timeout=SimplePerfBench.TIMEOUT):
            if isinstance(_event, BenchmarkDoneEvent):
                if _event.round != self.current_round:
                    continue

                if _event.peer_id not in self._calculators:
                    self._calculators.append(_event.peer_id)
                    self.push_log(f'Received benchmark result from ID: {_event.peer_id}.')

                # the first one arrived
                if new_aggregator == self.id:
                    new_aggregator = _event.peer_id
                    self.push_log(f'ID: {new_aggregator} is elected as the new aggregator.')
                    self.push_log('Begin to synchronize context with the new aggregatro.')

                    buffer = io.BytesIO()
                    torch.save(self.state_dict(), buffer)
                    # if self.involve_aggregator is set false, add self into participants list
                    if not self.involve_aggregator:
                        self._participants.append(self.id)
                    sync_data = AggregatorSyncData(state_dict=buffer.getvalue(),
                                                   participants=self._participants)
                    self.data_channel.send_stream(source=self.id,
                                                  target=[_event.peer_id],
                                                  data_stream=sync_data.to_bytes())
                    self.push_log('Successfully synchronized context with the new aggregatro.')

                if len(self._calculators) == len(self._participants):  # all finished
                    break

            elif isinstance(_event, CheckinEvent):
                self._handle_check_in(_event)

        # it's possible that there is no one complete benchmarking
        return new_aggregator

    def _wait_for_electing(self):
        """Try for being an aggregator."""
        logger.debug('_wait_for_electing ...')
        for _event in self.contractor.contract_events():
            if isinstance(_event, StartAggregatorElectionEvent):
                if _event.round != self.current_round:
                    continue
                SimplePerfBench().run()
                self.contractor.report_benchmark_done(round=self.current_round, peer_id=self.id)
                return
            elif isinstance(_event, FinishTaskEvent):
                raise TaskComplete()

    def _wait_for_election_result(self):
        logger.debug('_wait_for_election_result ...')
        for _event in self.contractor.contract_events():
            if isinstance(_event, SynchronizeAggregatorContextEvent):
                # is selected as the next aggregator and synchronise aggregator data
                self.push_log('Current node is selected as the new aggregator.')
                self.push_log('Begin to synchronize context with the original aggregator.')
                data_stream = self.data_channel.receive_stream(apply_event=_event,
                                                               receiver=self.id)
                sync_data = AggregatorSyncData.from_bytes(data=data_stream)
                buffer = io.BytesIO(sync_data.state_dict)
                _new_state_dict = torch.load(buffer)
                self.load_state_dict(state_dict=_new_state_dict)
                self._participants = sync_data.participants
                if self.id in self._participants and not self.involve_aggregator:
                    self._participants.remove(self.id)
                self.is_aggregator = True
                self.push_log('Successfully synchronized context with the original aggregator.')

            elif isinstance(_event, CloseAggregatorElectionEvent):
                if _event.round != self.current_round:
                    continue
                else:
                    return

            elif isinstance(_event, FinishTaskEvent):
                raise TaskComplete()

    def _run_as_aggregator(self):
        self._start_round()
        self._distribute_model()

        self._process_aggregation()

        self._check_and_run_test()
        self._close_round()

    def _close_round(self):
        """Close current round when finished."""
        self._switch_status(self._CLOSING_ROUND)
        self.contractor.close_round(round=self.current_round)
        self.push_log(f'The training of Round {self.current_round} complete.')

    def _start_round(self):
        """Prepare and start calculation of a round."""
        self.push_log(f'Begin the training of round {self.current_round}.')
        self._switch_status(self._SELECTING)
        self.push_log('Select calculators of current round.')
        self._select_calculators()
        self.push_log(f'Calculators of round {self.current_round} are: {self._calculators}.')
        self.contractor.start_round(round=self.current_round,
                                    calculators=self._calculators,
                                    aggregator=self.id)
        self.push_log(f'Calculation of round {self.current_round} is started.')

    def _distribute_model(self):
        buffer = io.BytesIO()
        torch.save(self.state_dict(), buffer)
        self.push_log('Distributing parameters ...')
        results = {_target: False for _target in self._calculators}
        targets = [_target for _target in results.keys() if _target != self.id]
        accept_list = self.data_channel.send_stream(source=self.id,
                                                    target=targets,
                                                    data_stream=buffer.getvalue())
        self.push_log(f'Successfully distributed parameters to: {accept_list}')
        if len(targets) != len(accept_list):
            reject_list = [_target for _target in targets if _target not in accept_list]
            self.push_log(f'Failed to distribute parameters to: {reject_list}')
        results.update({_target: True for _target in accept_list})

        _min_clients = (self.min_clients) - 1 if self.involve_aggregator else self.min_clients
        if sum(results.values()) < _min_clients:
            self.push_log('Task failed because of too few calculators getting ready')
            raise AggregationError(f'Too few calculators getting ready: {results}.')
        self.push_log(f'Distributed parameters to {sum(results.values())} calculators.')

    def _process_aggregation(self):
        """Process aggregation depending on specific algorithm."""
        self._switch_status(self._WAIT_FOR_AGGR)
        self.contractor.notify_ready_for_aggregation(round=self.current_round)
        self.push_log('Now waiting for executing calculation ...')
        accum_result, result_count = self._wait_for_calculation()
        if result_count < self.min_clients:
            self.push_log('Task failed because of too few calculation results gathered.')
            raise AggregationError(f'Too few results gathered: {result_count} copies.')
        self.push_log(f'Received {result_count} copies of calculation results.')

        self._switch_status(self._AGGREGATING)
        self.push_log('Begin to aggregate and update parameters.')
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

    def _persistent_running_context(self):
        self._switch_status(self._PERSISTING)
        self._save_model()
        self._save_runtime_context()

    def _check_and_run_test(self):
        """Run test if match configured conditions."""
        if (
            self.current_round == 1
            or (self.log_rounds > 0 and self.current_round % self.log_rounds == 0)
            or self.current_round == self.max_rounds
        ):
            self.push_log('Begin to make a model test.')
            self.test()
            self.push_log('Finished a round of test.')

    def _wait_for_calculation(self) -> Tuple[Dict[str, torch.Tensor], int]:
        """Wait for every calculator finish its task or timeout."""
        result_count = 0
        if self.id in self._calculators:
            self._execute_training()
            result_count += 1
            self.push_log(f'The aggregator ID: {self.id} obtained its calculation results.')
            accum_result = self.state_dict()
        else:
            accum_result = self.state_dict()
            for _param in accum_result.values():
                if isinstance(_param, torch.Tensor):
                    _param.zero_()

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
                result_count += 1
                self.push_log(f'Received calculation results from ID: {_event.source}')
                if result_count >= len(self._calculators):
                    return accum_result, result_count

            elif isinstance(_event, CheckinEvent):
                self._handle_check_in(_event)

        return accum_result, result_count

    def _is_reach_max_rounds(self) -> bool:
        """Is the max rounds configuration reached."""
        return self.current_round >= self.max_rounds

    def _select_calculators(self):
        """Select calculators of a round."""
        if len(self._participants) < self.min_clients:
            raise AggregationError(f'too few participants: {len(self._participants)}')

        if len(self._calculators) < self.min_clients:
            candidates = [_peer for _peer in self._participants
                          if _peer not in self._calculators]
            random.shuffle(candidates)
            self._calculators.extend(candidates[:self.min_clients - len(self._calculators)])

        elif len(self._calculators) > self.max_clients:
            random.shuffle(self._calculators)
            self._calculators = self._calculators[:self.max_clients]

    def _save_model(self):
        """Save latest model state."""
        with open(self._ckpt_file, 'wb') as f:
            torch.save(self.state_dict(), f)
        self.push_log('Saved latest parameters locally.')

    def _save_runtime_context(self):
        """Save runtime context information in case of restoring."""
        context_info = {
            'round': self.current_round,
            'ckpt_file': self._ckpt_file
        }
        with open(self._context_file, 'w') as f:
            f.write(json.dumps(context_info, ensure_ascii=False))
        self.push_log('Saved latest runtime context.')

    def _prepare_task_output(self) -> Tuple[str, str]:
        """Generate final output files of the task.

        Return:
            Local paths of the report file and model file.
        """
        self.push_log('Uploading task achievement and closing task ...')

        # TODO remove metrics_files later
        metrics_files = []
        for _name, _metrics in self._metrics_bucket.items():
            _file = f'{os.path.join(self._result_dir, _name)}.csv'
            _metrics.to_csv(_file)
            metrics_files.append(_file)
        report_file = os.path.join(self._result_dir, "report.zip")
        with ZipFile(report_file, 'w') as report_zip:
            for _file in metrics_files:
                report_zip.write(_file, os.path.basename(_file))
            for path, _, filenames in os.walk(self._log_dir):
                rel_dir = os.path.relpath(path=path, start=self._result_dir)
                rel_dir = rel_dir.lstrip('.')  # ./file => file
                for _file in filenames:
                    rel_path = os.path.join(rel_dir, _file)
                    report_zip.write(os.path.join(path, _file), rel_path)
        report_file_path = os.path.abspath(report_file)

        model_file = os.path.join(self._result_dir, "model.pt")
        with open(model_file, 'wb') as f:
            torch.save(self.state_dict(), f)
        model_file_path = os.path.abspath(model_file)

        self.push_log('Task achievement files are ready.')
        return report_file_path, model_file_path

    def _run_as_data_owner(self):
        try:
            self._wait_for_starting_round()
            self._switch_status(self._UPDATING)
            self._wait_for_updating_model()
            self._save_model()
            self._switch_status(self._CALCULATING)
            self.push_log('Begin to run calculation ...')
            self._execute_training()
            self.push_log('Local calculation complete.')

            self._wait_for_uploading_model()
            buffer = io.BytesIO()
            torch.save(self.state_dict(), buffer)
            self.push_log('Pushing local update to the aggregator ...')
            self.data_channel.send_stream(source=self.id,
                                          target=[self._aggregator],
                                          data_stream=buffer.getvalue())
            self.push_log('Successfully pushed local update to the aggregator.')
            self._switch_status(self._CLOSING_ROUND)
            self._wait_for_closing_round()
        except SkipRound:
            pass

        self.push_log(f'ID: {self.id} finished training task of round {self.current_round}.')

    def _execute_training(self):
        for _ in range(self.merge_epochs):
            self.train_an_epoch()

    def _wait_for_starting_round(self):
        """Wait for starting a new round of training."""
        self.push_log(f'Waiting for training of round {self.current_round} begin ...')
        for _event in self.contractor.contract_events():
            if isinstance(_event, StartRoundEvent):
                if _event.round != self.current_round:
                    continue
                if self.id not in _event.calculators:
                    raise SkipRound()
                self._aggregator = _event.aggregator
                self.push_log(f'Training of round {self.current_round} begins.')
                return
            elif isinstance(_event, FinishTaskEvent):
                raise TaskComplete()
            elif isinstance(_event, ResetRoundEvent):
                raise ResetRound()

    def _wait_for_updating_model(self):
        """Wait for receiving latest parameters from aggregator."""
        self.push_log('Waiting for receiving latest parameters from the aggregator ...')
        for _event in self.contractor.contract_events():
            if isinstance(_event, DistributeParametersEvent):
                if self.id not in _event.target:
                    continue
                parameters = self.data_channel.receive_stream(apply_event=_event,
                                                              receiver=self.id)
                buffer = io.BytesIO(parameters)
                new_state_dict = torch.load(buffer)
                self.load_state_dict(new_state_dict)
                self.push_log('Successfully received latest parameters.')
                return
            elif isinstance(_event, FinishTaskEvent):
                raise TaskComplete()
            elif isinstance(_event, ResetRoundEvent):
                raise ResetRound()

    def _wait_for_uploading_model(self):
        """Wait for uploading trained parameters to aggregator."""
        self.push_log('Waiting for aggregation begin ...')
        for _event in self.contractor.contract_events():
            if isinstance(_event, ReadyForAggregationEvent):
                if _event.round != self.current_round:
                    continue
                return
            elif isinstance(_event, FinishTaskEvent):
                raise TaskComplete()
            elif isinstance(_event, ResetRoundEvent):
                raise ResetRound()

    def _wait_for_closing_round(self):
        """Wait for closing current round of training."""
        self.push_log(f'Waiting for closing signal of training round {self.current_round} ...')
        for _event in self.contractor.contract_events():
            if isinstance(_event, CloseRoundEvent):
                if _event.round != self.current_round:
                    continue
                return
            elif isinstance(_event, FinishTaskEvent):
                raise TaskComplete()
            elif isinstance(_event, ResetRoundEvent):
                raise ResetRound()


class FedSGDScheduler(FedAvgScheduler):
    """Implementation of FedSGD."""

    def __init__(self,
                 min_clients: int,
                 name: str = None,
                 max_rounds: int = 0,
                 calculation_timeout: int = 300,
                 perf_bench_timeout: int = 30,
                 schedule_timeout: int = 30,
                 log_rounds: int = 0,
                 is_centralized: bool = True):
        """Init.

        By now, IterableDataset with no length is not supported.

        Args:
            min_clients:
                Minimal number of calculators for each round.
            name:
                Default to the task ID.
            max_rounds:
                Maximal number of training rounds.
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
                         max_clients=sys.maxsize,
                         name=name,
                         max_rounds=max_rounds,
                         merge_epochs=1,
                         calculation_timeout=calculation_timeout,
                         perf_bench_timeout=perf_bench_timeout,
                         schedule_timeout=schedule_timeout,
                         log_rounds=log_rounds,
                         is_centralized=is_centralized)

    def _setup_context(self, id: str, task_id: str, is_initiator: bool = False):
        super()._setup_context(id=id, task_id=task_id, is_initiator=is_initiator)
        # Since build_train_dataloader is implemented by the user, and DataLoader base
        # implementation does not allow to modify batch_size after initialization,
        # there is no way to mandatorily set batch size to the correct value.
        # So a post check is used.
        self.push_log(f'train batch size = {self.train_loader.batch_size}')
        try:
            num_samples = len(self.train_loader.dataset)
            self.push_log(f'train examples = {num_samples}')
            if self.train_loader.batch_size != len(num_samples):
                raise ConfigError('batch size must be the total number of samples.')
        except TypeError:
            raise ConfigError('Does not support iterable dataset with no length.')

    def _select_calculators(self):
        """Select calculators of a round."""
        if len(self._calculators) < self.min_clients:
            raise AggregationError(f'too few calculators: {len(self._calculators)}')
