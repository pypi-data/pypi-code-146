import time
import unittest
from emaux_client import pump


class PumpTestCase(unittest.TestCase):
    def test_pump(self):
        """Test pump methods"""

        _pump = pump.Pump("http://192.168.1.94")

        _pump.turn_off()
        time.sleep(1)
        data = _pump.get_data()
        self.assertFalse(data.on)

        _pump.turn_on()
        time.sleep(1)
        data = _pump.get_data()
        self.assertTrue(data.on)

        _pump.set_speed(1234)
        time.sleep(4)
        data = _pump.get_data()
        self.assertEqual(data.speed, 1234)

        _pump.set_speed(1500)


if __name__ == '__main__':
    unittest.main()
