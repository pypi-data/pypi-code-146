import json
import logging
import threading
import time
import queue
from typing import Any, Callable

import redis

logger = logging.getLogger("ipc_thread.IPC.dev")


class MockIoTCore:
    def __init__(self) -> None:
        pass

    def set_handler(self, callback: Any) -> None:
        pass


class MessageHandler(threading.Thread):
    def __init__(self, sub) -> None:
        super().__init__()
        self.sub = sub
        self.__handler = None
        self.start()

    def set_handler(self, callback: Callable[[str, str], None]) -> None:
        self.__handler = callback

    def run(self):
        for msg in self.sub.listen():
            if msg and msg["type"] == "message" and self.__handler:
                try:
                    self.__handler(json.loads(msg["data"]), msg["channel"].decode())
                    logger.debug(
                        f"[SUB] ({msg['channel'].decode()}) {json.loads(msg['data'])}"
                    )
                except queue.Full:
                     logger.debug(
                        f"[SUB_ERROR] ({msg['channel'].decode()}) Queue is full"
                    )
                except Exception as e:
                    logger.exception(f"[SUB_ERROR]")


class dev_IPC:
    def __init__(self):
        self.__ipc_client = None
        self.connect()
        self.__TIMEOUT = 10

    def connect(self) -> bool:
        try:
            self.__ipc_client = redis.Redis(host="localhost", port=6379, db=0)
            return True
        except InterruptedError:
            self.__ipc_client = None
            time.sleep(10)
            return self.connect()
        except Exception as e:
            self.__ipc_client = None
            time.sleep(10)
            return self.connect()

    def disconnect(self):
        if self.__ipc_client is not None:
            self.__ipc_client.close()
            self.__ipc_client = None

    def subscribe(self, topic: str) -> MessageHandler:
        if self.__ipc_client:
            sub = self.__ipc_client.pubsub()
            sub.subscribe(topic)
            logger.debug(f"Subscribed to new topic: {topic}")
            return MessageHandler(sub)
        else:
            raise Exception("IPC client not connected")

    def publish(self, topic: str, data: Any) -> None:
        if self.__ipc_client:
            self.__ipc_client.publish(topic, json.dumps(data))
            logger.debug(f"[PUB] ({topic}) {json.dumps(data)}")

    def publish_to_core(self, topic: str, data: Any) -> None:
        pass

    def subscribe_to_core(self, topic) -> MockIoTCore:
        return MockIoTCore()

    def subscribe_to_component_update(self) -> MockIoTCore:
        return MockIoTCore()

    def acknowledge_update(self, Any) -> None:
        pass

    def defer_update(self, Any) -> None:
        pass
