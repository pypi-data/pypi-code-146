import unittest

from sparrow_order_lib.es.es_util.mock import ESMockDSLInterface


class _testMock(ESMockDSLInterface):

    def get_dsl(self):
        return {}


class TestESMockDSLInterface(unittest.TestCase):

    def test_es_mock_dsl_interface(self):
        self.assertTrue(issubclass(_testMock, ESMockDSLInterface))


if __name__ == '__main__':
    unittest.main()
