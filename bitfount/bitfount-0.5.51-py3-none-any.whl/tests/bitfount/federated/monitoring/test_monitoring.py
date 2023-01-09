"""Tests for the monitor and decorator modules."""
from datetime import datetime, timezone
from itertools import chain
import random
from typing import Dict, Optional, Type, Union
from unittest.mock import Mock, create_autospec

from _pytest.logging import LogCaptureFixture
import pytest
from pytest import fixture
from pytest_mock import MockerFixture
from requests import HTTPError, RequestException

from bitfount import BitfountHub
from bitfount.federated.monitoring import (
    AdditionalMonitorMessageTypes,
    ExistingMonitorModuleError,
    MonitorRecordPrivacy,
    NoMonitorModuleError,
    ProgressCounterDict,
    monitor,
)
from bitfount.federated.monitoring.decorators import task_status
from bitfount.federated.monitoring.monitor import (
    _MONITOR_MODULE_LOCK,
    _get_task_monitor,
    _MonitorModule,
    _MonitorPostContent,
    _set_task_monitor,
    _unset_task_monitor,
    task_config_update,
    task_monitor_context,
    task_status_update,
)
from bitfount.federated.transport.message_service import _BitfountMessageType
from bitfount.hub.types import _MonitorPostJSON
from bitfount.types import _JSONDict
from tests.utils import PytestRequest
from tests.utils.helper import get_warning_logs, unit_test


@fixture
def wrapped_monitor_lock(mocker: MockerFixture) -> Mock:
    """Wraps the monitor lock in a mock so call assertions can be made."""
    mock_lock: Mock = mocker.patch(
        "bitfount.federated.monitoring.monitor._MONITOR_MODULE_LOCK",
        wraps=_MONITOR_MODULE_LOCK,
    )
    mock_lock.__enter__ = mock_lock.acquire
    mock_lock.__exit__ = lambda *_: mock_lock.release()
    return mock_lock


@fixture
def mock_hub() -> Mock:
    """Mock BitfountHub."""
    mock_hub: Mock = create_autospec(BitfountHub, instance=True)
    return mock_hub


@fixture
def task_id() -> str:
    """Task ID."""
    return "a-task-id"


@fixture
def sender_id() -> str:
    """Sender ID."""
    return "sender-mailbox-id"


@fixture(params=(True, False), ids=("recipient_id", "no_recipient_id"))
def recipient_id(request: PytestRequest) -> Optional[str]:
    """Recipient ID or None."""
    incl_recip_id: bool = request.param
    if incl_recip_id:
        return "recipient-mailbox-id"
    else:
        return None


@fixture
def mock_monitor_module() -> Mock:
    """A mock monitor module instance."""
    mock_monitor_module: Mock = create_autospec(_MonitorModule, instance=True)
    return mock_monitor_module


@unit_test
class TestMonitorModuleManagement:
    """Tests for the global monitor module control code."""

    def test__set_task_monitor_sets_monitor(
        self,
        mock_hub: Mock,
        mocker: MockerFixture,
        recipient_id: Optional[str],
        sender_id: str,
        task_id: str,
        wrapped_monitor_lock: Mock,
    ) -> None:
        """Test global monitor module can be set properly."""
        # Ensure _MONITOR_MODULE is None at beginning
        mocker.patch("bitfount.federated.monitoring.monitor._MONITOR_MODULE", None)

        _set_task_monitor(mock_hub, task_id, sender_id, recipient_id)

        # Check lock was used
        wrapped_monitor_lock.acquire.assert_called_once()
        wrapped_monitor_lock.release.assert_called_once()

        # Check monitor module has been created with correct task ID
        assert monitor._MONITOR_MODULE is not None
        assert monitor._MONITOR_MODULE.task_id == task_id

    def test__set_task_monitor_fails_if_existing(
        self,
        mock_hub: Mock,
        mocker: MockerFixture,
        recipient_id: Optional[str],
        sender_id: str,
        task_id: str,
        wrapped_monitor_lock: Mock,
    ) -> None:
        """Test global monitor module can be set properly."""
        # Ensure _MONITOR_MODULE is NOT None at beginning
        mock_monitor = mocker.patch(
            "bitfount.federated.monitoring.monitor._MONITOR_MODULE"
        )

        with pytest.raises(ExistingMonitorModuleError):
            _set_task_monitor(mock_hub, task_id, sender_id, recipient_id)

        # Check lock was used
        wrapped_monitor_lock.acquire.assert_called_once()
        wrapped_monitor_lock.release.assert_called_once()

        # Check monitor module is unchanged
        assert monitor._MONITOR_MODULE is mock_monitor

    @pytest.mark.parametrize(
        "initial_state",
        (None, object()),
        ids=("existing_monitor", "no_existing_monitor"),
    )
    def test__unset_task_monitor_gets_existing(
        self,
        initial_state: Optional[object],
        mocker: MockerFixture,
        wrapped_monitor_lock: Mock,
    ) -> None:
        """Test global monitor module can be unset properly."""
        # Set _MONITOR_MODULE to initial state
        mocker.patch(
            "bitfount.federated.monitoring.monitor._MONITOR_MODULE", initial_state
        )

        _unset_task_monitor()

        # Check lock was used
        wrapped_monitor_lock.acquire.assert_called_once()
        wrapped_monitor_lock.release.assert_called_once()

        # Check monitor module is removed
        assert monitor._MONITOR_MODULE is None

    def test__get_task_monitor_retrieves_monitor(
        self,
        mocker: MockerFixture,
        wrapped_monitor_lock: Mock,
    ) -> None:
        """Test existing global monitor module can be retrieved."""
        # Set _MONITOR_MODULE to mock
        mock_monitor = mocker.patch(
            "bitfount.federated.monitoring.monitor._MONITOR_MODULE"
        )

        retrieved_monitor = _get_task_monitor()

        # Check lock was used
        wrapped_monitor_lock.acquire.assert_called_once()
        wrapped_monitor_lock.release.assert_called_once()

        # Check retrieved monitor is correct monitor
        assert retrieved_monitor is mock_monitor

    def test__get_task_monitor_fails_on_no_existing_monitor(
        self,
        mocker: MockerFixture,
        wrapped_monitor_lock: Mock,
    ) -> None:
        """Test _get_task_monitor fails if no existing global monitor module."""
        # Set _MONITOR_MODULE to None
        mocker.patch("bitfount.federated.monitoring.monitor._MONITOR_MODULE", None)

        # Check error raised and refers to task_monitor_context()
        with pytest.raises(NoMonitorModuleError, match="task_monitor_context"):
            _get_task_monitor()

        # Check lock was used
        wrapped_monitor_lock.acquire.assert_called_once()
        wrapped_monitor_lock.release.assert_called_once()

    def test_task_monitor_context(
        self,
        mock_hub: Mock,
        mocker: MockerFixture,
        recipient_id: Optional[str],
        sender_id: str,
        task_id: str,
        wrapped_monitor_lock: Mock,
    ) -> None:
        """Test that the task_monitor_context correctly creates monitor context."""
        # Set _MONITOR_MODULE to None
        mocker.patch("bitfount.federated.monitoring.monitor._MONITOR_MODULE", None)

        with task_monitor_context(mock_hub, task_id, sender_id, recipient_id):
            # Check monitor exists and is for task
            assert monitor._MONITOR_MODULE is not None
            assert monitor._MONITOR_MODULE.task_id == task_id

            # Check lock was used during creation but is currently unlocked
            wrapped_monitor_lock.acquire.assert_called_once()
            wrapped_monitor_lock.acquire.reset_mock()
            wrapped_monitor_lock.release.assert_called_once()
            wrapped_monitor_lock.release.reset_mock()

        # Check monitor no longer exists
        assert monitor._MONITOR_MODULE is None

        # Check locks were used during deletion but is currently unlocked
        wrapped_monitor_lock.acquire.assert_called_once()
        wrapped_monitor_lock.release.assert_called_once()

    def test_task_monitor_context_fails_if_existing_monitor(
        self,
        mock_hub: Mock,
        mocker: MockerFixture,
        recipient_id: Optional[str],
        sender_id: str,
        task_id: str,
        wrapped_monitor_lock: Mock,
    ) -> None:
        """Test task_monitor_context fails if already in task context."""
        # Set _MONITOR_MODULE to NOT None
        mock_monitor = mocker.patch(
            "bitfount.federated.monitoring.monitor._MONITOR_MODULE"
        )

        with pytest.raises(ExistingMonitorModuleError):
            with task_monitor_context(mock_hub, task_id, sender_id, recipient_id):
                # We shouldn't reach here as it should fail when entering the
                # task monitor context
                pytest.fail("In task monitor context despite failure")

        # Check monitor is unchanged
        assert monitor._MONITOR_MODULE is mock_monitor

        # Check locks were used during attempted setting but is currently unlocked
        wrapped_monitor_lock.acquire.assert_called_once()
        wrapped_monitor_lock.release.assert_called_once()


@unit_test
class TestMonitorFunctions:
    """Test the functions that interact with the monitor module."""

    def test_task_status_update(
        self,
        mock_monitor_module: Mock,
        mocker: MockerFixture,
        wrapped_monitor_lock: Mock,
    ) -> None:
        """Test task_status_update works correctly."""
        # Patch out _get_task_monitor
        mock_get_task_monitor = mocker.patch(
            "bitfount.federated.monitoring.monitor._get_task_monitor",
            return_value=mock_monitor_module,
        )

        task_status_update(
            message="Hello World!",
            privacy=MonitorRecordPrivacy.PRIVATE,
            metadata={"meta": "data"},
            progress={"progress": {"value": 1}},
            resource_usage={"resource": 10},
        )

        # Check monitor was retrieved via approved function
        mock_get_task_monitor.assert_called_once()

        # Check locks were used correctly
        wrapped_monitor_lock.acquire.assert_called_once()
        wrapped_monitor_lock.release.assert_called_once()

        # Check sending to monitor service
        mock_monitor_module.send_to_monitor_service.assert_called_once_with(
            event_type=AdditionalMonitorMessageTypes.TASK_STATUS_UPDATE,
            message="Hello World!",
            privacy=MonitorRecordPrivacy.PRIVATE,
            metadata={"meta": "data"},
            progress={"progress": {"value": 1}},
            resource_usage={"resource": 10},
        )

    def test_task_status_update_handles_no_monitor(
        self,
        caplog: LogCaptureFixture,
        mock_monitor_module: Mock,
        mocker: MockerFixture,
        wrapped_monitor_lock: Mock,
    ) -> None:
        """Test task_status_update handles the case when no monitor exists."""
        # Patch out _get_task_monitor to raise exception because no monitor
        mock_get_task_monitor = mocker.patch(
            "bitfount.federated.monitoring.monitor._get_task_monitor",
            side_effect=NoMonitorModuleError("TEST ERROR"),
            return_value=mock_monitor_module,
        )

        task_status_update(
            message="Hello World!",
            privacy=MonitorRecordPrivacy.PRIVATE,
            metadata={"meta": "data"},
            progress={"progress": {"value": 1}},
            resource_usage={"resource": 10},
        )

        # Check monitor retrieval was attempted via approved function
        mock_get_task_monitor.assert_called_once()

        # Check locks were used correctly
        wrapped_monitor_lock.acquire.assert_called_once()
        wrapped_monitor_lock.release.assert_called_once()

        # Check sending to monitor service didn't occur because of error
        mock_monitor_module.send_to_monitor_service.assert_not_called()

        # Check warning was logged
        warning_logs = get_warning_logs(caplog)
        assert "Unable to send task status update: TEST ERROR" in warning_logs

    def test_task_config_update(
        self,
        mock_monitor_module: Mock,
        mocker: MockerFixture,
        wrapped_monitor_lock: Mock,
    ) -> None:
        """Test task_config_update works correctly."""
        # Patch out _get_task_monitor
        mock_get_task_monitor = mocker.patch(
            "bitfount.federated.monitoring.monitor._get_task_monitor",
            return_value=mock_monitor_module,
        )

        task_config_update(
            task_config={"a": "task", "config": "example"},
            privacy=MonitorRecordPrivacy.PRIVATE,
        )

        # Check monitor was retrieved via approved function
        mock_get_task_monitor.assert_called_once()

        # Check locks were used correctly
        wrapped_monitor_lock.acquire.assert_called_once()
        wrapped_monitor_lock.release.assert_called_once()

        # Check sending to monitor service
        mock_monitor_module.send_to_monitor_service.assert_called_once_with(
            event_type=AdditionalMonitorMessageTypes.TASK_CONFIG,
            metadata={"a": "task", "config": "example"},
            privacy=MonitorRecordPrivacy.PRIVATE,
        )

    def test_task_config_update_handles_no_monitor(
        self,
        caplog: LogCaptureFixture,
        mock_monitor_module: Mock,
        mocker: MockerFixture,
        wrapped_monitor_lock: Mock,
    ) -> None:
        """Test task_config_update handles the case when no monitor exists."""
        # Patch out _get_task_monitor to raise exception because no monitor
        mock_get_task_monitor = mocker.patch(
            "bitfount.federated.monitoring.monitor._get_task_monitor",
            side_effect=NoMonitorModuleError("TEST ERROR"),
            return_value=mock_monitor_module,
        )

        task_config_update(
            task_config={"a": "task", "config": "example"},
            privacy=MonitorRecordPrivacy.PRIVATE,
        )

        # Check monitor retrieval was attempted via approved function
        mock_get_task_monitor.assert_called_once()

        # Check locks were used correctly
        wrapped_monitor_lock.acquire.assert_called_once()
        wrapped_monitor_lock.release.assert_called_once()

        # Check sending to monitor service didn't occur because of error
        mock_monitor_module.send_to_monitor_service.assert_not_called()

        # Check warning was logged
        warning_logs = get_warning_logs(caplog)
        assert "Unable to send task config update: TEST ERROR" in warning_logs


@unit_test
class TestMonitorModule:
    """Tests for the actual _MonitorModule class."""

    @fixture
    def monitor_module(
        self, mock_hub: Mock, recipient_id: str, sender_id: str, task_id: str
    ) -> _MonitorModule:
        """Creates a _MonitorModule instance."""
        return _MonitorModule(
            hub=mock_hub,
            task_id=task_id,
            sender_id=sender_id,
            recipient_id=recipient_id,
        )

    @fixture
    def patch_datetime_now(self, mocker: MockerFixture) -> datetime:
        """Fix a constant datetime instance for tests."""
        current = datetime.now(timezone.utc)
        mock_datetime = mocker.patch("bitfount.federated.monitoring.monitor.datetime")
        mock_datetime.now.return_value = current
        return current

    def test_task_id_property(
        self, monitor_module: _MonitorModule, task_id: str
    ) -> None:
        """Test task_id property returns expected value."""
        assert monitor_module.task_id == task_id

    def test_send_to_monitor_service(
        self,
        mock_hub: Mock,
        monitor_module: _MonitorModule,
        patch_datetime_now: datetime,
        recipient_id: str,
        sender_id: str,
        task_id: str,
    ) -> None:
        """Test send_to_monitor_service works correctly."""
        monitor_module.send_to_monitor_service(
            event_type=AdditionalMonitorMessageTypes.TASK_STATUS_UPDATE,
            privacy=MonitorRecordPrivacy.PRIVATE,
            message="Hello, world!",
            metadata={"meta": "data"},
            progress={"progress": {"value": 1}},
            resource_usage={"resource": 10},
        )

        # Check actual call to hub
        update_json: _MonitorPostJSON = {
            "taskId": task_id,
            "senderId": sender_id,
            "timestamp": patch_datetime_now.isoformat(),
            "privacy": "PRIVATE",
            "type": "TASK_STATUS_UPDATE",
            "message": "Hello, world!",
            "metadata": {"meta": "data"},
            "progress": {"progress": {"value": 1}},
            "resourceUsage": {"resource": 10},
        }
        if recipient_id:
            update_json["recipientId"] = recipient_id
        mock_hub.send_monitor_update.assert_called_once_with(update_json)

    @pytest.mark.parametrize("api_error_cls", (HTTPError, RequestException))
    def test_send_to_monitor_service_handles_api_failure(
        self,
        api_error_cls: Type[Exception],
        caplog: LogCaptureFixture,
        mock_hub: Mock,
        monitor_module: _MonitorModule,
        patch_datetime_now: datetime,
        recipient_id: str,
        sender_id: str,
        task_id: str,
    ) -> None:
        """Test send_to_monitor_service handles error in api call.

        Shouldn't error out, should instead log exception details.
        """
        # Set error condition
        mock_hub.send_monitor_update.side_effect = api_error_cls("ERROR MESSAGE")

        monitor_module.send_to_monitor_service(
            event_type=AdditionalMonitorMessageTypes.TASK_STATUS_UPDATE,
            privacy=MonitorRecordPrivacy.PRIVATE,
            message="Hello, world!",
            metadata={"meta": "data"},
            progress={"progress": {"value": 1}},
            resource_usage={"resource": 10},
        )

        # Check logs
        warning_logs = get_warning_logs(caplog)
        assert (
            "Unable to send monitoring update of type TASK_STATUS_UPDATE;"
            " error was: ERROR MESSAGE" in warning_logs
        )


@pytest.mark.parametrize(
    "message_type",
    # Too many message types in _BitfountMessageType so just choose 5
    argvalues=(
        i
        for i in chain(
            random.sample(list(_BitfountMessageType), 5),
            AdditionalMonitorMessageTypes,
        )
    ),
    ids=lambda x: f"message_type={x.name}",
)
@pytest.mark.parametrize(
    "opt_message",
    argvalues=("Hello, world!", None),
    ids=lambda x: f"message={bool(x)}",
)
@pytest.mark.parametrize(
    "opt_metadata",
    argvalues=({"meta": "data"}, None),
    ids=lambda x: f"metadata={bool(x)}",
)
@pytest.mark.parametrize(
    "opt_progress",
    argvalues=({"progress": {"value": 1}}, None),
    ids=lambda x: f"progress={bool(x)}",
)
@pytest.mark.parametrize(
    "opt_resource_usage",
    argvalues=({"resource": 10}, None),
    ids=lambda x: f"resource={bool(x)}",
)
@pytest.mark.parametrize(
    "privacy",
    argvalues=(i for i in MonitorRecordPrivacy),
    ids=lambda x: f"privacy={x.name}",
)
@unit_test
def test_monitor_post_json_conversion(
    message_type: Union[_BitfountMessageType, AdditionalMonitorMessageTypes],
    opt_message: Optional[str],
    opt_metadata: Optional[_JSONDict],
    opt_progress: Optional[Dict[str, ProgressCounterDict]],
    opt_resource_usage: Optional[Dict[str, float]],
    privacy: MonitorRecordPrivacy,
    recipient_id: Optional[str],
    sender_id: str,
    task_id: str,
) -> None:
    """Test the .json() conversion of _MonitorPostContent."""
    now = datetime.now(timezone.utc)

    mpc = _MonitorPostContent(
        task_id=task_id,
        sender_id=sender_id,
        timestamp=now,
        privacy=privacy,
        type=message_type,
        recipient_id=recipient_id,
        message=opt_message,
        metadata=opt_metadata,
        progress=opt_progress,
        resource_usage=opt_resource_usage,
    )
    mpc_json = mpc.json()

    expected_json: _MonitorPostJSON = {
        "taskId": task_id,
        "senderId": sender_id,
        "timestamp": now.isoformat(),
        "privacy": privacy.value,
        "type": (
            message_type.value
            if isinstance(message_type, AdditionalMonitorMessageTypes)
            else message_type.name
        ),
    }
    if recipient_id:
        expected_json["recipientId"] = recipient_id
    if opt_message:
        expected_json["message"] = opt_message
    if opt_metadata:
        expected_json["metadata"] = opt_metadata
    if opt_progress:
        expected_json["progress"] = opt_progress
    if opt_resource_usage:
        expected_json["resourceUsage"] = opt_resource_usage

    assert mpc_json == expected_json


@unit_test
class TestMonitorDecorators:
    """Tests for the monitor decorator functions."""

    @task_status("status update test")
    def _simple_func(self, y: int) -> int:
        return y + 1

    def test_task_status_decorator(
        self,
        mock_monitor_module: Mock,
        mocker: MockerFixture,
        wrapped_monitor_lock: Mock,
    ) -> None:
        """Test the task_status decorator works."""
        # Patch out _get_task_monitor
        mock_get_task_monitor = mocker.patch(
            "bitfount.federated.monitoring.monitor._get_task_monitor",
            return_value=mock_monitor_module,
        )

        x = self._simple_func(1)

        # Check monitor was retrieved via approved function
        mock_get_task_monitor.assert_called_once()

        # Check locks were used correctly
        wrapped_monitor_lock.acquire.assert_called_once()
        wrapped_monitor_lock.release.assert_called_once()

        # Check sending to monitor service
        mock_monitor_module.send_to_monitor_service.assert_called_once_with(
            event_type=AdditionalMonitorMessageTypes.TASK_STATUS_UPDATE,
            message="status update test",
            privacy=MonitorRecordPrivacy.ALL_PARTICIPANTS,
            metadata=None,
            progress=None,
            resource_usage=None,
        )

        # Check function return unaffected
        assert x == 2

    def test_task_status_decorator_handles_error(
        self,
        caplog: LogCaptureFixture,
        mock_monitor_module: Mock,
        mocker: MockerFixture,
        wrapped_monitor_lock: Mock,
    ) -> None:
        """Test the task_status decorator works."""
        # Patch out _get_task_monitor
        mock_get_task_monitor = mocker.patch(
            "bitfount.federated.monitoring.monitor._get_task_monitor",
            side_effect=NoMonitorModuleError("TEST ERROR"),
            return_value=mock_monitor_module,
        )

        x = self._simple_func(1)

        # Check monitor was retrieved via approved function
        mock_get_task_monitor.assert_called_once()

        # Check locks were used correctly
        wrapped_monitor_lock.acquire.assert_called_once()
        wrapped_monitor_lock.release.assert_called_once()

        # Check sending to monitor service didn't occur because of error
        mock_monitor_module.send_to_monitor_service.assert_not_called()

        # Check warning was logged
        warning_logs = get_warning_logs(caplog)
        assert "Unable to send task status update: TEST ERROR" in warning_logs

        # Check function return unaffected
        assert x == 2
