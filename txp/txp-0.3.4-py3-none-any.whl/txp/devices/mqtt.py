"""
This module offers MQTT utilities for the Gateway object.
"""
# ====================== Imports ===============================
from txp.common.config import settings
import paho.mqtt.client as paho_mqtt_client
from typing import Callable, Optional, List, Dict, Set, Union, Tuple
import ssl
import time
import threading
import jwt
import datetime
from txp.common.config import settings
import logging
import random
from txp.devices.exceptions import (
    MqttNetworkingUnavailableError,
    MqttPrivateKeyError,
    MqttConnectTimeoutError,
    MqttMessageNotPublished
)
import enum
from collections import defaultdict
import dataclasses

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)

# ===================== Data ===================================
mqtt_bridge_hostname = settings.gateway.mqtt.mqtt_bridge_hostname
mqtt_bridge_port = settings.gateway.mqtt.mqtt_bridge_port
jwt_expires_hours = settings.gateway.mqtt.jwt_expires_hours
seconds_per_hour = 3600


class MQTTMessageType(enum.Enum):
    """Enumerated message types for the messages published in MQTT broker"""
    TELEMETRY_MESSAGE = 0
    ATTACH_MESSAGE = 1
    DETACH_MESSAGE = 2
    STATE_MESSAGE = 3
    DEVICES_PAIRING_MESSAGE = 4

    def __str__(self):
        return self.name


@dataclasses.dataclass
class MQTTSentPayloadContext:
    """This context allows to store unacknowledged messages in
    order to retry sending"""
    device_id: str
    topic: str
    payload: Union[str, bytes]
    attach: bool

    def __post_init__(self):
        # A timestamp to handle some reasonable timeout for
        # unacknowledged messages
        self.timestamp = time.time()


# ==============================================================================
# Definition of the GatewayConfigurationListener class.
# ==============================================================================
class GatewayMQTTClient:
    def __init__(
            self,
            gateway_ref: "Gateway",
            on_message_callback: Callable
    ):
        """Args:

            gateway_ref: the reference to the Gateway instance.
            on_message_callback: The callback to be executed by the client when a message
                is received. The Gateway should pass the instance method for this callback,
                and any processing will be performed by the Gateway instance.
        """
        self._project_id = gateway_ref.gateway_config.project_id
        self._cloud_region = gateway_ref.gateway_config.cloud_region
        self._registry_id = gateway_ref.gateway_config.registry_id
        self._gateway_id = gateway_ref.gateway_config.gateway_id
        self._on_message_callback = on_message_callback

        self._acknowledge_rtt_timeout = 10

        self._connected_flag = False
        self._disconnected_flag = True
        self._networking_fatal_error = False  # A networking fatal error makes it impossible for the MQTT library
        # to create a Client instance.

        self._client: paho_mqtt_client.Client = None

        # seconds since the token was issued
        # https://cloud.google.com/iot/docs/how-tos/credentials/jwts
        self._jwt_iat: int = 0

        # Control and state attributes
        self._subscribed_topics: Dict[str, str] = {}
        """_subscribed_topics: A dict to hold the subscribed topics and devices ID for when 
        the client is restarted"""

        self._attached_devices: Set[str] = set()
        """_attached_devices: To track attached devices between client restarts"""

        # The initial backoff time after a disconnection occurs, in seconds.
        self._MINIMUM_BACKOFF_TIME = 1
        self._MAXIMUM_BACKOFF_TIME = 64
        self._should_backoff: bool = False

        self._connection_resource_lock: threading.RLock = threading.RLock()

        self._tracked_messages: Dict[int, Tuple[bool, MQTTMessageType, Union[str, bytes, MQTTSentPayloadContext]]] = defaultdict(tuple)
        """_tracked_messages: 
        
        A Map of messages ids -> (bool, message type, payload). 
            The tuple elements are: 
                0 -> bool to indicate if the message was acknowledge or not by the broker.
                1 -> The MQTTMessageType provided when a client of the class publish a message.
                2 -> The payload published. 
                
        This internal table helps the client to track the result of
        published messages, specifically if they were delivered to the broker and all the 
        appropriate handshakes were made."""

        try:
            self._refresh_client()

        except MqttConnectTimeoutError:
            log.error("The Mqtt client could not establish a connection at initialization time")

        except MqttNetworkingUnavailableError:
            log.error("The MQTT client could not establish a connection at initialization time.")

    def _refresh_client(self) -> None:
        """Internally creates a new paho MQTT client and assigns the corresponding
        values in the instance attributes.

        Raises:
            MqttConnectionTimeoutError: if the client could not connect to the MQTT broker
                after the configured timeout.
            MqttNetworkingUnavailableError: if the client could not connect because there's an
                unknown error with the networking of the operative system.
        """
        try:
            if self._should_backoff:
                if self._MINIMUM_BACKOFF_TIME < self._MAXIMUM_BACKOFF_TIME:
                    self._MINIMUM_BACKOFF_TIME = self._MINIMUM_BACKOFF_TIME * 2
                    log.info(f'Increasing Exponential Backoff minimum to: {self._MINIMUM_BACKOFF_TIME} seconds')

            self._client: paho_mqtt_client.Client = self._get_client(
                self._project_id, self._cloud_region, self._registry_id, self._gateway_id,
                on_connect_callback=self._on_connect,
                on_disconnect_callback=self._on_disconnect,
                on_message=self._on_message_callback,
                should_backoff=self._should_backoff,
                backoff_time=self._MINIMUM_BACKOFF_TIME,
                on_publish_callback=self._on_publish_callback
            )

            start_wait = time.time()
            while not self._connected_flag:
                end_wait = time.time()
                self._client.loop(timeout=2)
                if (end_wait - start_wait) > settings.gateway.mqtt.connection_timeout_secs:
                    raise MqttConnectTimeoutError()

            self._jwt_iat = datetime.datetime.utcnow()
            log.info("New paho MQTT client connected")

            for attached_device in self._attached_devices:
                self._attach_device(attached_device, "")
                log.debug(f'Device re-attached for new client: {attached_device}')

            time.sleep(settings.gateway.mqtt.attach_timeout_secs)

            for topic in self._subscribed_topics:
                self._client.subscribe(topic, qos=1)
                log.debug(f'Topic resubscribed for new client: {topic}')

        except MqttConnectTimeoutError:
            log.error("Timeout exceeded to establish connection with MQTT Broker")
            self._connected_flag = False
            self._disconnected_flag = True
            self._should_backoff = True
            raise

        except Exception as e:
            log.error(f'Unexpected exception connecting the MQTT client with connect() method: {e}')
            self._connected_flag = False
            self._disconnected_flag = True
            self._should_backoff = True
            self._networking_fatal_error = True
            raise MqttNetworkingUnavailableError

    def enable_incoming_messages_processing(self, duration_secs: int):
        """Enables the MQTT client to process callbacks for incoming messages that are found
        in the incoming messages buffer.


        Raises:
            MqttConnectionTimeoutError: if the client tries to reconnect and fails.
            MqttNetworkingUnavailableError: if the client tries to reconnect and the networking presents
                an unknown problem.
        """
        try:
            self._connection_resource_lock.acquire()

            if self._networking_fatal_error or self._disconnected_flag:
                log.info('MQTT client disconnected. Trying to reconnect.')
                self._refresh_client()

            error_code = self._client.loop_start()

            if error_code is not None:  # Somebody already started the loop. Just return.
                log.debug("Other thread already called enable_incoming_messages_processing. "
                          " Leaving silently.")
                return

            time.sleep(duration_secs)

            self._client.loop_stop()

            if self._disconnected_flag:  # the incoming messages processed a disconnection. Try to reconnect immediately
                self._refresh_client()

            if self._jwt_expired():  # Tries to refresh if JWT expired
                self._refresh_jwt()

        except Exception as e:
            log.error(f'Exception encountered while enabling incoming messages: {e}.')
            raise

        finally:
            self._connection_resource_lock.release()

    def _jwt_expired(self) -> bool:
        """Returns True if the JSON Web Token expired."""
        seconds_since_issue = (datetime.datetime.utcnow() - self._jwt_iat).seconds
        return seconds_since_issue > seconds_per_hour * jwt_expires_hours

    def _refresh_jwt(self):
        """Creates a new internal paho MQTT client with a new token"""
        log.info('Refreshing JWT for MQTT client')
        self._client.loop_stop()
        self._client.disconnect()
        while not self._disconnected_flag:
            self.enable_incoming_messages_processing(1)  # Waits for disconnect processing

        self._refresh_client()

    def _on_connect(self, unused_client, unused_userdata, unused_flags, rc):
        """Callback to be executed asynchronously when the internal self._client
        gets connected."""
        log.info(f"Connection to MQTT IoT Bridge established")
        self._connected_flag = True
        self._disconnected_flag = False
        self._should_backoff = False
        self._networking_fatal_error = False
        self._MINIMUM_BACKOFF_TIME = 1

    def _on_disconnect(self, unused_client, unused_userdata, rc):
        """Callback to be executed asynchronously when the internal self._client
        is disconnected from the broker"""
        log.info(f"MQTT client disconnected. Disconnect Code:{rc}")
        if rc != 0:
            log.warning(f'Unexpected disconnect code in MQTT client: {rc}')
        self._disconnected_flag = True
        self._connected_flag = False
        self._should_backoff = True

    def _on_publish_callback(self, client, userdata, mid):
        """Callback to be executed asynchronously when a published message was acknowledge and
        it was delivered to the broker successfully."""
        if mid not in self._tracked_messages:
            log.debug(f"The message {mid} was delivered to the broker, "
                      f"but no tracking is active for that message id. Nothing is done.")

        else:
            value = self._tracked_messages[mid]
            self._tracked_messages[mid] = (True, value[1], value[2])
            log.debug(f"The message {mid} was delivered to the broker, "
                      f"Delivered tracking of the message is set to True. ")

    def subscribe_to_topic(self, device_id: str, topic: str, attach: bool) -> None:
        """Subscribe the client to the specified topic.

        Args:
            device_id: the device_id of the device related to the topic.
            topic: the topic to subscribe to.
            attach: True if the device must be 'attached' before subscribe. Edge devices must be 'attached' to the
                Gateway to allow the Gateway to publish telemetry in the name of the devices.

        Reference:
            https://github.com/GoogleCloudPlatform/python-docs-samples/blob/fca5081e785a19bcf28f2bde69240bf96b40d58f/iot/api-client/mqtt_example/cloudiot_mqtt_example.py#L210

        Returns:
            None
        """
        try:
            self._connection_resource_lock.acquire()

            if self._networking_fatal_error or self._disconnected_flag:
                log.info('MQTT client disconnected. Trying to reconnect.')
                self._refresh_client()

            if topic in self._subscribed_topics.keys():
                return

            if attach:
                self._attach_device(device_id, "")
                time.sleep(settings.gateway.mqtt.attach_timeout_secs)

            self._client.subscribe(topic, qos=1)
            self._subscribed_topics[topic] = device_id
            log.info(f'MQTT client subscribed to topic: {topic}')

        except Exception as e:
            log.error(f'Exception encountered while subscribing to topic: {e}')
            raise

        finally:
            self._connection_resource_lock.release()

    def publish_message(
            self,
            message_type: MQTTMessageType,
            device_id: str,
            topic: str,
            payload: Union[str, bytes],
            attach: bool,
            track_acknowledge: bool,
            try_reconnect: bool = True,
            delay: int = 0
    ):
        """Publish the message payload to the provided topic

        Published messages can be requested to be tracked by the MQTT client
        if the user of the class requires to know that a message was delivered or not.

        Args:
            message_type: The message type to be published.
            device_id: The device ID in IoT Core.
            topic: The MQTT Topic in the IoT Core Broker.
            payload: the message payload.
            attach: True if the device requires to be attached to the
                Gateway owner of this MQTT Client.
            track_acknowledge: If True, the MQTT client will track the
                published message on the on_publish() callback
                More info about on_publish() callback here:
                    https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php#callbacks

        """
        try:
            self._connection_resource_lock.acquire()

            if self._networking_fatal_error or self._disconnected_flag:
                if not try_reconnect:
                    log.error(f'There was an error publishing a message to the topic: {topic}')
                    raise MqttMessageNotPublished
                else:
                    log.info('MQTT client disconnected. Trying to reconnect.')
                    self._refresh_client()

            if self._jwt_expired():
                self._refresh_jwt()

            if attach and not self._is_attached(device_id):
                self._attach_device(device_id, "")
                time.sleep(settings.gateway.mqtt.attach_timeout_secs)

            if delay:
                time.sleep(delay)

            (result, mid) = self._client.publish(topic, payload, qos=1)
            log.debug(f'Publishing message in topic: {topic}. '
                      f'mid: {mid}. result:{result}')

            if result == paho_mqtt_client.MQTT_ERR_SUCCESS:
                log.debug(f'Message successfully published for topic {topic}')
                if track_acknowledge:
                    if mid in self._tracked_messages:
                        log.warning(f"The message id {mid} was found in the tracked messages table."
                                    f" Overriding previous value.")
                    self._tracked_messages[mid] = (
                        False,
                        message_type,
                        MQTTSentPayloadContext(device_id, topic, payload, attach)
                    )
            else:
                log.error(f'There was an error publishing a message to the topic: {topic}')
                raise MqttMessageNotPublished

        except Exception as e:
            log.error(f'Unexpected Exception in MQTT connection operation: {e}')
            raise MqttMessageNotPublished

        finally:
            self._connection_resource_lock.release()

    def get_unacknowledged_messages(self, message_type: MQTTMessageType) -> List:
        """Returns a list of unsent messages according to the message type.

        The returned messages will be cleaned from the client tracking.

        Note: The list is not ordered according to how the messages were sent.

        Returns:
            List of unacknowledged payloads.
        """
        filtered_list = []
        items_to_pop = []
        log.debug(f"Checking for unacknowledged messages of type: {message_type.__str__()}")

        for mid, entry in self._tracked_messages.copy().items():
            is_sent, m_type, payload = entry
            if not is_sent and m_type == message_type:
                log.debug(f"Message with id {mid} was not acknowledge. Computing timeout valid")
                timeout_exceeded = (time.time() - payload.timestamp) > self._acknowledge_rtt_timeout
                if timeout_exceeded:
                    log.debug(f"The message {mid} exceeded timeout. Returning as unacknowledged")
                    filtered_list.append(payload)
                    self._tracked_messages.pop(mid)

        log.debug(f"{len(filtered_list)} unacknowledged messages found")
        return filtered_list

    def clear_acknowledged_messages(self, message_type: MQTTMessageType) -> None:
        """Clears the internal tracking of acknowledged messages of type message_type

        Returns:
            None
        """
        init_sz = len(self._tracked_messages)
        self._tracked_messages = {
            m_id: m_entry for m_id, m_entry in self._tracked_messages.items()
            if not m_entry[0] and not m_entry[1] == message_type
            # If not sent and message type is not message_type
        }
        after_sz = len(self._tracked_messages)
        log.debug(f"Removed {init_sz-after_sz} sent messages from tracking registry")

    def unsubscribe_from_topic(self, topic: str):
        """Unsubscribe the client from the specified topic.

        Args:
            The topic to unsubscribe from.

        Returns:
            None
        """
        try:
            self._connection_resource_lock.acquire()

            if self._networking_fatal_error or self._disconnected_flag:
                log.info('MQTT client disconnected. Trying to reconnect.')
                self._refresh_client()

            if topic not in self._subscribed_topics:
                log.warning(f'Trying to unsubscribe from topic {topic}, '
                            f'but the topic was not previously subscribed')
                return

            device_id = self._subscribed_topics[topic]

            if device_id in self._attached_devices:
                self._detach_device(device_id)

            self._client.unsubscribe(topic)
            log.info(f'MQTT client unsubscribed from topic: {topic}')

            self._subscribed_topics.pop(topic)

        except Exception as e:
            log.error(f'Unexpected Exception in MQTT connection operation: {e}')
            raise

        finally:
            self._connection_resource_lock.release()

    def _detach_device(self, device_id):
        """Detach the device from the gateway."""
        detach_topic = settings.gateway.mqtt.device_dettach_topic_template.format(
            device_id
        )
        log.debug("Detaching: {}".format(detach_topic))
        self._client.publish(detach_topic, "{}", qos=1)
        self._attached_devices.remove(device_id)

    def _attach_device(self, device_id, auth):
        """Attach the device to the gateway."""
        log.debug("Attaching: {}".format(device_id))
        attach_topic = settings.gateway.mqtt.device_attach_topic_template.format(
            device_id
        )
        attach_payload = '{{"authorization" : "{}"}}'.format(auth)
        self._client.publish(attach_topic, attach_payload, qos=1)
        self._attached_devices.add(device_id)

    def _is_attached(self, device_id: str) -> bool:
        """Returns True if the device is attached to the Gateway client."""
        return device_id in self._attached_devices

    @staticmethod
    def _create_jwt(project_id: str):
        """Creates a JWT to establish an MQTT connection

        Raises:
            MqttPrivateKeyError: If could not deserialize the Private Key data.
        """
        algorithm = "RS256"  # I created the key with this algorithm
        token = {
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=jwt_expires_hours),
            "aud": project_id
        }

        try:
            with open(settings.gateway.private_key_path, "r") as f:
                private_key = f.read()

            log.info("Creating JWT using {} from private key file {}".format(
                algorithm, settings.gateway.private_key_path
            ))

            return jwt.encode(token, private_key, algorithm=algorithm)

        except:
            raise MqttPrivateKeyError()

    @classmethod
    def _get_client(
            cls,
            project_id: str,
            cloud_region: str,
            registry_id: str,
            device_id: str,
            on_connect_callback: Optional[Callable] = None,
            on_disconnect_callback: Optional[Callable] = None,
            on_message: Optional[Callable] = None,
            on_publish_callback: Optional[Callable] = None,
            should_backoff: bool = False,
            backoff_time: int = 0
    ):
        """Creates a Paho mqtt Client instance to handle the MQTT protocol communication"""
        client_id = settings.gateway.mqtt.device_id_template.format(
            project_id, cloud_region, registry_id, device_id
        )
        log.info(f"MQTT client ID configured {client_id}")

        client = paho_mqtt_client.Client(client_id=client_id)

        client.username_pw_set(
            username='unused',
            password=cls._create_jwt(project_id)
        )

        client.tls_set(
            ca_certs=settings.gateway.ca_certs,
            tls_version=ssl.PROTOCOL_TLSv1_2
        )

        client.on_connect = on_connect_callback
        client.on_disconnect = on_disconnect_callback
        client.on_message = on_message
        client.on_publish = on_publish_callback

        if should_backoff:
            delay = backoff_time + random.randint(0, 1000) / 1000.0
            time.sleep(delay)

        client.connect(mqtt_bridge_hostname, mqtt_bridge_port,
                       settings.gateway.mqtt.keep_alive_minutes * 60)

        return client

    @staticmethod
    def validate_connection_values(
        project_id: str,
        cloud_region: str,
        registry_id: str,
        device_id: str,
    ) -> bool:
        """Validate if a Cloud Connection could be established using the passed
            arguments and the existing private key.

            Args:
                project_id: the project ID in Cloud IoT
                cloud_region: the cloud region configured for the project in Cloud IoT
                registry_id: the registry ID configured in the project
                device_id: the device ID of the Gateway (the serial)

            Raises:
                ValueError: If could not deserialize the Private Key data.

            Returns:
                True if the connection was established successfully. False otherwise.
        """

        def on_connect_closure(flags):
            """Callback for when a device connects."""

            def on_connect_callback(unused_client, unused_userdata, unused_flags, rc):
                log.info(f"Connection to MQTT IoT Bridge established")
                flags[0] = True

            return on_connect_callback

        def on_disconnect(unused_client, unused_userdata, rc):
            """Paho callback for when a device disconnects."""
            message = paho_mqtt_client.connack_string(rc)
            log.info(f"Disconnected from MQTT IoT Bridge {message}")

        def on_message_closure(flags):
            def on_message_callback(unused_client, unused_userdata, message):
                """Callback when the device receives a message on a subscription."""
                flags[1] = True
                log.info(f"Message received from MQTT IoT Bridge received")

            return on_message_callback

        flags = [False, False]

        try:
            client: paho_mqtt_client.Client = GatewayMQTTClient._get_client(
                project_id, cloud_region, registry_id, device_id,
                on_connect_closure(flags), on_disconnect, on_message_closure(flags)
            )
        except ValueError as key_deseriaize_error:
            raise key_deseriaize_error

        client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

        # Subscribe to the Gateway topic.
        mqtt_config_topic = "/devices/{}/config".format(device_id)

        client.subscribe(mqtt_config_topic, qos=1)

        jwt_iat = datetime.datetime.utcnow()
        test_start = time.time()

        while True:
            client.loop_start()

            seconds_since_issue = (datetime.datetime.utcnow() - jwt_iat).seconds
            if seconds_since_issue > seconds_per_hour * jwt_expires_hours:
                log.info("Refreshing token after {}s".format(seconds_since_issue))
                jwt_iat = datetime.datetime.utcnow()
                client.loop_stop()
                client.disconnect()
                client = GatewayMQTTClient._get_client(
                    project_id, cloud_region, registry_id, device_id,
                    on_connect_closure(flags), on_disconnect, on_message_closure(flags)
                )

            client.loop_stop()
            time.sleep(1)  # sleeps for 1 second for next loop activation

            elapsed = time.time() - test_start

            if elapsed > 15 or all(flags):
                client.disconnect()
                break

        if all(flags):
            log.info(f"Connection to MQTT IoT Bridge validated")
            return True
        else:
            log.warning(f"Could not validate Connection to MQTT IoT Bridge")
            return False
