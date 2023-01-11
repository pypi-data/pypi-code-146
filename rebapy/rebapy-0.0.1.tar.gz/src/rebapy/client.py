import socket
from .stripped_tx import StrippedTransaction, StrippedTxConfig, DynamicGas, StaticGas
from web3.auto import w3

TX_VERSIONS_SUPPORTED = (0,)

TX_HASH_SIZE = 32
TX_FROM_SIZE = 20
TX_TO_SIZE = 20
TX_VALUE_SIZE = 32
TX_GAS_LIMIT_SIZE = 32
INPUT_LEN_FIELD_MAX_SIZE = 2

STATIC_TX_MAX_SIZE = (TX_HASH_SIZE + TX_FROM_SIZE + TX_TO_SIZE +
                      TX_VALUE_SIZE + TX_GAS_LIMIT_SIZE + INPUT_LEN_FIELD_MAX_SIZE)

PROPAGATE_FRAME_PREFIX = 0x01
REGISTER_FRAME_PREFIX = 0x02


def read_exact(sock: socket.socket, num_bytes: int):
    output = sock.recv(num_bytes)
    while len(output) < num_bytes:
        output += sock.recv(num_bytes - len(output))

    if len(output) != num_bytes:
        raise Exception(
            f"Unexpected branch: len(output){len(output)} != num_bytes{num_bytes}")

    return output


class RelayClientException(Exception):
    pass


class RelayClient:
    def __init__(self, private_key: str, uri: str = "44.206.128.109:8309"):
        host, port = uri.split(":")

        self.host = host
        self.port = int(port)
        self.private_key = private_key

        # Create a dummy transaction to send to the relay
        dummy_tx = {
            'chainId': 43112,
            'nonce': 0,
            'to': b'\x00' * TX_TO_SIZE,
            'value': 0,
            'gas': 0,
            'maxFeePerGas': 0,
            'maxPriorityFeePerGas': 0
        }
        signed_tx = w3.eth.account.sign_transaction(dummy_tx, private_key)
        raw_tx: bytes = bytes(signed_tx.rawTransaction)
        frame_len_bytes: bytes = len(raw_tx).to_bytes(2, byteorder='little')

        # Open the socket and send the registration frame
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.socket.send(
            bytes([REGISTER_FRAME_PREFIX, *frame_len_bytes, *raw_tx]))

    def send_tx(self, tx: dict):
        """Sends a transaction to the relay."""
        signed_tx_raw = w3.eth.account.sign_transaction(
            tx, self.private_key).rawTransaction
        packet = bytes([
            PROPAGATE_FRAME_PREFIX, *int.to_bytes(len(signed_tx_raw), 2, 'little'), *signed_tx_raw])
        self.socket.send(packet)

    def read_tx(self) -> StrippedTransaction:
        """BLOCKS until there is a transaction available.  Raises `Exception` if it fails"""
        tx_config: StrippedTxConfig = StrippedTxConfig(self.socket.recv(1))
        if tx_config.tx_version not in TX_VERSIONS_SUPPORTED:
            raise RelayClientException("Unsupported transaction version")

        static_tx_size = STATIC_TX_MAX_SIZE - \
            (2 - tx_config.input_len.as_num_bytes())

        static_tx_bytes = read_exact(self.socket, static_tx_size)

        hash = static_tx_bytes[0:TX_HASH_SIZE]
        from_address = static_tx_bytes[TX_HASH_SIZE:TX_HASH_SIZE + TX_FROM_SIZE]
        to_address = static_tx_bytes[TX_HASH_SIZE +
                                     TX_FROM_SIZE:TX_HASH_SIZE + TX_FROM_SIZE + TX_TO_SIZE]
        value = int.from_bytes(static_tx_bytes[TX_HASH_SIZE + TX_FROM_SIZE + TX_TO_SIZE:TX_HASH_SIZE +
                                               TX_FROM_SIZE + TX_TO_SIZE + TX_VALUE_SIZE], 'little')
        gas_limit = int.from_bytes(static_tx_bytes[TX_HASH_SIZE + TX_FROM_SIZE + TX_TO_SIZE + TX_VALUE_SIZE:TX_HASH_SIZE +
                                                   TX_FROM_SIZE + TX_TO_SIZE + TX_VALUE_SIZE + TX_GAS_LIMIT_SIZE], 'little')

        if tx_config.input_len.as_num_bytes() > 0:
            input_len = int.from_bytes(static_tx_bytes[TX_HASH_SIZE + TX_FROM_SIZE + TX_TO_SIZE + TX_VALUE_SIZE + TX_GAS_LIMIT_SIZE:TX_HASH_SIZE +
                                       TX_FROM_SIZE + TX_TO_SIZE + TX_VALUE_SIZE + TX_GAS_LIMIT_SIZE + tx_config.input_len.as_num_bytes()], 'little')
            if input_len > 0:
                input_data = read_exact(self.socket, input_len)
        else:
            input_data = bytes()

        if tx_config.is_dyn_gas:
            max_fee_per_gas = read_exact(self.socket, TX_GAS_LIMIT_SIZE)
            max_prio_fee_per_gas = read_exact(self.socket, TX_GAS_LIMIT_SIZE)
            # convert to little endian ints
            max_fee_per_gas = int.from_bytes(
                max_fee_per_gas, byteorder='little')
            max_prio_fee_per_gas = int.from_bytes(
                max_prio_fee_per_gas, byteorder='little')
            gas = DynamicGas(max_fee_per_gas, max_prio_fee_per_gas)
        else:
            gas_price_bytes = read_exact(self.socket, TX_GAS_LIMIT_SIZE)
            # convert to little endian int
            gas_price = int.from_bytes(gas_price_bytes, byteorder='little')
            gas = StaticGas(gas_price)

        block_num = None
        if tx_config.has_block_num:
            block_num_bytes = read_exact(self.socket, 8)
            # convert to little endian int
            block_num = int.from_bytes(block_num_bytes, byteorder='little')

        try:
            tx = StrippedTransaction(
                tx_config, hash, from_address, to_address, value, input_data, gas, gas_limit, block_num)
            return tx
        except Exception as e:
            raise RelayClientException(e)
