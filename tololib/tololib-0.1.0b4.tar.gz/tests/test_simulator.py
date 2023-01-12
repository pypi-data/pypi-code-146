from unittest import TestCase

from tololib import Simulator, ToloServer
from tololib.const import AromaTherapy, Calefaction, LampMode, Model


class SimulatorTest(TestCase):
    def test_init_settings(self) -> None:
        server = ToloServer("localhost", 0)
        simulator = Simulator(server)
        simulator._init_settings()

        self.assertEqual(simulator.settings.target_temperature, 43)
        self.assertEqual(simulator.settings.target_humidity, 95)
        self.assertEqual(simulator.settings.power_timer, 45)
        self.assertEqual(simulator.settings.salt_bath_timer, 30)
        self.assertEqual(simulator.settings.aroma_therapy, AromaTherapy.B)
        self.assertEqual(simulator.settings.sweep_timer, 0)
        self.assertEqual(simulator.settings.lamp_mode, LampMode.MANUAL)
        self.assertEqual(simulator.settings.fan_timer, 5)

    def test_init_status(self) -> None:
        server = ToloServer("localhost", 0)
        simulator = Simulator(server)
        simulator._init_settings()
        simulator._init_status()

        self.assertEqual(simulator.status.power_on, False)
        self.assertEqual(simulator.status.current_temperature, 17)
        self.assertEqual(simulator.status.power_timer, None)
        self.assertEqual(simulator.status.flow_in, False)
        self.assertEqual(simulator.status.flow_out, True)
        self.assertEqual(simulator.status.calefaction, Calefaction.INACTIVE)
        self.assertEqual(simulator.status.aroma_therapy_on, False)
        self.assertEqual(simulator.status.sweep_on, False)
        # TODO add descaling
        self.assertEqual(simulator.status.lamp_on, False)
        self.assertEqual(simulator.status.water_level, 0)
        self.assertEqual(simulator.status.fan_on, False)
        self.assertEqual(simulator.status.fan_timer, None)
        self.assertEqual(simulator.status.current_humidity, 52)
        self.assertEqual(simulator.status.tank_temperature, 17)
        self.assertEqual(simulator.status.model, Model.DOMESTIC)
        self.assertEqual(simulator.status.salt_bath_on, False)
        self.assertEqual(simulator.status.salt_bath_timer, 0)

    def test_update_status(self) -> None:
        pass  # TODO write tests
