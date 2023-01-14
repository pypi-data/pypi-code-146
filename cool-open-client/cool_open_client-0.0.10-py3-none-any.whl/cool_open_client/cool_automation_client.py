import functools
import gc
import logging
import threading
import time
import websocket
import json
import marshmallow
import marshmallow_dataclass
import sys

from typing import Callable, Iterable, Union, cast
from threading import Thread

from dataclasses import dataclass, field

from websocket import (
    WebSocketConnectionClosedException,
    WebSocketException,
    WebSocketConnectionClosedException,
)
from .client.api_client import ApiClient

from .client.models.unit_control_fans_body import UnitControlFansBody
from .client.api.me_api import MeApi
from .client.models.user_response_data import UserResponseData


from .client.api.devices_api import DevicesApi
from .client.models.device_response_data import DeviceResponseData
from .client.models.devices_response import DevicesResponse
from .client.models.devices_response_data import DevicesResponseData

from .client import UnitControlApi, UnitControlSwitchesBody
from .client.api.services_api import ServicesApi
from .client.api.units_api import UnitsApi
from .client.api.unit_api import UnitApi
from .client.models.types_response_data import TypesResponseData
from .client.models.units_response import UnitsResponse
from .client.models.unit_response_data import UnitResponseData
from .client.rest import ApiException
from .client.api.authentication_api import AuthenticationApi
from .client.models.unit_control_modes_body import UnitControlModesBody
from .client.models.unit_control_setpoints_body import UnitControlSetpointsBody
from .client.models.unit_control_swings_body import UnitControlSwingsBody

from .utils.dictionaries import DictTypes
from .utils.singleton import Singleton
from .utils.updatable import Updatable
from .utils.dict_to_model import dict_to_model


_LOGGER = logging.getLogger(__package__)
_LOGGER.addHandler(logging.StreamHandler(sys.stdout))
_LOGGER.setLevel(logging.WARNING)

###
# Data Sample
# {'data': {'ambientTemperature': 29,
#           'deviceId': '61bb087a212f1c7c42b9e76a',
#           'fan': 3,
#           'filter': False,
#           'internalId': '283B960300D4:31303336',
#           'operationMode': 0,
#           'operationStatus': 2,
#           'serviceUnits': [],
#           'setpoint': 25,
#           'site': '61f8e091a8a31c1966b33a29',
#           'swing': 6,
#           'temperatureScale': 1,
#           'unitId': '61f8e56960bf483d1e5b0743'},
#  'name': 'UPDATE_UNIT'}
###


@dataclass
class UnitUpdateMessage:
    """Data class representing the update message received from the server"""

    ambient_temperature: int = field(
        metadata={"required": False, "data_key": "ambientTemperature"}
    )
    unit_id: str = field(metadata={"required": True, "data_key": "unitId"})
    fan_mode: Union[str, int] = field(metadata={"required": True, "data_key": "fan"})
    filter: bool = field(metadata={"required": False, "data_key": "filter"})
    operation_mode: Union[str, int] = field(
        metadata={"required": True, "data_key": "operationMode"}
    )
    operation_status: Union[str, int] = field(
        metadata={"required": True, "data_key": "operationStatus"}
    )
    setpoint: int = field(metadata={"required": True, "data_key": "setpoint"})
    swing: Union[str, int] = field(metadata={"required": True, "data_key": "swing"})
    temperature_scale: int = field(
        metadata={"required": False, "data_key": "temperatureScale"}, default=1
    )


UnitUpdateMessageSchema = marshmallow_dataclass.class_schema(UnitUpdateMessage)


def with_exception(function):
    @functools.wraps(function)
    async def wrapper(*args, **kwargs):
        try:
            return await function(*args, **kwargs)
        except ApiException as exception:
            body = json.loads(exception.body)
            if exception.status == CoolAutomationClient.UNAUTHORIZES_ERROR_CODE:
                raise InvalidTokenException() from exception
            else:
                raise exception

    return wrapper


class WebSocketThread(Thread):
    """Extension of Thread class to handle the websocket connection"""

    def __init__(
        self, socket_params: dict[str, Callable], logger: logging.Logger = None
    ):
        threading.Thread.__init__(self)
        self.name = "CoolAutomationClientWebsocketClient"
        self.setDaemon(True)
        self.websocket = None
        self.close_flag = False
        self.logger = _LOGGER if logger is None else logger
        self.socket_params = socket_params

    def run(self):
        self.close_flag = False
        while not self.close_flag:
            try:
                if self.websocket is not None:
                    try:
                        self.websocket.keep_running = False
                        self.websocket.close()
                        gc.collect()
                    except:
                        pass
                self.websocket = websocket.WebSocketApp(**self.socket_params)
                self.websocket.run_forever()

            except WebSocketException as socket_exception:
                gc.collect()
                self.logger.error(
                    "Exception when calling open socket: %s", socket_exception
                )
            except Exception as exception:
                gc.collect()
                self.logger.error("Exception when calling open socket: %s", exception)

            time.sleep(10)

    def close(self):
        self.close_flag = True
        self.websocket.close()


class CoolAutomationClient(Singleton):
    """
    The coolautomation_client for CoolAutomationCloud service
    """

    UNAUTHORIZES_ERROR_CODE = 401
    SOCKET_URI = "wss://api.coolremote.net:443/ws/v2"

    @classmethod
    async def create(cls, token, logger=None):
        self = cls(logger=logger)
        if token is None:
            raise ValueError("Toke cannot be None")
        self.token = token
        dictionaries = await self.get_dictionary()
        self._dictionaries: TypesResponseData = dictionaries
        self.temperature_scale = DictTypes(dictionaries.temperature_scale)
        self.operation_statuses = DictTypes(dictionaries.operation_statuses)
        self.operation_modes = DictTypes(dictionaries.operation_modes)
        self.fan_modes = DictTypes(dictionaries.fan_modes)
        self.swing_modes = DictTypes(dictionaries.swing_modes)
        return self

    @classmethod
    async def authenticate(cls, username: str, password: str) -> str:
        """
        Perform Authentication
        """
        body = {"username": username, "password": password, "appId": "coolAutomationControl"}
        api = AuthenticationApi()
        try:
            result = await api.users_authenticate_post(body)
        except ApiException as error:
            if error.status == cls.UNAUTHORIZES_ERROR_CODE:
                return "Unauthorized"
        return result.data.token

    def __init__(self, logger: logging.Logger = None) -> None:
        self.token = None
        self._dictionaries: TypesResponseData = None
        self.temperature_scale = None
        self.operation_statuses = None
        self.operation_modes = None
        self.fan_modes = None
        self.swing_modes = None
        self.socket = None
        self._registered_units: dict[str, Updatable] = {}
        self.api_client = ApiClient()
        self.logger = logger if logger is not None else _LOGGER
        self.ws_thread: Thread = None

    @with_exception
    async def get_me(self) -> UserResponseData:
        api = MeApi(api_client=self.api_client)
        response = await api.users_me_get(self.token)
        return response.data

    @with_exception
    async def get_dictionary(self) -> TypesResponseData:
        """
        Pulls dictionary from the API

        Returns:
            TypesResponseData: Dictionary from api service
        """
        api = ServicesApi(self.api_client)
        response = await api.services_types_get(self.token)
        return response.data

    @with_exception
    async def get_controllable_units(self) -> UnitsResponse:
        """
        Retrieves the controllable units from the web api
        """
        # pp = pprint.PrettyPrinter(indent=4).pprint
        api = UnitsApi(api_client=self.api_client)
        units: UnitsResponse = await api.units_get(self.token)

        return units

    @with_exception
    async def get_updated_controllable_unit(self, unit_id: str) -> UnitUpdateMessage:
        """
        Retrieves the controllable units from the web api
        """
        api = UnitApi(api_client=self.api_client)
        unit: UnitResponseData = (await api.units_unit_id_get(self.token, unit_id)).data

        message = UnitUpdateMessage(
            ambient_temperature=unit.ambient_temperature,
            fan_mode=unit.active_fan_mode,
            operation_mode=unit.active_operation_mode,
            setpoint=unit.active_setpoint,
            swing=unit.active_swing_mode,
            operation_status=unit.active_operation_status,
            filter=unit.filter,
            unit_id=unit.id,
        )
        return self._transform_message(message)

    @with_exception
    async def get_devices(self) -> list[Union[DeviceResponseData, None]]:
        """Returns a list of connected devices

        Returns:
            list[Union[DeviceResponseData, None]]: List of devices
        """
        api = DevicesApi(api_client=self.api_client)
        devices: DevicesResponse = await api.devices_get(self.token)
        data: DevicesResponseData = devices.data
        devices = [
            dict_to_model(DeviceResponseData, device)
            for device in cast(Iterable[DeviceResponseData], data.values())
            if device["isConnected"]
        ]
        return devices

    @with_exception
    async def set_operation_status(self, unit_id: str, status: str):
        """
        Set the operation status of the device

        Args:
            unit_id (str): Unit ID
            status (str): Status
        """
        api_instance = UnitControlApi(api_client=self.api_client)
        status = self.operation_statuses.get_inverse(status)
        body = UnitControlSwitchesBody(status)

        # set unit operation status
        api_response = await api_instance.units_unit_id_controls_operation_statuses_put(
            x_access_token=self.token, body=body, unit_id=unit_id
        )

    @with_exception
    async def set_operation_mode(self, unit_id: str, mode: str):
        """
        Sets the operation mode of the HVAC unit

        Args:
            unit_id (str): The ID of the unit
            mode (str): The mode to set the unit to
        """
        api_instance = UnitControlApi(api_client=self.api_client)
        status = self.operation_modes.get_inverse(mode)
        body = UnitControlModesBody(status)

        api_response = await api_instance.units_unit_id_controls_operation_modes_put(
            x_access_token=self.token, body=body, unit_id=unit_id
        )

    @with_exception
    async def set_swing_mode(self, unit_id: str, mode: str):
        """Set the swing mode of the HVAC unit

        Args:
            unit_id (str): Unit ID
            mode (str): The swing mode to set on the device
        """
        api_instance = UnitControlApi(api_client=self.api_client)
        mode = self.swing_modes.get_inverse(mode)
        body = UnitControlSwingsBody(mode)

        api_response = await api_instance.units_unit_id_controls_swing_modes_put(
            x_access_token=self.token, body=body, unit_id=unit_id
        )

    @with_exception
    async def set_fan_mode(self, unit_id: str, mode: str):
        """Set the fan mode of the HVAC unit

        Args:
            unit_id (str): Unit ID
            mode (str): The fan mode to set on the device
        """
        api_instance = UnitControlApi(api_client=self.api_client)
        mode = self.fan_modes.get_inverse(mode)
        body = UnitControlFansBody(mode)

        api_response = await api_instance.units_unit_id_controls_fan_modes_put(
            x_access_token=self.token, body=body, unit_id=unit_id
        )

    @with_exception
    async def set_temperature_set_point(self, unit_id: str, temp: int):
        """Set the desired setpoint on the HVAC unit

        Args:
            unit_id (str): The identifier of the unit
            temp (int): The desired setpoint temperature
        """
        api_instance = UnitControlApi(self.api_client)
        body = UnitControlSetpointsBody(temp)

        api_response = await api_instance.units_unit_id_controls_setpoints_put(
            x_access_token=self.token, body=body, unit_id=unit_id
        )

    def register_for_updates(self, unit: Updatable):
        """Register an HVAC unit to receive updates from service calls or WebSocket

        Args:
            unit (Updatable): The identifier of the unit
        """
        self._registered_units[unit.get_updatable_id()] = unit

    def on_open_socket(self, ws):
        ws.send(f'{{"type":"authenticate","content":{{"token":"{self.token}"}}}}')

    def on_close_socket(self, ws: websocket.WebSocketApp, message: str) -> None:
        """Callback to handle close event of the socket
           function will attempt to reopen the socket

        Args:
            ws (websocket.WebSocketApp): active websocket
            message (str): message received from socket
        """
        self.logger.warning("Cool open client socket closed...")

    def on_message_socket(self, ws: websocket.WebSocketApp, message: str) -> None:
        """Callback to handle message received from socket

        Args:
            ws (websocket.WebSocketApp): active websocket
            message (str): message received from socket
        """

        try:
            loaded_json = json.loads(message)
            self.logger.debug("Message from socket: %s", message)
            self._handle_ping_pong(ws, loaded_json)
            self._handle_ws_message(loaded_json)
        except WebSocketException as error:
            self.logger.error("Error handling message from socket: %s", error)
            raise error
        except Exception as error:
            self.logger.error("Error handling message from socket: %s", error)
            raise error

    def _handle_ping_pong(self, ws: websocket.WebSocketApp, loaded_json: dict) -> None:
        """Handle ping pong message from websocket, return pong on ping
           with the correct format

        Args:
            ws (websocket.WebSocketApp): active websocket
            loaded_json (dict): dictionary with data loaded from the websocket message
        """
        self.logger.debug(
            "Entered Ping Pong Handler %s", loaded_json.get("type", "Not Ping Pong")
        )
        if loaded_json.get("type", None) == "ping":
            self.logger.debug("...Ping Pong...")
            ws.send('{"type":"pong"}')
        self.logger.debug("Exiting Ping Pong Handler")

    def _handle_ws_message(self, loaded_json: dict) -> None:
        """Handle update message from websocket
           Will handle all messages except fot ping

        Args:
            loaded_json (dict): dict baring data loaded from message json
        """
        self.logger.debug("Entered Message Handler %s", str(loaded_json))

        data = loaded_json.get("data", None)
        if data is not None:
            self.logger.debug("Received data from websocket: %s", str(data))
            update_message: UnitUpdateMessage = UnitUpdateMessageSchema().load(
                data, unknown=marshmallow.EXCLUDE
            )
            self.logger.debug("Update message: %s", update_message)
            if update_message is not None:
                unit = self._registered_units.get(update_message.unit_id)
                update_message = self._transform_message(update_message)
                if unit is not None:
                    unit.notify(update_message)
        self.logger.debug("Exiting Message Handler")

    def on_error_socket(self, ws: websocket.WebSocketApp, message: str) -> None:
        """Handle error from the websocket

        Args:
            ws (websocket.WebSocketApp): active websocket
            message (str): error message arriving from the socket

        Raises:
            WebSocketConnectionClosedException: Propagates received error
        """
        self.logger.error("Error from socket: %s", message)
        raise WebSocketConnectionClosedException()

    def open_socket(self) -> None:
        """
        Open a websocket to the CoolAutomationsServer
        """
        self.logger.debug("Entered open socket")

        if self.socket is not None and self.socket.sock.connected:
            self.socket.close()

        try:
            socket_params = {
                "url": self.SOCKET_URI,
                "on_open": self.on_open_socket,
                "on_message": self.on_message_socket,
                "on_error": self.on_error_socket,
                "on_close": self.on_close_socket,
            }
            self.ws_thread = WebSocketThread(socket_params, logger=self.logger)
            self.ws_thread.start()

        except WebSocketException as socket_exception:
            self.logger.error(
                "Exception when calling open socket: %s", socket_exception
            )

    def _transform_message(self, message: UnitUpdateMessage) -> UnitUpdateMessage:
        """Transform message from numeric type ids to string values

        Args:
            message (UnitUpdateMessage): update message object with numeric ids

        Returns:
            UnitUpdateMessage: update message object with string type values
        """
        message.fan_mode = self.fan_modes.get(message.fan_mode)
        message.swing = self.swing_modes.get(message.swing)
        message.operation_mode = self.operation_modes.get(message.operation_mode)
        message.operation_status = self.operation_statuses.get(message.operation_status)
        return message


class UnauthorizedException(Exception):
    pass


class InvalidTokenException(Exception):
    pass
