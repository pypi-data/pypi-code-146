import io
import json
import os
import shutil
from abc import abstractmethod
from tempfile import TemporaryFile
from typing import List, Set, Tuple

import torch
import torch.nn as nn
import torch.optim as optim

from .. import get_runtime_dir, logger
from ..scheduler import ConfigError, TaskComplete, TaskFailed
from .contractor import (CheckinResponseEvent, CloseRoundEvent,
                         CloseTestRoundEvent, CompleteTaskEvent, FailTaskEvent,
                         ReadyForFusionEvent, ResetRoundEvent,
                         SendFeatureGradEvent, StartRoundEvent,
                         StartTestRoundEvent, SyncStateEvent)
from .hetero_nn import HeteroNNScheduler, ResetRound
from .psi import RSAPSICollaboratorScheduler


class HeteroNNCollaboratorScheduler(HeteroNNScheduler):
    """Schedule the process of a collaborator in a hetero_nn task."""

    _WAITING_FOR_FEATUE_GRAD = 'wait_4_feature_grad'

    def __init__(self,
                 feature_key: str,
                 name: str = None,
                 schedule_timeout: int = 30,
                 is_feature_trainable: bool = True) -> None:
        """Init.

        :args
            :feature_key
                A unique key of feature used by the host to distinguish features
                from collaborators.
            :name
                Default to the task ID.
            :schedule_timeout
                Seconds to timeout for process scheduling. Takeing off timeout
                by setting its value to 0.
            :is_feature_trainable
                Decide whether or not train the feature model
        """
        super().__init__()
        self._switch_status(self._INIT)

        self.feature_key = feature_key
        self.name = name
        self.schedule_timeout = schedule_timeout
        self.is_feature_trainable = is_feature_trainable

        self._validate_config()

        self.current_round = 0

        self.host = None

        self._feature_grad: torch.Tensor = None

    def _validate_config(self):
        if not self.feature_key or not isinstance(self.feature_key, str):
            raise ConfigError('Must specify a feature_key of type string.')

    def validate_context(self):
        """Validate if the local running context is ready.

        For example: check if train and test dataset could be loaded successfully.
        """
        if self.feature_model is None:
            raise ConfigError('Failed to initialize a feature model.')
        if not isinstance(self.feature_model, nn.Module):
            err_msg = 'Support feature model of type torch.Module only.'
            err_msg += f'Got a {type(self.feature_model)} object.'
            raise ConfigError(err_msg)
        if self.feature_optimizer is None:
            raise ConfigError('Failed to initialize a feature optimizer.')
        if not isinstance(self.feature_optimizer, optim.Optimizer):
            err_msg = 'Support feature optimizer of type torch.optim.Optimizer only.'
            err_msg += f'Got a {type(self.feature_optimizer)} object.'
            raise ConfigError(err_msg)

    @abstractmethod
    def iterate_train_feature(self,
                              feature_model: nn.Module,
                              train_ids: Set[str]) -> torch.Tensor:
        """Iterate over train dataset and features a batch of data each time.

        :args
            :feature_model
                The feature model object to train & test.
            :train_ids
                The ID set of train dataset.
        """

    @abstractmethod
    def iterate_test_feature(self,
                             feature_model: nn.Module,
                             test_ids: Set[str]) -> torch.Tensor:
        """Iterate over test dataset and features a batch of data each time.

        :args
            :feature_model
                The feature model object to train & test.
            :train_ids
                The ID set of test dataset.
        """

    def _setup_context(self, id: str, task_id: str, is_initiator: bool = False):
        super()._setup_context(id=id, task_id=task_id, is_initiator=is_initiator)
        if not self.name:
            self.name = f'guest_{self.task_id}'

        self._runtime_dir = get_runtime_dir(self.task_id)
        self._context_file = os.path.join(self._runtime_dir, ".context.json")
        self._checkpoint_dir = os.path.join(self._runtime_dir, 'checkpoint')
        self._feature_ckpt_file = os.path.join(self._checkpoint_dir, "feature_model_ckp.pt")

        self.push_log(message='Begin to validate local context.')
        self.validate_context()

    def _recover_progress(self):
        if not os.path.isfile(self._context_file):
            raise TaskFailed('Failed to recover progress: missing cached context.')

        with open(self._context_file, 'r') as f:
            context_info = json.load(f)
        feature_ckpt_file = context_info.get('feature_ckpt_file')
        assert (
            feature_ckpt_file and isinstance(feature_ckpt_file, str)
        ), f'Invalid feature_ckpt_file: {feature_ckpt_file} .'
        if not os.path.isfile(feature_ckpt_file):
            raise TaskFailed('Failed to recover progress: missing checkpoint parameters.')

        self.current_round = round
        with open(feature_ckpt_file, 'rb') as f:
            state_dict = torch.load(f)
            self.feature_model.load_state_dict(state_dict)

    def _clean_progress(self):
        """Clean existing progress data."""
        shutil.rmtree(self._runtime_dir, ignore_errors=True)
        shutil.rmtree(self._result_dir, ignore_errors=True)
        os.makedirs(self._runtime_dir, exist_ok=True)
        os.makedirs(self._checkpoint_dir, exist_ok=True)
        os.makedirs(self._result_dir, exist_ok=True)

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

                    if not self._id_intersection:
                        self._switch_status(self._ID_INTERSECTION)
                        self._make_id_intersection()

                    self._switch_status(self._IN_A_ROUND)
                    self._run_a_round()
                    self._switch_status(self._READY)
                except ResetRound:
                    self.push_log('WARNING: Reset runtime context, there might be an error raised.')
                    self._switch_status(self._READY)
                    self._id_intersection = None
                    continue

        except TaskComplete:
            logger.info('Task complete')
            self._close_task(is_succ=True)

        except TaskFailed as err:
            logger.exception(err)
            self._close_task(is_succ=False)

    def _check_in(self):
        """Check in task."""
        is_checked_in = False
        # the host may be in special state so can not response
        # correctly nor in time, then retry periodically
        self.push_log('Checking in the task ...')
        while not is_checked_in:
            nonce = self.contractor.checkin(peer_id=self.id)
            logger.debug('_wait_for_check_in_response ...')
            for _event in self.contractor.contract_events(timeout=self.schedule_timeout):
                if isinstance(_event, CheckinResponseEvent):
                    if _event.nonce != nonce:
                        continue
                    self.current_round = _event.round
                    self.host = _event.host
                    is_checked_in = True
                    break

                elif isinstance(_event, FailTaskEvent):
                    raise TaskFailed('Aborted by host.')

        self.push_log(f'Node {self.id} have taken part in the task.')

    def _sync_state(self):
        """Synchronize state before each round, so it's easier to manage the process.

        As a partner, synchronizes state and gives a response.
        """
        self.push_log('Waiting for synchronizing state with the host ...')
        for _event in self.contractor.contract_events():
            if isinstance(_event, SyncStateEvent):
                self.current_round = _event.round
                self.contractor.respond_sync_state(round=self.current_round,
                                                   peer_id=self.id,
                                                   host=_event.host)
                self.push_log('Successfully synchronized state with the host.')
                return
            elif isinstance(_event, FailTaskEvent):
                raise TaskFailed('Aborted by host.')
            elif isinstance(_event, CompleteTaskEvent):
                raise TaskComplete()
            elif isinstance(_event, ResetRoundEvent):
                raise ResetRound()

        self.push_log(f'Successfully synchronized state in round {self.current_round}')

    def _make_id_intersection(self) -> List[str]:
        """Make PSI and get id intersection for training."""
        local_ids = self.load_local_ids()
        psi_scheduler = RSAPSICollaboratorScheduler(
            task_id=self.task_id,
            collaborator_id=self.id,
            ids=local_ids,
            contractor=self.contractor
        )
        self._id_intersection = psi_scheduler.collaborate_intersection()

    def _run_a_round(self):
        self._wait_for_starting_round()
        self.feature_model.train()
        for _batch_features in self.iterate_train_feature(self.feature_model, self.train_ids):
            self.push_log('Featured a batch of data.')
            self._switch_status(self._PROJECTING)
            self._local_features = _batch_features
            self._send_feature()

            self._switch_status(self._WAITING_FOR_FEATUE_GRAD)
            self._wait_for_feature_grad()
            self._switch_status(self._UPDATING)
            self.feature_optimizer.zero_grad()
            self._local_features.backward(self._feature_grad)
            self.feature_optimizer.step()

        self._switch_status(self._PERSISTING)
        self._save_model()
        self._save_runtime_context()

        self._switch_status(self._TESTING)
        self._wait_for_testing_round()

        self._switch_status(self._CLOSING_ROUND)
        self._wait_for_closing_round()

        self.push_log(f'ID: {self.id} finished training task of round {self.current_round}.')

    def _wait_for_starting_round(self):
        """Wait for starting a new round of training ..."""
        self.push_log(f'Waiting for training of round {self.current_round} begin ...')
        for _event in self.contractor.contract_events():
            if isinstance(_event, StartRoundEvent):
                assert (
                    _event.round == self.current_round
                ), f'Lost synchronization, host: {_event.round}; local: {self.current_round}.'
                self.push_log(f'Training of round {self.current_round} begins.')
                return
            elif isinstance(_event, FailTaskEvent):
                raise TaskFailed('Aborted by host.')
            elif isinstance(_event, ResetRoundEvent):
                raise ResetRound()

    def _send_feature(self):
        """Send local features of a batch of data to the host."""
        self.push_log('Waiting for sending features ...')
        for _event in self.contractor.contract_events():
            if isinstance(_event, ReadyForFusionEvent):
                assert (
                    _event.round == self.current_round
                ), f'Lost synchronization, host: {_event.round}; local: {self.current_round}.'
                break
            elif isinstance(_event, FailTaskEvent):
                raise TaskFailed('Aborted by host.')
            elif isinstance(_event, ResetRoundEvent):
                raise ResetRound()

        self.push_log('Begin to send features.')
        with TemporaryFile() as tf:
            torch.save({self.feature_key: self._local_features}, tf)
            tf.seek(0)
            self.data_channel.send_stream(source=self.id,
                                          target=self.host,
                                          data_stream=tf.read())
        self.push_log('Sending features complete.')

    def _wait_for_feature_grad(self):
        """Wait for cipher grad of feature model output."""
        self.push_log('Waiting for cipher grad of feature model output ...')
        for _event in self.contractor.contract_events():
            if isinstance(_event, SendFeatureGradEvent):
                stream = self.data_channel.receive_stream(apply_event=_event,
                                                          receiver=self.id)
                buffer = io.BytesIO(stream)
                self._feature_grad = torch.load(buffer)
                break
            elif isinstance(_event, ResetRoundEvent):
                raise ResetRound()
        self.push_log('Received and decrypted cipher grad of feature model output.')

    def _save_model(self):
        """Save latest model state."""
        with open(self._feature_ckpt_file, 'wb') as f:
            torch.save(self.feature_model.state_dict(), f)
        self.push_log('Saved latest parameters locally.')

    def _save_runtime_context(self):
        """Save runtime context information in case of restoring."""
        context_info = {
            'feature_ckpt_file': self._feature_ckpt_file
        }
        with open(self._context_file, 'w') as f:
            f.write(json.dumps(context_info, ensure_ascii=False))
        self.push_log('Saved latest runtime context.')

    def _wait_for_testing_round(self):
        """Wait for handle a round of testing."""
        self.push_log('Waiting for start a round of testing ...')
        for _event in self.contractor.contract_events():
            if isinstance(_event, StartTestRoundEvent):
                assert (
                    _event.round == self.current_round
                ), f'Lost synchronization, host: {_event.round}; local: {self.current_round}.'

                self.feature_model.eval()
                features = {
                    self.feature_key: list(self.iterate_test_feature(self.feature_model,
                                                                     self.test_ids))
                }
                with TemporaryFile() as tf:
                    torch.save(features, tf)
                    tf.seek(0)
                    self.data_channel.send_stream(source=self.id,
                                                  target=self.host,
                                                  data_stream=tf.read())
                self.push_log('Sent all batches of feature to the host.')

            elif isinstance(_event, CloseTestRoundEvent):
                self.push_log('Skipped or closed a round of testing.')
                return
            elif isinstance(_event, FailTaskEvent):
                raise TaskFailed('Aborted by host.')
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
            elif isinstance(_event, CompleteTaskEvent):
                raise TaskComplete()
            elif isinstance(_event, ResetRoundEvent):
                raise ResetRound()

    def _close_task(self, is_succ: bool = True):
        """Close the task and upload the final parameters."""
        self.push_log(f'Closing task {self.task_id} ...')

        self._switch_status(self._FINISHING)
        if is_succ:
            model_file_path = self._prepare_task_output()
            self.contractor.upload_task_achivement(aggregator=self.id,
                                                   model_file=model_file_path)
            self.contractor.notify_collaborator_complete(peer_id=self.id, host=self.host)
            self.push_log(f'Task {self.task_id} complete. Byebye!')
        else:
            self.push_log(f'Task {self.task_id} failed. Byebye!')

    def _prepare_task_output(self) -> Tuple[str, str]:
        """Generate final output files of the task.

        :return
            Local paths of the model file.
        """
        self.push_log('Generating task achievement files ...')

        # torch.jit doesn't work with a TemporaryFile
        feature_model_file = os.path.join(self._result_dir,
                                          f'feature_model_{self.feature_key}.pt')
        with open(feature_model_file, 'wb') as f:
            torch.save(self.feature_model.state_dict(), f)
        model_file_path = os.path.abspath(feature_model_file)

        self.push_log('Task achievement files are ready.')
        return model_file_path
