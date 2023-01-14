"""MQTT Daemon Base."""
import asyncio
import logging
import os
import signal
import uuid
from contextlib import AsyncExitStack

import asyncio_mqtt as mqtt

from mqtt_hass_base.error import MQTTHassBaseError


class MqttClientDaemon:
    """Mqtt device base class."""

    mqtt_port: int = -1
    mqtt_client: mqtt.Client
    mqtt_discovery_root_topic: str
    mqtt_data_root_topic: str
    tasks: set[asyncio.Task[None]] = set()

    def __init__(
        self,
        name: str | None = None,
        host: str | None = None,
        port: int | None = None,
        username: str | None = None,
        password: str | None = None,
        mqtt_discovery_root_topic: str | None = None,
        mqtt_data_root_topic: str | None = None,
        log_level: str | None = None,
        first_connection_timeout: int = 10,
    ):
        """Create new MQTT daemon."""
        if name:
            self.name = name
        else:
            self.name = os.environ.get("MQTT_NAME", "mqtt-device-" + str(uuid.uuid1()))
        self.must_run = False
        # mqtt
        self.mqtt_host = host
        if port:
            self.mqtt_port = port
        self.mqtt_username = username
        self.mqtt_password = password
        self.log_level = log_level
        self._first_connection_timeout = first_connection_timeout
        # Get logger
        self.logger = self._get_logger()
        self.logger.info("Initializing...")
        self.read_base_config(mqtt_discovery_root_topic, mqtt_data_root_topic)
        self.read_config()

    def _get_logger(self) -> logging.Logger:
        """Build logger."""
        logging_level = logging.DEBUG
        logger = logging.getLogger(name=self.name)
        logger.setLevel(logging_level)
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        return logger

    def read_config(self) -> None:
        """Read configuration."""
        raise NotImplementedError

    def read_base_config(
        self,
        mqtt_discovery_root_topic: str | None,
        mqtt_data_root_topic: str | None,
    ) -> None:
        """Read base configuration from env vars."""
        if self.mqtt_username is None:
            self.mqtt_username = os.environ.get("MQTT_USERNAME", None)
        if self.mqtt_password is None:
            self.mqtt_password = os.environ.get("MQTT_PASSWORD", None)
        if self.mqtt_host is None:
            self.mqtt_host = os.environ.get("MQTT_HOST", "127.0.0.1")
        if self.mqtt_port is None or self.mqtt_port <= 0:
            try:
                self.mqtt_port = int(os.environ.get("MQTT_PORT", 1883))
            except ValueError as exp:
                self.logger.critical("Bad MQTT port")
                raise ValueError from exp
            if self.mqtt_port <= 0:
                self.logger.critical("Bad MQTT port")
                raise ValueError("Bad MQTT port")
        if mqtt_discovery_root_topic is None:
            self.mqtt_discovery_root_topic = os.environ.get(
                "MQTT_DISCOVERY_ROOT_TOPIC",
                os.environ.get("ROOT_TOPIC", "homeassistant"),
            )
        else:
            self.mqtt_discovery_root_topic = mqtt_discovery_root_topic
        if mqtt_data_root_topic is None:
            self.mqtt_data_root_topic = os.environ.get(
                "MQTT_DATA_ROOT_TOPIC", "homeassistant"
            )
        else:
            self.mqtt_data_root_topic = mqtt_data_root_topic
        if self.log_level is None:
            self.log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
        self.logger.setLevel(getattr(logging, self.log_level.upper()))

    async def _mqtt_connect(self, stack: AsyncExitStack) -> None:
        """Connecto to the MQTT server."""
        self.logger.info("Connecting to MQTT server")
        self.mqtt_client = mqtt.Client(
            hostname=str(self.mqtt_host),
            port=self.mqtt_port,
            # logger==
            keepalive=60,
            client_id=self.name,
            username=self.mqtt_username,
            password=self.mqtt_password,
        )
        self.logger.info("Reaching MQTT server")

        timeout = self._first_connection_timeout
        while not self.is_mqtt_connected and self.must_run:
            try:
                await stack.enter_async_context(self.mqtt_client)
                # Ensure we are connected
                await asyncio.sleep(0.1)
                self.logger.info("Connected to MQTT server")
                return
            except mqtt.MqttError as exp:
                self.logger.info(
                    "Waiting for the connection to the mqtt server. %s", exp
                )
                await asyncio.sleep(1)
                if timeout is not None:
                    if timeout == 0:
                        msg = "Mqtt connection timed out. Exiting..."
                        self.logger.error(msg)
                        raise MQTTHassBaseError(msg) from exp
                    timeout -= 1

    async def _init_main_loop(self, stack: AsyncExitStack) -> None:
        """Init method called just before the start of the main loop."""
        raise NotImplementedError

    @property
    def is_mqtt_connected(self) -> bool:
        """Get mqtt connection state."""
        if hasattr(self, "mqtt_client"):
            return bool(getattr(self.mqtt_client, "_client").is_connected())
        return False

    async def async_run(self) -> None:
        """Run main base loop."""
        self.logger.info("Start main process")
        self.must_run = True
        # Add signal handler
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(
            signal.SIGINT,
            lambda: asyncio.ensure_future(self._base_signal_handler("SIGINT")),
        )
        # # type: ignore[arg-type]
        # We 💛 context managers. Let's create a stack to help
        # us manage them.
        async with AsyncExitStack() as stack:
            # Keep track of the asyncio tasks that we create, so that
            # we can cancel them on exit
            stack.push_async_callback(self._cancel_tasks)
            # Connect to Mqtt
            await self._mqtt_connect(stack)

            if self.is_mqtt_connected:
                # Before main Main loop
                await self._init_main_loop(stack)

                await asyncio.gather(*self.tasks)
                # Main loop
                while self.must_run:
                    self.logger.debug("We are in the main loop")
                    await self._main_loop(stack)

                self.logger.info("Main loop stopped")
                await self._loop_stopped()
                self.logger.info("Closing MQTT client")
                await self.mqtt_client.disconnect(timeout=10)
                await self._base_on_disconnect()
            else:
                self.logger.info("Main loop never started")
                await self._loop_stopped()

    async def _main_loop(self, stack: AsyncExitStack) -> None:
        """Run main loop.

        This method is recalled at each iteration.
        """
        raise NotImplementedError

    async def _loop_stopped(self) -> None:
        """Run after main loop is stopped."""
        raise NotImplementedError

    async def _base_signal_handler(self, sig_name: str) -> None:
        """Signal handler."""
        self.logger.info("%s received", sig_name)
        self.must_run = False
        await self._signal_handler(sig_name)
        await self._cancel_tasks()
        self.logger.info("Exiting...")

    async def _signal_handler(self, sig_name: str) -> None:
        """System signal callback to handle KILLSIG."""
        raise NotImplementedError

    async def _cancel_tasks(self) -> None:
        """Cancel all the asyncio tasks."""
        for task in self.tasks:
            if task.done():
                continue
            try:
                task.cancel()
                await task
            except asyncio.CancelledError:
                pass

    async def _base_on_disconnect(self) -> None:
        """MQTT on_disconnect callback."""
        self.logger.debug("Disconnected from MQTT server successfully")

        await self._on_disconnect()
        self.logger.debug("Disconnection done")

    async def _on_disconnect(self) -> None:
        """On disconnect callback method."""
        raise NotImplementedError
