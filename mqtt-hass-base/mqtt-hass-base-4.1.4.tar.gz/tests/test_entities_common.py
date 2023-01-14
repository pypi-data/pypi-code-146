"""Tests for binary sensor."""
import logging
from contextlib import AsyncExitStack
from unittest.mock import MagicMock

import pytest

import mqtt_hass_base.error
from mqtt_hass_base.entity.common import MqttEntity


class FakeEntity(MqttEntity):  # pylint: disable=abstract-method
    """Fake entity for test."""

    _component = "test_component"


class TestEntityBinarySensor:
    """Base test class."""

    mqtt_discov_topic = "discovery_root_topic"
    mqtt_data_topic = "data_root_topic"

    @pytest.mark.asyncio
    async def test_1_error(self) -> None:
        """Base error test for binary sensor."""
        with pytest.raises(mqtt_hass_base.error.MQTTHassBaseError) as excinfo:
            fake_mqtt_client = MagicMock()
            MqttEntity(
                name="test_sensor",
                unique_id="test_sensor",
                mqtt_client=fake_mqtt_client,
                mqtt_discovery_root_topic=self.mqtt_discov_topic,
                mqtt_data_root_topic=self.mqtt_data_topic,
                logger=logging.getLogger("test_logger"),
                subscriptions={},
            )
        assert excinfo.traceback[-1].name == "__init__"

    @pytest.mark.asyncio
    async def test_2_error(self) -> None:
        """Base error test for binary sensor."""
        with pytest.raises(mqtt_hass_base.error.MQTTHassBaseError) as excinfo:
            fake_mqtt_client = MagicMock()
            MqttEntity(
                name="test_sensor",
                unique_id="test_sensor",
                mqtt_client=fake_mqtt_client,
                mqtt_discovery_root_topic=self.mqtt_discov_topic,
                mqtt_data_root_topic=self.mqtt_data_topic,
                logger=logging.getLogger("test_logger"),
                device_payload={},
                subscriptions={},
            )
        assert excinfo.traceback[-1].name == "__init__"

    @pytest.mark.asyncio
    async def test_3_error(self) -> None:
        """Base error test for binary sensor."""
        fake_mqtt_client = MagicMock()
        test_ent = FakeEntity(
            name="test_sensor",
            unique_id="test_sensor",
            mqtt_client=fake_mqtt_client,
            mqtt_discovery_root_topic=self.mqtt_discov_topic,
            mqtt_data_root_topic=self.mqtt_data_topic,
            logger=logging.getLogger("test_logger"),
            device_payload={},
            subscriptions={},
        )
        with pytest.raises(NotImplementedError) as excinfo1:
            await test_ent.register()
        assert excinfo1.traceback[-1].name == "register"

        with pytest.raises(NotImplementedError) as excinfo2:
            await test_ent.send_state("ON")
        assert excinfo2.traceback[-1].name == "send_state"

        with pytest.raises(ValueError) as excinfo3:
            await test_ent.send_attributes("Bad attributes")  # type: ignore[arg-type]
        assert excinfo3.traceback[-1].name == "send_attributes"

        async def callback() -> None:
            pass

        test_ent._subscriptions = {"toto": callback}
        async with AsyncExitStack() as stack:
            with pytest.raises(NotImplementedError) as excinfo:
                await test_ent.subscribe(stack)
        assert excinfo.traceback[-1].name == "subscribe"
