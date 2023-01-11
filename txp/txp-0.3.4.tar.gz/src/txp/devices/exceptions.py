"""
This module defines the base exceptions to be used in the Gateway
system.
"""
# ============================ imports =========================================
class GatewayRecoverableException(Exception):
    """This exception class is thought to use across the system
    when errors that are **expected** could happen and are treated
    gracefully by the callers.
    """
    pass


class GatewayFatalException(Exception):
    """This exception base class is thought to use across the system
    when an error should transition the Gateway States machine to an
    error state."""
    pass


class MqttNetworkingUnavailableError(GatewayRecoverableException):
    """This exception should be used when a unexpected error
    is found with the networking of the device."""
    pass


class MqttPrivateKeyError(GatewayRecoverableException):
    """This exception should be used when the received private
    key provided could not be parsed."""
    pass


class MqttConnectTimeoutError(GatewayRecoverableException):
    """This exception should be used when the MQTT paho client
    can not establish the connection with the broker. It's most
    used for internet outages."""
    pass


class MqttMessageNotPublished(GatewayRecoverableException):
    """This exception should be used when the MQTT paho client
    fails to publish a message to the broker.

    Specifically, the rc code is not zero:
        https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php#publishing
    """
    pass
