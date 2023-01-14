"""Tests for MqttClientDaemon."""
import asyncio
import copy
import os
import signal
import threading
import traceback
from collections.abc import AsyncGenerator, Callable
from contextlib import AsyncExitStack
from typing import Any

import asyncio_mqtt as mqtt
import paho.mqtt.client as paho
import pytest

from mqtt_hass_base.daemon import MqttClientDaemon
from mqtt_hass_base.error import MQTTHassBaseError


class FakeDaemon(MqttClientDaemon):  # pylint: disable=abstract-method
    """Base Mqtt daemon."""


def catch_thread_exceptions(test_func: Callable) -> Callable:  # type: ignore[type-arg]
    """Catch all thread exceptions."""

    async def wrapper(  # type: ignore[no-untyped-def]
        test_obj, *args, **kwargs
    ) -> Callable:  # type: ignore[type-arg]
        def excepthook(exp_args: BaseException) -> None:
            test_obj.thread_except.append(exp_args)

        threading.excepthook = excepthook  # type: ignore[assignment]
        return await test_func(test_obj, *args, **kwargs)  # type: ignore[no-any-return]

    return wrapper


def get_fakedaemon(
    test_step: int, *args: Any, custom_methods: Any = None, **kwargs: Any
) -> FakeDaemon:
    """Create FakeDaemon object.

    Set correct methods and create FakeDaemon object
    """
    test_fake_daemon = copy.copy(FakeDaemon)
    if test_step >= 3:

        def _read_config(  # pylint: disable=unused-argument
            self: MqttClientDaemon,
        ) -> None:
            pass

        test_fake_daemon.read_config = _read_config  # type: ignore[assignment]

    if test_step >= 6:

        async def _init_main_loop(  # pylint: disable=unused-argument,invalid-name
            self: MqttClientDaemon,
            stack: AsyncExitStack,
        ) -> None:
            await asyncio.sleep(1)

        test_fake_daemon._init_main_loop = _init_main_loop  # type: ignore[assignment]
    if test_step >= 7:

        async def on_messages(
            messages: AsyncGenerator[  # pylint: disable=unused-argument
                paho.MQTTMessage, None
            ]
        ) -> None:
            pass

        async def _main_loop(  # pylint: disable=unused-argument,invalid-name
            self: MqttClientDaemon,
            stack: AsyncExitStack,
        ) -> None:
            messages = await stack.enter_async_context(
                self.mqtt_client.unfiltered_messages()
            )

            task = asyncio.create_task(on_messages(messages))
            self.tasks.add(task)
            await asyncio.gather(*self.tasks)
            self.must_run = False

        test_fake_daemon._main_loop = _main_loop  # type: ignore[assignment]
    if test_step >= 8:

        async def _loop_stopped(  # pylint: disable=unused-argument,invalid-name
            self: MqttClientDaemon,
        ) -> None:
            pass

        test_fake_daemon._loop_stopped = _loop_stopped  # type: ignore[assignment]
    if test_step >= 9:

        async def _on_disconnect(  # pylint: disable=unused-argument,invalid-name
            self: MqttClientDaemon,
        ) -> None:
            pass

        test_fake_daemon._on_disconnect = _on_disconnect  # type: ignore[assignment]

    if test_step >= 13:

        async def _signal_handler(  # pylint: disable=unused-argument,invalid-name
            self: MqttClientDaemon, sig_name: str
        ) -> None:
            pass

        test_fake_daemon._signal_handler = _signal_handler  # type: ignore[assignment]

    if custom_methods:
        for method_name, func in custom_methods.items():
            setattr(test_fake_daemon, method_name, func)

    return test_fake_daemon(*args, **kwargs)


class TestBase:
    """Base test class."""

    def setup_method(self) -> None:
        """Prepare tests."""
        if "MQTT_PORT" in os.environ:
            del os.environ["MQTT_PORT"]
        if "MQTT_USERNAME" in os.environ:
            del os.environ["MQTT_USERNAME"]
        if "MQTT_PASSWORD" in os.environ:
            del os.environ["MQTT_PASSWORD"]
        self.thread_except: list[BaseException] = []

    def _check_frame_exceptions(
        self, excepted_exptypes: list[type], excepted_expnames: list[str]
    ) -> None:
        """Check if there is exceptions in the collected thread frames."""
        if not excepted_exptypes and not excepted_expnames:
            assert not self.thread_except
            return
        assert len(self.thread_except) == len(excepted_exptypes)
        assert len(self.thread_except) == len(excepted_expnames)
        for index, exp in enumerate(self.thread_except):
            assert exp.exc_type == excepted_exptypes[index]  # type: ignore[attr-defined]
            frames = traceback.extract_tb(exp.exc_traceback)  # type: ignore[attr-defined]
            assert frames[-1].name == excepted_expnames[index]

    @pytest.mark.asyncio
    async def test_1_error__bad_port(self) -> None:
        """Error test 1 for mqttdaemon."""
        os.environ["MQTT_PORT"] = "BAD_PORT"
        with pytest.raises(ValueError) as excinfo:
            # Missing read_config
            MqttClientDaemon(name="fake_daemon")
        assert excinfo.traceback[-1].name == "read_base_config"

        os.environ["MQTT_PORT"] = "-100"
        with pytest.raises(ValueError) as excinfo:
            # Missing read_config
            MqttClientDaemon(name="fake_daemon")
        assert excinfo.traceback[-1].name == "read_base_config"

    @pytest.mark.asyncio
    async def test_2_error__missing__read_config(
        self,
    ) -> None:
        """Error test 1 for mqttdaemon."""
        with pytest.raises(NotImplementedError) as excinfo:
            # Missing read_config
            MqttClientDaemon(name="fake_daemon")

        assert excinfo.traceback[-1].name == "read_config"

    @pytest.mark.asyncio
    @catch_thread_exceptions
    async def test_4_error__connection_timeout(self) -> None:
        """Error test 2 for mqttdaemon."""
        os.environ["MQTT_PORT"] = "1888"
        os.environ["MQTT_USERNAME"] = "BAD_USERNAME"
        os.environ["MQTT_PASSWORD"] = "BAD_PASSWORD"

        test_mqtt_daemon = get_fakedaemon(test_step=4, first_connection_timeout=3)
        assert test_mqtt_daemon.is_mqtt_connected is False
        with pytest.raises(MQTTHassBaseError) as excinfo:
            await test_mqtt_daemon.async_run()
        # Wait to ensure catching exception
        await asyncio.sleep(1)

        assert excinfo.traceback[-1].name == "_mqtt_connect"

        self._check_frame_exceptions([], [])

    @pytest.mark.asyncio
    @catch_thread_exceptions
    async def test_5_error__missing__init_main_loop(
        self,
    ) -> None:
        """Error test with _init_main_loop missing."""
        test_mqtt_daemon = get_fakedaemon(test_step=5)

        with pytest.raises(NotImplementedError) as excinfo:
            await test_mqtt_daemon.async_run()
        # Wait to ensure catching exception
        await asyncio.sleep(1)

        assert excinfo.traceback[-1].name == "_init_main_loop"

    @pytest.mark.asyncio
    @catch_thread_exceptions
    async def test_6_error__missing__main_loop(self) -> None:
        """Error test 2 for mqttdaemon."""
        test_mqtt_daemon = get_fakedaemon(test_step=6)

        with pytest.raises(NotImplementedError) as excinfo:
            await test_mqtt_daemon.async_run()
        # Wait to ensure catching exception
        await asyncio.sleep(1)

        assert excinfo.traceback[-1].name == "_main_loop"

        self._check_frame_exceptions([], [])

    @pytest.mark.asyncio
    @catch_thread_exceptions
    async def test_7_error__missing__loop_stopped(self) -> None:
        """Error test 2 for mqttdaemon."""
        test_mqtt_daemon = get_fakedaemon(test_step=7)
        with pytest.raises(NotImplementedError) as excinfo:
            await test_mqtt_daemon.async_run()
        # Wait to ensure catching exception
        await asyncio.sleep(1)

        assert excinfo.traceback[-1].name == "_loop_stopped"

        self._check_frame_exceptions([], [])

    @pytest.mark.asyncio
    @catch_thread_exceptions
    async def test_8_error__missing__on_disconnect(self) -> None:
        """Error test 2 for mqttdaemon."""
        test_mqtt_daemon = get_fakedaemon(test_step=8)
        with pytest.raises(NotImplementedError) as excinfo:
            await test_mqtt_daemon.async_run()
        # Wait to ensure catching exception
        await asyncio.sleep(1)

        # missing on_disconnect
        assert excinfo.traceback[-1].name == "_on_disconnect"

    @pytest.mark.asyncio
    @catch_thread_exceptions
    async def test_9_happy_path(self) -> None:
        """Happy path test with auto stopping main loop."""
        test_mqtt_daemon = get_fakedaemon(test_step=9)
        await test_mqtt_daemon.async_run()
        # Wait to ensure catching exception
        await asyncio.sleep(1)

        self._check_frame_exceptions([], [])

    @pytest.mark.asyncio
    @catch_thread_exceptions
    async def test_12_error__missing__on_signal_handler(
        self,
    ) -> None:
        """Error test 3 for mqttdaemon."""
        test_mqtt_daemon = get_fakedaemon(test_step=12)

        with pytest.raises(NotImplementedError) as excinfo:
            await test_mqtt_daemon._signal_handler("SIGINT")

        assert excinfo.traceback[-1].name == "_signal_handler"

    @pytest.mark.asyncio
    @catch_thread_exceptions
    async def test_13_happy_path_with_sigint(self) -> None:
        """Happy path test with SIGINT to stop main loop."""
        test_mqtt_daemon = get_fakedaemon(
            test_step=13,
            port=1883,
            mqtt_discovery_root_topic="/home-assistant",
            mqtt_data_root_topic="/hydroqc",
        )

        await test_mqtt_daemon.async_run()
        # Wait to ensure catching exception
        await asyncio.sleep(1)

        # orig = signal.signal(signal.SIGTERM, signal.getsignal(signal.SIGINT))
        pid = os.getpid()

        os.kill(pid, signal.SIGINT)
        await asyncio.sleep(3)

        self._check_frame_exceptions([], [])

    @pytest.mark.asyncio
    async def test_14_error_nerver_start(
        self,
    ) -> None:
        """Error test 3 for mqttdaemon."""

        async def _mqtt_connect(
            stack: AsyncExitStack,  # pylint: disable=unused-argument
        ) -> None:
            pass

        test_mqtt_daemon = get_fakedaemon(test_step=14)
        test_mqtt_daemon._mqtt_connect = _mqtt_connect  # type: ignore

        await test_mqtt_daemon.async_run()
        # Wait to ensure catching exception
        await asyncio.sleep(1)

        self._check_frame_exceptions([], [])

    @pytest.mark.asyncio
    @catch_thread_exceptions
    async def test_15_error__mqtt_client_disconnected(
        self,
    ) -> None:
        """Error test 3 for mqttdaemon."""

        async def main_loop(
            self: MqttClientDaemon,
            stack: AsyncExitStack,  # pylint: disable=unused-argument
        ) -> None:
            self.must_run = False
            await self.mqtt_client.disconnect()
            await self.mqtt_client.publish("toto", "toto")

        test_mqtt_daemon = get_fakedaemon(
            test_step=15, custom_methods={"_main_loop": main_loop}
        )

        with pytest.raises(mqtt.MqttCodeError) as excinfo:
            await test_mqtt_daemon.async_run()

        # Wait to ensure catching exception
        assert excinfo.traceback[-1].name == "publish"
        self._check_frame_exceptions([], [])
