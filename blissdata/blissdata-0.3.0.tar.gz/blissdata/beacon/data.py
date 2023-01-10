"""Get Bliss data information from Beacon."""

import struct
from ._base import BeaconClient
from ._base import IncompleteBeaconMessage


class BeaconData(BeaconClient):
    """Provides the API to read the redis databases urls."""

    REDIS_QUERY = 30
    REDIS_QUERY_ANSWER = 31

    REDIS_DATA_SERVER_QUERY = 32
    REDIS_DATA_SERVER_FAILED = 33
    REDIS_DATA_SERVER_OK = 34

    def get_redis_db(self) -> str:
        """Returns the URL of the Redis database that contains the Bliss settings. For example 'foobar:25001'."""
        msg = b"%s%s" % (struct.pack("<ii", self.REDIS_QUERY, 0), b"")
        self._connection.sendall(msg)
        data = b""
        while True:
            raw_data = self._connection.recv(16 * 1024)
            if not raw_data:
                break
            data = b"%s%s" % (data, raw_data)
            try:
                message_type, message, data = self._unpack_message(data)
            except IncompleteBeaconMessage:
                continue
            break
        if message_type != self.REDIS_QUERY_ANSWER:
            raise RuntimeError(f"Unexpected message type '{message_type}'")
        return message.decode()

    def get_redis_data_db(self) -> str:
        """Returns the URL of the Redis database that contains the Bliss scan data. For example 'foobar:25002'."""
        response = self._request(self.REDIS_DATA_SERVER_QUERY, "")
        response_type, data = response.read()
        if response_type == self.REDIS_DATA_SERVER_OK:
            return data.decode().replace("|", ":", 1)
        elif response_type == self.REDIS_DATA_SERVER_FAILED:
            raise RuntimeError(data.decode())
        raise RuntimeError(f"Unexpected Beacon response type {response_type}")
