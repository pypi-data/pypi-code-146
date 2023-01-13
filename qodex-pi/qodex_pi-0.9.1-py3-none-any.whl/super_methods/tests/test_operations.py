from qpi.super_methods import operations
import unittest

class OperationsTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connections_dict = {'connection1':
                                     {'subscribe': False},
                                 'connection2':
                                     {'random_key': True}}

    def test_subscribe_status_set(self):
        response = operations.set_connection_subscribe(self.connections_dict, 'connection1')
        self.assertTrue(response['status'] and self.connections_dict['connection1']['subscribe'])

    def test_hello_world(self):
        response = operations.get_hello_answer()
        self.assertTrue(response['status'] and response['info'] == 'Hello you too!')


if __name__ == '__main__':
    unittest.main()