import unittest
from sensor_tracker_client import sensor_tracker_client as stc
from sensor_tracker_client.exceptions import AuthenticationError


class TestConnect(unittest.TestCase):
    def setUp(self):

        stc.HOST = 'http://127.0.0.1:8001/'
        stc.authentication.username = "xling"
        stc.authentication.password = "changeme"

    def test_url(self):
        print(stc.authentication.is_username_and_password_valid())
