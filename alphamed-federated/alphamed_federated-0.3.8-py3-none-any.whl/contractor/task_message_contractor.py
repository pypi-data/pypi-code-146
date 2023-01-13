"""公共合约."""

import base64
import json
import os
import secrets
import time
from abc import ABCMeta
from dataclasses import dataclass
from datetime import datetime
from io import IOBase
from typing import Dict, List, Optional, Union, overload

import requests
from requests import Response

from .. import is_mock_mode, logger, mock_node_id
from ..mock import _get_mock_contract, _put_mock_contract
from ..utils import retry
from .common import (ContractEvent, ContractEventFactory, ContractException,
                     Contractor)
from .task_contractor import AutoTaskContractor, TaskContractor

__all__ = [
    'ApplySendingDataEvent',
    'ApplyGRPCSendingDataEvent',
    'ApplySharedFileSendingDataEvent',
    'DenySendingDataEvent',
    'AcceptSendingDataEvent',
    'AcceptGRPCSendingDataEvent',
    'AcceptSharedFileSendingDataEvent',
    'TaskMessageEventFactory',
    'TaskMessageContractor',
    'AutoTaskMessageContractor'
]


@dataclass
class ApplySendingDataEvent(ContractEvent, metaclass=ABCMeta):
    """An event of requesting sending data."""

    session_id: str
    source: str
    target: Union[str, List[str]]


@dataclass
class ApplyGRPCSendingDataEvent(ApplySendingDataEvent):
    """An event of requesting sending data by GRPC."""

    TYPE = 'apply_grpc_sending_data'

    public_key: bytes

    @classmethod
    def contract_to_event(cls, contract: dict) -> 'ApplyGRPCSendingDataEvent':
        event_type = contract.get('type')
        session_id = contract.get('session_id')
        source = contract.get('source')
        target = contract.get('target')
        base64_key = contract.get('public_key')
        assert event_type == cls.TYPE, f'合约类型错误: {event_type}'
        assert session_id and isinstance(session_id, str), f'invalid session_id: {session_id}'
        assert source and isinstance(source, str), f'invalid source: {source}'
        assert target and isinstance(session_id, str), f'invalid target: {target}'
        assert base64_key and isinstance(base64_key, str), f'invalid public_key: {base64_key}'
        public_key = base64.b64decode(base64_key.encode())
        return ApplyGRPCSendingDataEvent(session_id=session_id,
                                         source=source,
                                         target=target,
                                         public_key=public_key)


@dataclass
class ApplySharedFileSendingDataEvent(ApplySendingDataEvent):
    """An event of requesting sending data by shared file."""

    TYPE = 'apply_sf_sending_data'

    file_url: str

    @classmethod
    def contract_to_event(cls, contract: dict) -> 'ApplySharedFileSendingDataEvent':
        event_type = contract.get('type')
        session_id = contract.get('session_id')
        source = contract.get('source')
        target = contract.get('target')
        file_url = contract.get('file_url')
        assert event_type == cls.TYPE, f'合约类型错误: {event_type}'
        assert session_id and isinstance(session_id, str), f'invalid session_id: {session_id}'
        assert source and isinstance(source, str), f'invalid source: {source}'
        assert (
            target and isinstance(target, list) and all(isinstance(_id, str) for _id in target)
        ), f'invalid target: {target}'
        assert file_url and isinstance(file_url, str), f'invalid public_key: {file_url}'
        return ApplySharedFileSendingDataEvent(session_id=session_id,
                                               source=source,
                                               target=target,
                                               file_url=file_url)


@dataclass
class DenySendingDataEvent(ContractEvent):
    """An event of denying sending data."""

    TYPE = 'deny_sending_data'

    session_id: str
    rejecter: str
    cause: str = None

    @classmethod
    def contract_to_event(cls, contract: dict) -> 'DenySendingDataEvent':
        event_type = contract.get('type')
        session_id = contract.get('session_id')
        rejecter = contract.get('rejecter')
        cause = contract.get('cause')
        assert event_type == cls.TYPE, f'合约类型错误: {event_type}'
        assert session_id and isinstance(session_id, str), f'invalid session_id: {session_id}'
        assert rejecter and isinstance(rejecter, str), f'invalid rejecter: {rejecter}'
        assert not cause or isinstance(cause, str), f'invalid cause: {cause}'
        return DenySendingDataEvent(session_id=session_id, rejecter=rejecter, cause=cause)


@dataclass
class AcceptSendingDataEvent(ContractEvent, metaclass=ABCMeta):
    """A event of accepting receiving data."""

    session_id: str


@dataclass
class AcceptGRPCSendingDataEvent(AcceptSendingDataEvent):
    """A event of accepting receiving data by GRPC."""

    TYPE = 'accept_grpc_sending_data'

    public_key: bytes
    port: bytes

    @classmethod
    def contract_to_event(cls, contract: dict) -> 'AcceptGRPCSendingDataEvent':
        event_type = contract.get('type')
        session_id = contract.get('session_id')
        base64_key = contract.get('public_key')
        base64_port = contract.get('port')
        assert event_type == cls.TYPE, f'合约类型错误: {event_type}'
        assert session_id and isinstance(session_id, str), f'invalid session_id: {session_id}'
        assert base64_key and isinstance(base64_key, str), f'invalid public_key: {base64_key}'
        assert base64_port and isinstance(base64_port, str), f'invalid port: {base64_port}'
        public_key = base64.b64decode(base64_key.encode())
        port = base64.b64decode(base64_port.encode())
        return AcceptGRPCSendingDataEvent(session_id=session_id,
                                          public_key=public_key,
                                          port=port)


@dataclass
class AcceptSharedFileSendingDataEvent(AcceptSendingDataEvent):
    """A event of accepting receiving data by shared file."""

    TYPE = 'accept_sf_sending_data'

    receiver: str

    @classmethod
    def contract_to_event(cls, contract: dict) -> 'AcceptSharedFileSendingDataEvent':
        event_type = contract.get('type')
        session_id = contract.get('session_id')
        receiver = contract.get('receiver')
        assert event_type == cls.TYPE, f'合约类型错误: {event_type}'
        assert session_id and isinstance(session_id, str), f'invalid session_id: {session_id}'
        assert receiver and isinstance(receiver, str), f'invalid receiver: {receiver}'
        return AcceptSharedFileSendingDataEvent(session_id=session_id, receiver=receiver)


@dataclass
class UploadTaskAchievementEvent(ContractEvent):
    """A event of uploading task achievement materials."""

    TYPE = 'upload_task_achieve'

    model: str
    report: str = None

    @classmethod
    def contract_to_event(cls, contract: dict) -> 'UploadTaskAchievementEvent':
        event_type = contract.get('type')
        model = contract.get('model')
        report = contract.get('report')
        assert event_type == cls.TYPE, f'合约类型错误: {event_type}'
        assert model and isinstance(model, str), f'invalid model: {model}'
        assert not report or isinstance(report, str), f'invalid report: {report}'
        return UploadTaskAchievementEvent(model=model, report=report)


@dataclass
class NoticeTaskCompletionEvent(ContractEvent):
    """A event of noticing task manager that current task is complete."""

    TYPE = 'notice_task_completion'

    result: bool

    @classmethod
    def contract_to_event(cls, contract: dict) -> 'NoticeTaskCompletionEvent':
        event_type = contract.get('type')
        result = contract.get('result')
        assert event_type == cls.TYPE, f'合约类型错误: {event_type}'
        assert isinstance(result, bool), f'invalid result: {result}'
        return NoticeTaskCompletionEvent(result=result)


class TaskMessageEventFactory(ContractEventFactory):

    _CLASS_MAP: Dict[str, ContractEvent] = {
        ApplyGRPCSendingDataEvent.TYPE: ApplyGRPCSendingDataEvent,
        ApplySharedFileSendingDataEvent.TYPE: ApplySharedFileSendingDataEvent,
        DenySendingDataEvent.TYPE: DenySendingDataEvent,
        AcceptGRPCSendingDataEvent.TYPE: AcceptGRPCSendingDataEvent,
        AcceptSharedFileSendingDataEvent.TYPE: AcceptSharedFileSendingDataEvent,
        UploadTaskAchievementEvent.TYPE: UploadTaskAchievementEvent,
        NoticeTaskCompletionEvent.TYPE: NoticeTaskCompletionEvent
    }

    @classmethod
    def contract_to_event(cls, contract: dict) -> Optional[ContractEvent]:
        try:
            assert contract and isinstance(contract, dict)
            event_type = contract.get('type')
            assert event_type in cls._CLASS_MAP.keys()
            event = cls._CLASS_MAP[event_type].contract_to_event(contract)
            return event
        except AssertionError:
            logger.exception(f'invalid contract data: {contract}')
            return None


class TaskMessageContractor(Contractor):
    """公共合约."""

    _URL = 'http://federated-service:9080/fed-service/api/v2/message'

    _TASK_INSIDE = 'task_inside'
    _UPLOAD_TASK_ACHIEVE = 'task_result_upload'
    _TASK_FINISH = 'task_finish'

    _TITLE_ALL = (_TASK_INSIDE, _UPLOAD_TASK_ACHIEVE, _TASK_FINISH)

    _CHANNEL = 'federated'

    def __init__(self, task_id: str) -> None:
        super().__init__()
        self.task_id = task_id
        self._event_factory = TaskMessageEventFactory
        self._task_contractor = TaskContractor(task_id=task_id)

    def _validate_response(self, resp: Response) -> dict:
        if resp.status_code < 200 or resp.status_code >= 300:
            raise ContractException(f'failed to submit a contract: {resp}')
        resp_json: dict = resp.json()
        if not resp_json or not isinstance(resp_json, dict):
            raise ContractException(f'invalid response:\nresp: {resp}\njson: {resp_json}')
        if resp_json.get('code') != 0:
            raise ContractException(f'failed to handle a contract: {resp_json}')
        data = resp_json.get('data')
        if data is None or not isinstance(data, dict):
            raise ContractException(f'contract data error: {resp_json}')
        task_id = data.get('task_id')
        assert task_id is None or task_id == self.task_id, f'task_id dismatch: {task_id}'
        return data

    @retry(exceptions=ContractException)
    def _new_contract(self,
                      targets: List[str],
                      event: ContractEvent,
                      message_title: str = _TASK_INSIDE) -> str:
        assert targets, 'must specify the target consumers of the contract'
        assert (
            isinstance(targets, list)
            and all(_target and isinstance(_target, str) for _target in targets)
        ), f'the target consumers must be an ID list: {targets}'
        assert event, 'cannot send empty contract'
        assert (
            isinstance(event, ContractEvent)
        ), f'"event" should be a contract event object: {event}'
        assert (
            message_title and message_title in self._TITLE_ALL
        ), f'invalid message_title: {message_title}'

        event.validate()

        if is_mock_mode():
            return self._new_contract_mock(targets=targets,
                                           event=event,
                                           message_title=message_title)
        else:
            return self._new_contract_normal(targets=targets,
                                             event=event,
                                             message_title=message_title)

    def _new_contract_mock(self,
                           targets: List[str],
                           event: ContractEvent,
                           message_title: str = _TASK_INSIDE) -> str:
        content = json.dumps(event.event_to_contract(), ensure_ascii=False)
        return _put_mock_contract(targets=targets,
                                  message_title=message_title,
                                  content=content,
                                  message_time=int(datetime.now().timestamp()),
                                  channel=self._CHANNEL)

    def _new_contract_normal(self,
                             targets: List[str],
                             event: ContractEvent,
                             message_title: str = _TASK_INSIDE) -> str:
        url = f'{self._URL}/push'
        post_data = {
            'task_id': self.task_id,
            'node_id_list': targets,
            'message_title': message_title,
            'message_content': event.event_to_contract(),
            'message_time': int(datetime.now().timestamp()),
            'channel': self._CHANNEL
        }
        logger.debug(f'contract content: {post_data}')
        resp = requests.post(url=url, json=post_data, headers=self._HEADERS)
        resp_data = self._validate_response(resp=resp)
        message_uuid: str = resp_data.get('message_uuid')
        assert message_uuid and isinstance(message_uuid, str), f'invalid TxId: {message_uuid}'
        logger.info(f'successfully pushed a new contract: {message_uuid=}')
        # The contract framework doesn't promise the sequence of contractors when
        # they are pushed almost at the same time, so we have to apart them a little.
        # TODO remove me when it changes.
        time.sleep(0.2)
        return message_uuid

    def _pop_contract(self) -> Optional[dict]:
        """Popup a contract for consuming if exists."""
        if is_mock_mode():
            return self._pop_contract_mock()
        else:
            return self._pop_contract_normal()

    def _pop_contract_mock(self) -> Optional[dict]:
        content = _get_mock_contract(node_id=mock_node_id(), channel=self._CHANNEL)
        return json.loads(content) if content is not None else None

    def _pop_contract_normal(self) -> Optional[dict]:
        post_data = {
            'task_id': self.task_id,
            'channel': self._CHANNEL
        }
        post_url = f'{self._URL}/pop'
        resp = requests.post(url=post_url, json=post_data, headers=self._HEADERS)
        resp_data = self._validate_response(resp=resp)
        if not resp_data:
            return None
        logger.debug(f'popped up a contract: {resp_data}')
        _content = resp_data.get('message_content')
        assert _content and isinstance(_content, dict), f'invalid contract content: {_content}'
        return _content

    @overload
    def apply_sending_data(self, source: str, target: str, public_key: bytes) -> str:
        ...

    @overload
    def apply_sending_data(self, source: str, target: List[str], file_url: str) -> str:
        ...

    def apply_sending_data(self, source: str, target: Union[str, List[str]], **kwargs) -> str:
        """发送数据传输请求合约."""
        session_id = secrets.token_hex(16)
        file_url = kwargs.get('file_url')
        public_key = kwargs.get('public_key')
        if file_url:
            event = ApplySharedFileSendingDataEvent(session_id=session_id,
                                                    source=source,
                                                    target=target,
                                                    file_url=file_url)
            self._new_contract(targets=target, event=event)
        else:
            event = ApplyGRPCSendingDataEvent(session_id=session_id,
                                              source=source,
                                              target=target,
                                              public_key=public_key)
            self._new_contract(targets=[target], event=event)
        return session_id

    def deny_sending_data(self,
                          target: str,
                          session_id: str,
                          rejecter: str,
                          cause: str = None) -> None:
        """拒绝数据传输请求合约."""
        event = DenySendingDataEvent(session_id=session_id, rejecter=rejecter, cause=cause)
        self._new_contract(targets=[target], event=event)

    @overload
    def accept_sending_data(self,
                            target: str,
                            session_id: str,
                            public_key: bytes,
                            cipher_port: bytes) -> None:
        """接受数据传输请求合约.

        通过 GRPC 数据通道。

        Args:
            session_id:
                the session id of this data sending
            public_key:
                the public key of the data receiver
            cipher_port:
                the port number used for connecting, encrypted by the sender's public key
        """

    @overload
    def accept_sending_data(self, target: str, session_id: str, receiver: str) -> None:
        """接受数据传输请求合约.

        通过共享文件数据通道。

        :args
            :session_id
                the session id of this data sending
            :public_key
                the public key of the data receiver
            :cipher_port
                the port number used for connecting, encrypted by the sender's public key
        """

    def accept_sending_data(self, target: str, session_id: str, **kwargs) -> None:
        public_key = kwargs.get('public_key')
        if public_key:
            public_key = kwargs.get('public_key')
            cipher_port = kwargs.get('cipher_port')
            assert (
                public_key and isinstance(public_key, bytes)
            ), f'Invalid public key: {public_key} .'
            assert (
                cipher_port and isinstance(cipher_port, bytes)
            ), f'Invalid cipher port: {cipher_port} .'
            event = AcceptGRPCSendingDataEvent(session_id=session_id,
                                               public_key=public_key,
                                               port=cipher_port)
        else:
            receiver = kwargs.get('receiver')
            assert receiver and isinstance(receiver, str), f'Invalid receiver: {receiver} .'
            event = AcceptSharedFileSendingDataEvent(session_id=session_id, receiver=receiver)
        self._new_contract(targets=[target], event=event)

    def contract_events(self, timeout: int = 0) -> ContractEvent:
        """Return contract events iteratively.

        :args
            :timeout
                The seconds to timeout. Will never timeout if is set less or equal to 0.
        """
        if not isinstance(timeout, int) or timeout < 0:
            timeout = 0  # disable timeout
        if timeout > 0:
            start = datetime.utcnow().timestamp()
        while timeout <= 0 or datetime.utcnow().timestamp() - start < timeout:
            _contract = self._pop_contract()
            if _contract:
                event = self._event_factory.contract_to_event(contract=_contract)
                if event:
                    yield event
                else:
                    logger.warn(f'failed to parse a contract to an event: {_contract}')
            else:
                time.sleep(1)
            continue

    @retry()
    def query_address(self, target: str) -> Optional[str]:
        """Query address of the target."""
        return self._task_contractor.query_address(target=target)

    def upload_task_achivement(self,
                               aggregator: str,
                               model_file: str,
                               report_file: str = ''):
        """Upload achivement materials after a task is complete.

        :args
            :aggregator
                The ID of the aggregator.
            :model_file
                Local path of the model file.
            :report_file
                Local path of the report file.
        """
        assert aggregator and isinstance(aggregator, str), f'unknown aggregator: {aggregator}'
        assert (
            model_file and isinstance(model_file, str)
            and os.path.exists(model_file)
            and os.path.isfile(model_file)
        ), f'the model_file does not exist or can not be accessed: {model_file}'
        if report_file:
            assert (
                isinstance(report_file, str)
                and os.path.exists(report_file)
                and os.path.isfile(report_file)
            ), f'the report_file does not exist or can not be accessed: {report_file}'

        with open(model_file, 'rb') as model_fp:
            model_file_url = self.upload_file(fp=model_fp,
                                              persistent=True,
                                              upload_name=os.path.basename(model_file))
        report_file_url = ''
        if report_file:
            with open(report_file, 'rb') as report_fp:
                report_file_url = self.upload_file(fp=report_fp,
                                                   persistent=True,
                                                   upload_name=os.path.basename(report_file))

        event = UploadTaskAchievementEvent(report=report_file_url,
                                           model=model_file_url)
        TxId = self._new_contract(targets=[aggregator],
                                  event=event,
                                  message_title=self._UPLOAD_TASK_ACHIEVE)
        if not TxId:
            raise ContractException('failed to notify task completion')

    def notify_task_completion(self, result: bool):
        """Notify task manager a task is complete.

        :args
            :result
                True if successful otherwize False.
        """
        event = NoticeTaskCompletionEvent(result=result)
        TxId = self._new_contract(targets=self.EVERYONE,
                                  event=event,
                                  message_title=self._TASK_FINISH)
        if not TxId:
            raise ContractException('failed to notify task completion')

    def report_progress(self, percent: int):
        """Report training progress (percent integer value)."""
        self._task_contractor.report_progress(percent=percent)

    def query_nodes(self) -> List[str]:
        """Query all nodes in this task."""
        return self._task_contractor.query_nodes()

    @overload
    def upload_file(self, fp: str, persistent: bool = False, upload_name: str = None) -> str: ...

    @overload
    def upload_file(self, fp: IOBase, persistent: bool = False, upload_name: str = None) -> str: ...

    def upload_file(self, fp, persistent: bool = False, upload_name: str = None) -> str:
        """Upload a file to file system."""
        return self._task_contractor.upload_file(fp=fp,
                                                 upload_name=upload_name,
                                                 persistent=persistent)


class AutoTaskMessageContractor(TaskMessageContractor):
    """AutoML version of TaskMessageContractor."""

    _CHANNEL = 'automl'

    def __init__(self, task_id: str) -> None:
        super().__init__(task_id)
        self._task_contractor = AutoTaskContractor(task_id=task_id)
