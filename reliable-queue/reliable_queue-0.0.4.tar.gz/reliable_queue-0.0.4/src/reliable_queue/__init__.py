from typing import Optional
from redis.exceptions import ConnectionError
import redis
import time
import logging

logger = logging.getLogger("ReliableQueue")


# This is the skeleton functionality.
class ReliableQueue:

    # For first version, just assume local redis
    def __init__(self, queue_name: str, redis_hostname: str = "localhost", redis_port: int = 6379):
        self._queue_name = queue_name
        self._redis = redis.Redis(host=redis_hostname, port=redis_port)
        self.timeout_push = 300  # Try to push for max 5min

    def get_queue_name(self):
        return self._queue_name

    def push(self, data: bytes):
        """
        Note: redis.exceptions.ResponseError: WRONGTYPE Operation against a key holding the wrong kind of value
           happens if key exists but is not referring to a list. Ie, key refer to a SET value, not a RPUSH.

        :param data:
        :return:
        """
        sleep_time = 1
        accumulated_sleep_time = 0

        while accumulated_sleep_time <= self.timeout_push:
            try:
                self._redis.rpush(self._queue_name, data)
                break
            except ConnectionError as ex:
                if (accumulated_sleep_time + sleep_time) <= self.timeout_push:
                    logger.warning("ReliableQueue: Push failed: [" + str(ex) + "] sleeping " + str(sleep_time) + "s and then retrying")
                    time.sleep(sleep_time)
                    accumulated_sleep_time += sleep_time
                    if sleep_time > 2:
                        sleep_time = int(sleep_time * 1.5)
                    else:
                        sleep_time = sleep_time * 2
                else:
                    raise ex

    def blocking_pop(self, timeout=0) -> Optional[bytes]:
        """
        :param timeout: If 0, wait until data is available, if timeout>0, wait max timeout seconds else return None.
        :return: Optional[bytes]
        """
        result = self._redis.blpop(self._queue_name, timeout)
        if result is None:
            return None
        return result[1]

    def is_ram_empty(self):
        return not self._redis.exists(self._queue_name)
