import sys
from unittest.mock import Mock, patch

import pytest

# The default address Private Key for local networks
PRIVATE_KEY  = '0x56289e99c94b6912bfc12adc093c9b51124f0dc54ac7a766b2bc5ccf558d8027'

class MockSocket():

    def __init__(self, data):
        self.data_to_send = data
        self.received = []

    def recv(self, num_bytes: int):
        # If there is no data left, raise an exception
        if not self.data_to_send:
            raise Exception("Out of data!")

        # If we don't have enough data to satisfy, send what we have 
        if len(self.data_to_send) < num_bytes:
            data = self.data_to_send
            self.data_to_send = []
            return data

        # Send the number of bytes requested
        data = self.data_to_send[0:num_bytes]
        self.data_to_send = self.data_to_send[num_bytes:]
        return data


    def connect(self, _data):
        pass

    def send(self, data):
        self.received += data
        pass


from rebapy.client import RelayClient
from rebapy.stripped_tx import DynamicGas


@patch("socket.socket" , Mock(return_value=MockSocket(data=[])))
def test_init():
    client = RelayClient(PRIVATE_KEY)

TEST_TX = bytes([144, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 141, 185, 124, 124, 236, 226, 73, 194, 185, 139, 220, 2, 38, 204, 76, 42, 87, 191, 82, 252, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 202, 154, 59, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 132, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1, 2, 3, 4, 5, 0, 160, 114, 78, 24, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 232, 118, 72, 23, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
@patch("socket.socket" , Mock(return_value=MockSocket(data=TEST_TX)))
def test_read_tx():
    client = RelayClient(PRIVATE_KEY)
    tx = client.read_tx()

    assert tx.hash == bytes([0x00] * 32)
    assert tx.from_address  == bytes([0x8d, 0xb9, 0x7c, 0x7c, 0xec, 0xe2, 0x49, 0xc2, 0xb9, 0x8b, 0xdc, 0x02, 0x26, 0xcc, 0x4c, 0x2a, 0x57, 0xbf, 0x52, 0xfc])
    assert tx.to_address == bytes([0x00] * 20)
    assert tx.value == 1000000000
    assert tx.input == bytes([0x01, 0x02, 0x03, 0x04, 0x05])
    assert tx.gas_limit == 2000000
    assert tx.block_number is None
    assert isinstance(tx.gas, DynamicGas)
    assert tx.gas.max_fee_per_gas == 10000000000000
    assert tx.gas.max_priority_fee_per_gas == 100000000000


    assert tx is not None

if __name__ == "__main__":
    pytest.main(sys.argv)
