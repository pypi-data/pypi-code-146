from unittest import TestCase

from tololib.const import Calefaction, Model
from tololib.message_info import SettingsInfo, StatusInfo


class StatusInfoTest(TestCase):
    def test_init(self) -> None:
        self.assertRaises(ValueError, StatusInfo, b"foobar")

    def test_getters_setters(self) -> None:
        info = StatusInfo()

        info.power_on = True
        self.assertEqual(info.power_on, True)
        self.assertEqual(info[0], 1)

        info.power_on = False
        self.assertEqual(info.power_on, False)
        self.assertEqual(info[0], 0)

        info.current_temperature = 45
        self.assertEqual(info.current_temperature, 45)
        self.assertEqual(info[1], 45)

        info.power_timer = None
        self.assertEqual(info.power_timer, None)
        self.assertEqual(info[2], 61)

        info.power_timer = 0
        self.assertEqual(info.power_timer, 00)
        self.assertEqual(info[2], 0)

        info.power_timer = 30
        self.assertEqual(info.power_timer, 30)
        self.assertEqual(info[2], 30)

        info.aroma_therapy_on = True
        self.assertTrue(info.aroma_therapy_on)
        self.assertEqual(info[4], 1)

        info.aroma_therapy_on = False
        self.assertFalse(info.aroma_therapy_on)
        self.assertEqual(info[4], 0)

        info.sweep_on = True
        self.assertTrue(info.sweep_on)
        self.assertEqual(info[5], 1)

        info.sweep_on = False
        self.assertFalse(info.sweep_on)
        self.assertEqual(info[5], 0)

        info.lamp_on = True
        self.assertTrue(info.lamp_on)
        self.assertEqual(info[7], 1)

        info.lamp_on = False
        self.assertFalse(info.lamp_on)
        self.assertEqual(info[7], 0)

        info.water_level = 2
        self.assertEqual(info.water_level, 2)
        self.assertEqual(info.water_level_percent, 66)
        self.assertEqual(info[8], 2)

        info.fan_on = True
        self.assertTrue(info.fan_on)
        self.assertEqual(info[9], 1)

        info.fan_on = False
        self.assertFalse(info.fan_on)
        self.assertEqual(info[9], 0)

        info.fan_timer = None
        self.assertIsNone(info.fan_timer)
        self.assertEqual(info[10], 61)

        info.fan_timer = 30
        self.assertEqual(info.fan_timer, 30)
        self.assertEqual(info[10], 30)

        info.fan_timer = 0
        self.assertEqual(info.fan_timer, 0)
        self.assertEqual(info[10], 0)

        info.current_humidity = 95
        self.assertEqual(info.current_humidity, 95)
        self.assertEqual(info[11], 95)

        info.tank_temperature = 23
        self.assertEqual(info.tank_temperature, 23)
        self.assertEqual(info[12], 23)

        info.model = Model.DOMESTIC
        self.assertEqual(info.model, Model.DOMESTIC)
        self.assertEqual(info[14], 0)

        info.model = Model.COMMERCIAL
        self.assertEqual(info.model, Model.COMMERCIAL)
        self.assertEqual(info[14], 1)

        info.salt_bath_on = True
        self.assertTrue(info.salt_bath_on)
        self.assertEqual(info[15], 1)

        info.salt_bath_on = False
        self.assertFalse(info.salt_bath_on)
        self.assertEqual(info[15], 0)

        info.salt_bath_timer = 0
        self.assertEqual(info.salt_bath_timer, 0)
        self.assertEqual(info[16], 0)

        info.salt_bath_timer = 10
        self.assertEqual(info.salt_bath_timer, 10)
        self.assertEqual(info[16], 10)

    def test_flow_in_out_calefaction(self) -> None:
        info = StatusInfo()
        self.assertFalse(info.flow_in)
        self.assertFalse(info.flow_out)
        self.assertEqual(info.calefaction, 0)

        info.flow_in = True
        self.assertTrue(info.flow_in)
        self.assertFalse(info.flow_out)
        self.assertEqual(info.calefaction, 0)

        info.calefaction = Calefaction.KEEP
        self.assertTrue(info.flow_in)
        self.assertFalse(info.flow_out)
        self.assertEqual(info.calefaction, Calefaction.KEEP)

        info.flow_out = True
        self.assertTrue(info.flow_in)
        self.assertTrue(info.flow_out)
        self.assertEqual(info.calefaction, Calefaction.KEEP)

        info.calefaction = Calefaction.HEAT
        self.assertTrue(info.flow_in)
        self.assertTrue(info.flow_out)
        self.assertEqual(info.calefaction, Calefaction.HEAT)

        info.flow_in = False
        self.assertFalse(info.flow_in)
        self.assertTrue(info.flow_out)
        self.assertEqual(info.calefaction, Calefaction.HEAT)


class SettingsInfoTest(TestCase):
    def test_init(self) -> None:
        self.assertRaises(ValueError, SettingsInfo, b"foobar")

    def test_getters_setters(self) -> None:
        info = SettingsInfo()

        info.target_temperature = 42
        self.assertEqual(info.target_temperature, 42)
        self.assertEqual(info[0], 42)
