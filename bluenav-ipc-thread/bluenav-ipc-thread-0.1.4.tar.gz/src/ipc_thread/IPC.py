import json
import logging
import time
import queue
from typing import Any, Callable

import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.client as client
import awsiot.greengrasscoreipc.model as model
from awsiot.greengrasscoreipc.model import (
    QOS,
    ComponentUpdatePolicyEvents,
    DeferComponentUpdateRequest,
    JsonMessage,
    PublishMessage,
    PublishToIoTCoreRequest,
    PublishToTopicRequest,
    SubscribeToComponentUpdatesRequest,
    SubscribeToIoTCoreRequest,
    SubscribeToTopicRequest,
    SubscriptionResponseMessage,
)

from .SingletonMeta import SingletonMeta

logger = logging.getLogger("ipc_thread.IPC")


class TopicStreamHandler(client.SubscribeToTopicStreamHandler):
    """
    Event handler for SubscribeToTopicOperation
    i.e local IPC message between components
    """

    __operation: client.SubscribeToTopicOperation

    def __init__(self, topic: str):
        super().__init__()
        self.__topic = topic
        self.logger = logging.getLogger("bluenav-ipc-thread.local-ipc")

    def set_operation(self, operation: client.SubscribeToTopicOperation):
        self.__operation = operation

    def stop(self) -> None:
        self.__operation.close()

    def on_stream_event(self, event: SubscriptionResponseMessage) -> None:
        """
        Invoked when a SubscriptionResponseMessage is received.
        """
        try:
            if event.json_message:
                message = event.json_message.message
            elif event.binary_message:
                message = event.binary_message.message
            else:
                self.logger.warning("Unknown message type, discarding message")
                return

            if self.__handler:
                try:
                    self.__handler(message, self.__topic)
                    logger.debug(f"[SUB] ({self.__topic}) {message}")
                except queue.Full:
                    self.logger.debug(f"[SUB_ERROR] ({self.__topic}) Queue is full")
        except:
            self.logger.exception("Unandled exception")

    def on_stream_error(self, error: Exception) -> bool:
        self.logger.warning(error)
        return False  # Return True to close stream, False to keep stream open.

    def set_handler(self, callback: Callable[[Any, str], None]) -> None:
        """
        Handler will be trigger when a SubscriptionResponseMessage is received
        """
        self.__handler = callback


class CoreStreamHandler(client.SubscribeToIoTCoreStreamHandler):
    """
    Event handler for SubscribeToIoTCoreOperation
    i.e MQTT message between IoT Core and local device
    """

    __operation: client.SubscribeToIoTCoreOperation

    def __init__(self, topic):
        super().__init__()
        self.__handler = None
        self.__topic = topic
        self.logger = logging.getLogger("bluenav-ipc-thread.mqtt-core")

    def set_operation(self, operation: client.SubscribeToIoTCoreOperation):
        self.__operation = operation

    def stop(self) -> None:
        self.__operation.close()

    def on_stream_event(self, event: model.IoTCoreMessage) -> None:
        """
        Invoked when a IoTCoreMessage is received.
        """
        try:
            if event.message:
                if event.message.payload:
                    message = str(event.message.payload, "utf-8")
                    if self.__handler:
                        try:
                            self.__handler(message, self.__topic)
                            logger.debug(f"[SUB_CORE] ({self.__topic}) {message}")
                        except queue.Full:
                            self.logger.debug(f"[SUB_ERROR] ({self.__topic}) Queue is full")
        except:
            self.logger.exception("Unandled exception")

    def on_stream_error(self, error: Exception) -> bool:
        self.logger.warning(error)
        return True  # Return True to close stream, False to keep stream open.

    def set_handler(self, callback: Callable[[Any, str], None]) -> None:
        """
        Handler will be trigger when a IoTCoreMessage is received
        """
        self.__handler = callback


class UpdateStreamHandler(client.SubscribeToComponentUpdatesStreamHandler):
    """
    Event handler for SubscribeToComponentUpdatesOperation
    """

    def __init__(self):
        super().__init__()
        self.__handler = None

    def on_stream_event(self, event: ComponentUpdatePolicyEvents) -> None:
        """
        Invoked when a ComponentUpdatePolicyEvents is received.
        """
        if self.__handler:
            self.__handler(event)

    def set_handler(self, handler):
        self.__handler = handler


class IPC(metaclass=SingletonMeta):
    """
    Handle interprocess communication and subscribe/publish operation
    """

    __ipc_client = None

    def __init__(self):
        self.connect()
        self.__TIMEOUT = 10

    def connect(self) -> bool:
        try:
            self.__ipc_client = awsiot.greengrasscoreipc.connect()
            return True
        except InterruptedError:
            self.__ipc_client = None
            time.sleep(10)
            return self.connect()
        except Exception as e:
            self.__ipc_client = None
            time.sleep(10)
            return self.connect()

    def subscribe(self, topic: str) -> TopicStreamHandler:
        try:
            request = SubscribeToTopicRequest()
            request.topic = topic

            handler = TopicStreamHandler(topic)

            if self.__ipc_client:
                self.__operation = self.__ipc_client.new_subscribe_to_topic(handler)
            else:
                raise Exception

            handler.set_operation(self.__operation)
            future = self.__operation.activate(request)
            future.result(self.__TIMEOUT)

            logger.debug(f"Subscribed to new topic: {topic}")
            return handler
        except Exception as e:
            logging.error(f"Error subscribing to topic {topic}: {e}")
            time.sleep(10)
            return self.subscribe(topic)

    def publish(self, topic: str, message: dict):
        try:
            request = PublishToTopicRequest()
            request.topic = topic

            publish_message = PublishMessage()
            publish_message.json_message = JsonMessage()
            publish_message.json_message.message = message

            request.publish_message = publish_message

            if self.__ipc_client:
                operation = self.__ipc_client.new_publish_to_topic()
            else:
                raise Exception

            operation.activate(request)

            future = operation.get_response()
            future.result(self.__TIMEOUT)
            logger.debug(f"[PUB] ({topic}) {message}")
        except Exception as e:
            logging.error(f"Error publishing to topic {topic}: {e}")
            time.sleep(10)
            self.publish(topic, message)

    def disconnect(self):
        if self.__ipc_client != None:
            self.__ipc_client.close()
            self.__ipc_client = None

    def is_connected(self):
        return self.__ipc_client != None

    def publish_to_core(self, topic: str, message: str):
        if self.__ipc_client != None:
            op = self.__ipc_client.new_publish_to_iot_core()
            op.activate(
                PublishToIoTCoreRequest(
                    topic_name=topic,
                    qos=model.QOS.AT_LEAST_ONCE,
                    payload=json.dumps(message).encode(),
                )
            )
            op.get_response().result(timeout=5.0)
            logger.debug(f"[PUB_CORE] ({topic}) {message}")

    def subscribe_to_core(self, topic: str) -> CoreStreamHandler:
        try:
            qos = QOS.AT_LEAST_ONCE
            request = SubscribeToIoTCoreRequest()
            request.topic_name = topic
            request.qos = qos
            handler = CoreStreamHandler(topic)
            if self.__ipc_client:
                operation = self.__ipc_client.new_subscribe_to_iot_core(handler)
            else:
                raise Exception
            handler.set_operation(operation)
            future = operation.activate(request)
            future.result(self.__TIMEOUT)
            logger.debug(f"Subscribed to new core topic: {topic}")
            return handler
        except Exception as e:
            logging.error(f"Error subscribing to core: {e}")
            time.sleep(10)
            return self.subscribe_to_core(topic)

    def subscribe_to_component_update(self) -> UpdateStreamHandler:
        try:
            if self.__ipc_client != None:
                handler = UpdateStreamHandler()
                op = self.__ipc_client.new_subscribe_to_component_updates(handler)
                future = op.activate(SubscribeToComponentUpdatesRequest())
                future.result(self.__TIMEOUT)

                return handler
            else:
                raise Exception
        except Exception as e:
            logging.error(f"Error in subscribe_to_component_update: {e}")
            time.sleep(10)
            return self.subscribe_to_component_update()

    def defer_update(self, deployment_id: str) -> None:
        """
        Defer an update until restart
        """
        try:
            if self.__ipc_client:
                op = self.__ipc_client.new_defer_component_update()
                request = DeferComponentUpdateRequest()
                request.set_deployment_id(deployment_id)
                request.set_recheck_after_ms(60 * 1000 * 60 * 24 * 8000)

                future = op.activate(request)
                future.result(5)
        except Exception as e:
            return

    def acknowledge_update(self, deployment_id: str) -> None:
        try:
            if self.__ipc_client:
                op = self.__ipc_client.new_defer_component_update()
                request = DeferComponentUpdateRequest()
                request.set_deployment_id(deployment_id)
                # Specify recheck_after_ms=0 to acknowledge a component update.
                request.set_recheck_after_ms(0)

                future = op.activate(request)
                future.result(5)
        except Exception as e:
            return
