from typing import Any, Optional
from unittest import TestCase

from tololib import ToloClient, ToloServer
from tololib.command import Command
from tololib.const import AromaTherapy, LampMode
from tololib.message_info import SettingsInfo, StatusInfo


class ClientClassTest(TestCase):
    def test_discovery(self) -> None:
        self._server = ToloServer("", 0)
        self._server.start()
        result = ToloClient.discover(port=self._server.get_socket_info()[1])
        self.assertEqual(len(result), 1)
        self._server.stop()


class ClientInstanceTest(TestCase):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._server: Optional[ToloServer] = None

    def setUp(self) -> None:
        self._server = ToloServer("localhost", 0)
        self._server.start()

    def tearDown(self) -> None:
        if self._server is not None:
            self._server.stop()
            self._server.join()
            self._server = None

    def _get_port(self) -> int:
        if self._server is None:
            raise RuntimeError("server not set up")

        port = self._server.get_socket_info()[1]

        if not isinstance(port, int):
            raise RuntimeError("not an int value")

        return port

    def test_get_status_info(self) -> None:
        client = ToloClient("localhost", self._get_port())
        response = client.get_status_info()
        self.assertIsInstance(response, StatusInfo)

    def test_get_settings_info(self) -> None:
        client = ToloClient("localhost", self._get_port())
        response = client.get_settings_info()
        self.assertIsInstance(response, SettingsInfo)

    def test_main_setters(self) -> None:
        client = ToloClient("localhost", self._get_port())

        response = client.set_power_on(True)
        assert response is not None
        self.assertEqual(response.command, Command.SET_POWER_ON)
        self.assertEqual(response.data, True)

        response = client.set_power_on(False)
        assert response is not None
        self.assertEqual(response.command, Command.SET_POWER_ON)
        self.assertEqual(response.data, False)

        response = client.set_fan_on(True)
        assert response is not None
        self.assertEqual(response.command, Command.SET_FAN_ON)
        self.assertEqual(response.data, True)

        response = client.set_fan_on(False)
        assert response is not None
        self.assertEqual(response.command, Command.SET_FAN_ON)
        self.assertEqual(response.data, False)

        response = client.set_aroma_therapy_on(True)
        assert response is not None
        self.assertEqual(response.command, Command.SET_AROMA_THERAPY_ON)
        self.assertEqual(response.data, True)

        response = client.set_aroma_therapy_on(False)
        assert response is not None
        self.assertEqual(response.command, Command.SET_AROMA_THERAPY_ON)
        self.assertEqual(response.data, False)

        response = client.set_lamp_on(True)
        assert response is not None
        self.assertEqual(response.command, Command.SET_LAMP_ON)
        self.assertEqual(response.data, True)

        response = client.set_lamp_on(False)
        assert response is not None
        self.assertEqual(response.command, Command.SET_LAMP_ON)
        self.assertEqual(response.data, False)

        response = client.set_sweep_on(True)
        assert response is not None
        self.assertEqual(response.command, Command.SET_SWEEP_ON)
        self.assertEqual(response.data, True)

        response = client.set_sweep_on(False)
        assert response is not None
        self.assertEqual(response.command, Command.SET_SWEEP_ON)
        self.assertEqual(response.data, False)

        response = client.set_salt_bath_on(True)
        assert response is not None
        self.assertEqual(response.command, Command.SET_SALT_BATH_ON)
        self.assertEqual(response.data, True)

        response = client.set_salt_bath_on(False)
        assert response is not None
        self.assertEqual(response.command, Command.SET_SALT_BATH_ON)
        self.assertEqual(response.data, False)

    def test_setting_setters(self) -> None:
        client = ToloClient("localhost", self._get_port())

        # target temperature
        response = client.set_target_temperature(45)
        assert response is not None
        self.assertEqual(response.command, Command.SET_TARGET_TEMPERATURE)
        self.assertEqual(response.data, 45)

        self.assertRaises(ValueError, client.set_target_temperature, 90)
        self.assertRaises(ValueError, client.set_target_temperature, -33)
        self.assertRaises(ValueError, client.set_target_temperature, None)

        # target humidity
        response = client.set_target_humidity(93)
        assert response is not None
        self.assertEqual(response.command, Command.SET_TARGET_HUMIDITY)
        self.assertEqual(response.data, 93)

        self.assertRaises(ValueError, client.set_target_humidity, -3)
        self.assertRaises(ValueError, client.set_target_humidity, 101)
        self.assertRaises(ValueError, client.set_target_humidity, None)

        # power timer
        response = client.set_power_timer(None)
        assert response is not None
        self.assertEqual(response.command, Command.SET_POWER_TIMER)
        self.assertEqual(response.data, None)

        response = client.set_power_timer(30)
        assert response is not None
        self.assertEqual(response.command, Command.SET_POWER_TIMER)
        self.assertEqual(response.data, 30)

        self.assertRaises(ValueError, client.set_power_timer, -1)
        self.assertRaises(ValueError, client.set_power_timer, 0)
        self.assertRaises(ValueError, client.set_power_timer, 61)

        # salt bath timer
        response = client.set_salt_bath_timer(None)
        assert response is not None
        self.assertEqual(response.command, Command.SET_SALT_BATH_TIMER)
        self.assertEqual(response.data, None)

        response = client.set_salt_bath_timer(30)
        assert response is not None
        self.assertEqual(response.command, Command.SET_SALT_BATH_TIMER)
        self.assertEqual(response.data, 30)

        self.assertRaises(ValueError, client.set_salt_bath_timer, 0)
        self.assertRaises(ValueError, client.set_salt_bath_timer, -1)
        self.assertRaises(ValueError, client.set_salt_bath_timer, 61)

        # aroma therapy
        for aroma_therapy in AromaTherapy:
            response = client.set_aroma_therapy(aroma_therapy)
            assert response is not None
            self.assertEqual(response.command, Command.SET_AROMA_THERAPY)
            self.assertEqual(response.data, aroma_therapy)

        self.assertRaises(ValueError, client.set_aroma_therapy, -1)
        self.assertRaises(ValueError, client.set_aroma_therapy, 2)
        self.assertRaises(ValueError, client.set_aroma_therapy, None)

        # sweep timer
        response = client.set_sweep_timer(5)
        assert response is not None
        self.assertEqual(response.command, Command.SET_SWEEP_TIMER)
        self.assertEqual(response.data, 5)

        self.assertRaises(ValueError, client.set_sweep_timer, -1)
        self.assertRaises(ValueError, client.set_sweep_timer, 9)
        self.assertRaises(ValueError, client.set_sweep_timer, None)

        # lamp mode
        for lamp_mode in LampMode:
            response = client.set_lamp_mode(lamp_mode)
            assert response is not None
            self.assertEqual(response.command, Command.SET_LAMP_MODE)
            self.assertEqual(response.data, lamp_mode)

        self.assertRaises(ValueError, client.set_lamp_mode, None)
        self.assertRaises(ValueError, client.set_lamp_mode, -1)
        self.assertRaises(ValueError, client.set_lamp_mode, 2)

        # fan timer
        response = client.set_fan_timer(30)
        assert response is not None
        self.assertEqual(response.command, Command.SET_FAN_TIMER)
        self.assertEqual(response.data, 30)

        response = client.set_fan_timer(None)
        assert response is not None
        self.assertEqual(response.command, Command.SET_FAN_TIMER)
        self.assertEqual(response.data, None)

        response = client.set_fan_timer(None)
        assert response is not None
        self.assertEqual(response.command, Command.SET_FAN_TIMER)
        self.assertEqual(response.data, None)

        self.assertRaises(ValueError, client.set_fan_timer, 0)
        self.assertRaises(ValueError, client.set_fan_timer, -1)
