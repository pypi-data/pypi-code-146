from qpi.main import QPI
from qdk.main import QDK
from qpi.tests.test_core import TestCore
import unittest
import threading
from wsqluse.wsqluse import Wsqluse


class MainTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        test_core = TestCore()
        sql_shell = Wsqluse('wdb', 'watchman', 'hect0r1337', '192.168.100.118')
        self.qpi_test = QPI('localhost', 1337, sql_shell=sql_shell, users_table_name='api_users',
                            user_column_name='username', core=test_core)
        self.qdk_test = QDK('localhost', 1337, 'login', 'password')
        threading.Thread(target=self.qpi_test.launch_mainloop, args=()).start()

    def test_connect_qdk(self):
        self.qdk_test.make_connection()
        response = self.qdk_test.make_auth(get_response=True)
        print("RESP", response)
        self.assertTrue(response == {'status': True, 'info': 1, 'method_str': 'auth_me'})
        self.qdk_test.sock.close()

    def test_subscribe_qdk(self):
        self.qdk_test.make_connection()
        self.qdk_test.make_auth()
        response = self.qdk_test.subscribe(get_response=True)
        self.assertTrue(response['status'] is True)
        self.qdk_test.sock.close()

    def test_execute_hello_world(self):
        self.qdk_test.make_connection()
        self.qdk_test.make_auth()
        response = self.qdk_test.execute_method('hello_world', get_response=True)
        self.assertTrue(response['status'])
        self.qdk_test.sock.close()

    def test_execute_core_method(self):
        self.qdk_test.make_connection()
        self.qdk_test.make_auth()
        new_methods = {'hello_core': {'command': 'hello_core'}}
        self.qdk_test.expand_api_methods(new_methods)
        self.qdk_test.execute_method('hello_core', get_response=True)
        self.qdk_test.sock.close()






if __name__ == '__main__':
    unittest.main()