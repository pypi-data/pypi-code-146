from big_thing_py.utils import *


def make_super_request_key(requester_middleware_name: str, scenario_name: str) -> str:
    return '@'.join([requester_middleware_name, scenario_name])


def make_sub_request_key(subfunction_name: str, reqline_order: int) -> str:
    return '@'.join([subfunction_name, str(reqline_order)])


def make_request_ID(requester_middleware_name: str, super_thing_name: str, super_function_name: str, subrequest_order: int):
    return '@'.join([requester_middleware_name, super_thing_name, super_function_name, str(subrequest_order)])


def argument_to_dict(arguments: list, scenario: str) -> Dict:
    dict_arguments = dict(scenario=scenario,
                          arguments=[])
    for i, arg in enumerate(arguments):
        dict_arguments['arguments'].append(dict(order=i, value=arg))

    return dict_arguments


class SoPMQTTMessage(metaclass=ABCMeta):
    def __init__(self) -> None:
        self._protocol_type: Union[SoPProtocolType.Base,
                                   SoPProtocolType.Super,
                                   SoPProtocolType.WebClient] = None
        self._timestamp: float = None

    @abstractmethod
    def topic(self):
        pass

    @abstractmethod
    def payload(self):
        pass

    def mqtt_message(self):
        return encode_MQTT_message(self.topic(), self.payload())

    def timestamp(self):
        return self._timestamp

    def set_timestamp(self, timestamp: float = None):
        if timestamp:
            self._timestamp = timestamp
        else:
            self._timestamp = time.time()


class SoPMQTTSendMessage(SoPMQTTMessage, metaclass=ABCMeta):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def topic(self):
        pass

    @abstractmethod
    def payload(self):
        pass


class SoPMQTTReceiveMessage(SoPMQTTMessage):
    def __init__(self, msg: mqtt.MQTTMessage) -> None:
        super().__init__()
        self._topic, self._payload, self._timestamp = decode_MQTT_message(msg)

    def topic(self):
        return self._topic

    def payload(self):
        return self._payload


class SoPRegisterMessage(SoPMQTTSendMessage):
    def __init__(self, thing_name: str, payload: dict) -> None:
        super().__init__()
        self._protocol_type = SoPProtocolType.Base.TM_REGISTER

        # topic
        self._thing_name = thing_name

        # payload
        self._payload = payload

    def topic(self):
        return self._protocol_type.value % (self._thing_name)

    def payload(self):
        return self._payload


##############################################################################################################################

class SoPRegisterResultMessage(SoPMQTTReceiveMessage):
    def __init__(self, msg: mqtt.MQTTMessage) -> None:
        super().__init__(msg)
        self._protocol_type = SoPProtocolType.Base.MT_RESULT_REGISTER

        # topic
        self._thing_name = self._topic.split('/')[3]

        # payload
        self._middleware_name: str = self._payload['middleware_name']
        self._error: SoPErrorType = SoPErrorType.get(self._payload['error'])


class SoPUnregisterMessage(SoPMQTTSendMessage):
    def __init__(self, thing_name: str) -> None:
        super().__init__()
        self._protocol_type = SoPProtocolType.Base.TM_UNREGISTER

        # topic
        self._thing_name = thing_name

        # payload
        self._payload = '{}'

    def topic(self):
        return self._protocol_type.value % (self._thing_name)

    def payload(self):
        return self._payload


class SoPUnregisterResultMessage(SoPMQTTReceiveMessage):
    def __init__(self, msg: mqtt.MQTTMessage) -> None:
        super().__init__(msg)
        self._protocol_type = SoPProtocolType.Base.MT_RESULT_UNREGISTER

        # topic
        self._thing_name: str = self._topic.split('/')[3]

        # payload
        self._error = self._payload['error']


class SoPExecuteMessage(SoPMQTTReceiveMessage):
    def __init__(self, msg: mqtt.MQTTMessage) -> None:
        super().__init__(msg)
        self._protocol_type = SoPProtocolType.Base.MT_EXECUTE

        # topic
        self._function_name: str = self._topic.split('/')[2]
        self._thing_name: str = self._topic.split('/')[3]
        # optional
        try:
            self._middleware_name: str = self._topic.split('/')[4]
            self._request_ID: str = self._topic.split('/')[5]
        except IndexError:
            self._middleware_name: str = ''
            self._request_ID: str = ''

        # payload
        self._scenario: str = self._payload['scenario']
        self._arguments: List[dict] = self._payload['arguments']

    def tuple_arguments(self):
        self._arguments = sorted(
            self._arguments, key=lambda x: int(x['order']))
        real_arguments = tuple([argument['value']
                               for argument in self._arguments])
        return real_arguments

    def dict_arguments(self):
        self._arguments = sorted(
            self._arguments, key=lambda x: int(x['order']))
        json_arguments = [dict(order=arg['order'], value=arg['value'])
                          for arg in self._arguments]
        return json_arguments


class SoPExecuteResultMessage(SoPMQTTSendMessage):
    def __init__(self, function_name: str, thing_name: str, scenario: str,
                 return_type: SoPType, return_value: Union[int, float, bool, str], error: SoPErrorType,
                 middleware_name: str = '', request_ID: str = '') -> None:
        super().__init__()
        self._protocol_type = SoPProtocolType.Base.TM_RESULT_EXECUTE

        # topic
        self._function_name = function_name
        self._thing_name = thing_name
        # optional
        self._middleware_name: str = middleware_name
        self._request_ID: str = request_ID

        # payload
        self._scenario = scenario
        self._return_type = return_type
        self._return_value = return_value
        self._error = error

    def topic(self):
        if self._middleware_name and self._request_ID:
            topic = self._protocol_type.value % (
                self._function_name, self._thing_name, self._middleware_name, self._request_ID)
        else:
            topic: str = (self._protocol_type.value % (
                self._function_name, self._thing_name, '', '')).rstrip('/')
        return topic

    def payload(self):
        return dict(error=self._error.value,
                    scenario=self._scenario,
                    return_type=self._return_type.value,
                    return_value=self._return_value)


class SoPBinaryValueResultMessage(SoPMQTTReceiveMessage):
    # TODO: binary 부분 구현 완료 후 재점검
    def __init__(self, thing_name, function_name, payload) -> None:
        super().__init__()
        self._protocol_type = SoPProtocolType.Base.MT_RESULT_BINARY_VALUE

        # topic
        self._thing_name = self._topic.split('/')[3]

        # payload
        self._value_name = self._payload['value_name']


class SoPAliveMessage(SoPMQTTSendMessage):
    def __init__(self, thing_name) -> None:
        super().__init__()
        self._protocol_type = SoPProtocolType.Base.TM_ALIVE

        # topic
        self._thing_name = thing_name

        # payload
        self._payload = '{}'

    def topic(self):
        return self._protocol_type.value % (self._thing_name)

    def payload(self):
        return self._payload


class SoPValueMessage(SoPMQTTSendMessage):
    def __init__(self, thing_name: str, value_name: str, payload: dict) -> None:
        super().__init__()
        self._protocol_type = SoPProtocolType.Base.TM_VALUE_PUBLISH

        # topic
        self._thing_name = thing_name
        self._value_name = value_name

        # payload
        self._type = SoPType.get(payload['type'])
        self._value = payload['value']

    def topic(self):
        return self._protocol_type.value % (self._thing_name, self._value_name)

    def payload(self):
        return dict(type=self._type.value, value=self._value)


# for middleware detect
class SoPServiceListResultMessage(SoPMQTTReceiveMessage):
    def __init__(self, msg: mqtt.MQTTMessage) -> None:
        super().__init__(msg)
        self._protocol_type = SoPProtocolType.WebClient.ME_RESULT_SERVICE_LIST

        # topic
        self._client_id = self._topic.split('/')[3]

        # payload


class SoPAvailablityMessage(SoPMQTTSendMessage):
    def __init__(self, super_thing_name: str, payload: dict) -> None:
        super().__init__()
        self._protocol_type = SoPProtocolType.Super.SM_AVAILABILITY

        # topic
        self._super_thing_name = super_thing_name

        # payload
        self._payload = payload

    def topic(self):
        return self._protocol_type.value % (self._super_thing_name)

    def payload(self):
        return self._payload


class SoPRefreshMessage(SoPMQTTSendMessage):
    def __init__(self, super_thing_name: str) -> None:
        super().__init__()
        self._protocol_type = SoPProtocolType.Super.SM_REFRESH

        # topic
        self._super_thing_name = super_thing_name

        # payload
        self._payload = '{}'

    def topic(self):
        return self._protocol_type.value % (self._super_thing_name)

    def payload(self):
        return self._payload


class SoPNotifyMessage(SoPMQTTReceiveMessage):
    def __init__(self, msg: mqtt.MQTTMessage) -> None:
        super().__init__(msg)
        self._protocol_type = SoPProtocolType.WebClient.ME_NOTIFY_CHANGE

        # topic
        self._client_id = self._topic.split('/')[2]

        # payload


class SoPServiceListResultMessage(SoPMQTTReceiveMessage):
    def __init__(self, msg: mqtt.MQTTMessage) -> None:
        super().__init__(msg)
        self._protocol_type = SoPProtocolType.Super.MS_RESULT_SERVICE_LIST

        # topic
        self._super_thing_name: str = self._topic.split('/')[3]

        # payload
        self._services: List[dict] = self._payload['services']

    def service_list(self):
        return self._services


class SoPSuperScheduleMessage(SoPMQTTReceiveMessage):
    def __init__(self, msg: mqtt.MQTTMessage) -> None:
        super().__init__(msg)
        self._protocol_type = SoPProtocolType.Super.MS_SCHEDULE

        # topic
        self._super_function_name = self._topic.split('/')[2]
        self._super_thing_name = self._topic.split('/')[3]
        self._super_middleware_name = self._topic.split('/')[4]
        self._requester_middleware_name = self._topic.split('/')[5]

        # payload
        self._scenario = self._payload['scenario']
        self._period = self._payload['period']


class SoPSuperScheduleResultMessage(SoPMQTTSendMessage):
    def __init__(self, super_function_name: str, super_thing_name: str, super_middleware_name: str, requester_middleware_name: str,
                 scenario: str, error: SoPErrorType) -> None:
        super().__init__()
        self._protocol_type = SoPProtocolType.Super.SM_RESULT_SCHEDULE

        # topic
        self._super_function_name = super_function_name
        self._super_thing_name = super_thing_name
        self._super_middleware_name = super_middleware_name
        self._requester_middleware_name = requester_middleware_name

        # payload
        self._scenario = scenario
        self._error = error

    def topic(self):
        return self._protocol_type.value % (self._super_function_name, self._super_thing_name, self._super_middleware_name, self._requester_middleware_name)

    def payload(self):
        return dict(scenario=self._scenario, error=self._error.value)


class SoPSubScheduleMessage(SoPMQTTSendMessage):
    def __init__(self, subfunction_name: str, target_thing_name: str, target_middleware_name: str,
                 requester_middleware_name: str = None, super_thing_name: str = None, super_function_name: str = None, subrequest_order: int = None,
                 scenario: str = None, period: float = None,
                 request_ID: str = None, status: str = None) -> None:
        super().__init__()
        self._protocol_type = SoPProtocolType.Super.SM_SCHEDULE

        # topic
        self._subfunction_name = subfunction_name
        self._target_thing_name = target_thing_name
        self._target_middleware_name = target_middleware_name

        self._requester_middleware_name = requester_middleware_name
        self._super_thing_name = super_thing_name
        self._super_function_name = super_function_name
        self._subrequest_order = subrequest_order
        self._status: str = status  # 'check' or 'confirm'

        if request_ID:
            self._request_ID = request_ID
        else:
            self._request_ID = make_request_ID(
                self._requester_middleware_name, self._super_thing_name, self._super_function_name, self._subrequest_order)

        # payload
        self._scenario = scenario
        self._period = period

    def topic(self):
        return self._protocol_type.value % (self._subfunction_name, self._target_thing_name, self._target_middleware_name, self._request_ID)

    def payload(self):
        return dict(scenario=self._scenario, period=self._period, status=self._status)


class SoPSubScheduleResultMessage(SoPMQTTReceiveMessage):
    def __init__(self, msg: mqtt.MQTTMessage) -> None:
        super().__init__(msg)
        self._protocol_type = SoPProtocolType.Super.MS_RESULT_SCHEDULE

        # topic
        self._subfunction_name = self._topic.split('/')[3]
        self._target_thing_name = self._topic.split('/')[4]
        self._target_middleware_name = self._topic.split('/')[5]

        self._request_ID = self._topic.split('/')[6]
        self._requester_middleware_name = self._request_ID.split('@')[0]
        self._super_thing_name = self._request_ID.split('@')[1]
        self._super_function_name = self._request_ID.split('@')[2]
        self._subrequest_order = self._request_ID.split('@')[3]

        # payload
        self._scenario = self._payload['scenario']
        self._error = SoPErrorType.get(self._payload['error'])
        self._status: str = self._payload.get(
            'status', None)  # 'check' or 'confirm'


class SoPSuperExecuteMessage(SoPMQTTReceiveMessage):
    def __init__(self, msg: mqtt.MQTTMessage) -> None:
        super().__init__(msg)
        self._protocol_type = SoPProtocolType.Super.MS_EXECUTE

        # topic
        self._super_function_name = self._topic.split('/')[2]
        self._super_thing_name = self._topic.split('/')[3]
        self._super_middleware_name = self._topic.split('/')[4]
        self._requester_middleware_name = self._topic.split('/')[5]

        # payload
        self._scenario = self._payload['scenario']
        self._arguments = self._payload['arguments']

    def tuple_arguments(self):
        self._arguments = sorted(
            self._arguments, key=lambda x: int(x['order']))
        real_arguments = tuple([argument['value']
                               for argument in self._arguments])
        return real_arguments

    def dict_arguments(self):
        self._arguments = sorted(
            self._arguments, key=lambda x: int(x['order']))
        json_arguments = [dict(order=arg['order'], value=arg['value'])
                          for arg in self._arguments]
        return json_arguments


class SoPSuperExecuteResultMessage(SoPMQTTSendMessage):
    def __init__(self, super_function_name: str, super_thing_name: str, super_middleware_name: str, requester_middleware_name: str,
                 scenario: str, return_type: SoPType, return_value: Union[int, float, bool, str], error: SoPErrorType) -> None:
        super().__init__()
        # SM/RESULT/EXECUTE/[SuperFunctionName]/[SuperThingName]/[MiddlewareName]/[RequesterMWName]
        self._protocol_type = SoPProtocolType.Super.SM_RESULT_EXECUTE

        # topic
        self._super_function_name = super_function_name
        self._super_thing_name = super_thing_name
        self._super_middleware_name = super_middleware_name
        self._requester_middleware_name = requester_middleware_name

        # payload
        self._scenario = scenario
        self._return_type = return_type
        self._return_value = return_value
        self._error = error

    def topic(self):
        return self._protocol_type.value % (self._super_function_name, self._super_thing_name, self._super_middleware_name, self._requester_middleware_name)

    def payload(self):
        return dict(scenario=self._scenario,
                    return_type=self._return_type.value,
                    return_value=self._return_value,
                    error=self._error.value)


class SoPSubExecuteMessage(SoPMQTTSendMessage):
    def __init__(self, subfunction_name: str, target_thing_name: str, target_middleware_name: str,
                 requester_middleware_name: str = None, super_thing_name: str = None, super_function_name: str = None, subrequest_order: int = None,
                 scenario: str = None, arguments: List[dict] = None,
                 request_ID: str = None) -> None:
        super().__init__()
        self._protocol_type = SoPProtocolType.Super.SM_EXECUTE

        # topic
        self._subfunction_name = subfunction_name
        self._target_thing_name = target_thing_name
        self._target_middleware_name = target_middleware_name

        self._requester_middleware_name = requester_middleware_name
        self._super_thing_name = super_thing_name
        self._super_function_name = super_function_name
        self._subrequest_order = subrequest_order
        if request_ID:
            self._request_ID = request_ID
        else:
            self._request_ID = make_request_ID(
                self._requester_middleware_name, self._super_thing_name, self._super_function_name, self._subrequest_order)

        # payload
        self._scenario = scenario
        self._arguments = arguments

    def topic(self):
        return self._protocol_type.value % (self._subfunction_name, self._target_thing_name, self._target_middleware_name, self._request_ID)

    def payload(self):
        return dict(scenario=self._scenario, arguments=self._arguments)

    def json_arguments(self):
        self._arguments = sorted(
            self._arguments, key=lambda x: int(x['order']))
        json_arguments = [dict(order=arg['order'], value=arg['value'])
                          for arg in self._arguments]
        return json_arguments


class SoPSubExecuteResultMessage(SoPMQTTReceiveMessage):
    def __init__(self, msg: mqtt.MQTTMessage) -> None:
        super().__init__(msg)
        self._protocol_type = SoPProtocolType.Super.MS_RESULT_EXECUTE

        # topic
        self._subfunction_name = self._topic.split('/')[3]
        self._target_thing_name = self._topic.split('/')[4]
        self._target_middleware_name = self._topic.split('/')[5]

        self._request_ID = self._topic.split('/')[6]
        self._requester_middleware_name = self._request_ID.split('@')[0]
        self._super_thing_name = self._request_ID.split('@')[1]
        self._super_function_name = self._request_ID.split('@')[2]
        self._subrequest_order = self._request_ID.split('@')[3]

        # payload
        self._scenario = self._payload['scenario']
        self._return_type = self._payload['return_type']
        self._return_value = self._payload['return_value']
        self._error = SoPErrorType.get(self._payload['error'])

    def tuple_arguments(self):
        self._arguments = sorted(
            self._arguments, key=lambda x: int(x['order']))
        real_arguments = tuple([argument['value']
                               for argument in self._arguments])
        return real_arguments

    def dict_arguments(self):
        self._arguments = sorted(
            self._arguments, key=lambda x: int(x['order']))
        json_arguments = [dict(order=arg['order'], value=arg['value'])
                          for arg in self._arguments]
        return json_arguments


if __name__ == '__main__':
    payload = {
        'scenario': 'test',
        'arguments': [
            {
                'order': 0,
                'value': 1,
            },
            {
                'order': 1,
                'value': 2,
            }
        ]
    }
    msg = encode_MQTT_message('MT/EXECUTE/test1/test2', payload)
    message = SoPExecuteMessage(msg)
    print(message.tuple_arguments())
    print(message.dict_arguments(*(1, 2)))
