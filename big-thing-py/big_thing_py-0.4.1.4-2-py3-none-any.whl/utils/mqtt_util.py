from big_thing_py.utils.exception_util import *
from big_thing_py.utils.log_util import *
from big_thing_py.utils.json_util import *

import paho.mqtt.client as mqtt


def decode_MQTT_message(msg: mqtt.MQTTMessage = None, mode=dict) -> Tuple[str, dict]:
    try:
        topic: str = msg.topic
        payload: dict = msg.payload
        timestamp: float = msg.timestamp

        if type(msg.payload) == dict:
            payload: dict = msg.payload
        elif type(msg.payload) in [str, bytes]:
            payload: Union[str, dict] = json_string_to_dict(msg.payload)
            if payload is False:
                return topic, None, timestamp
        else:
            raise Exception('Unexpected type!!!')

        if type(payload) in [str, bytes]:
            return topic, str(msg.payload), timestamp
        if mode == dict:
            return topic, payload, timestamp
        elif mode == str:
            return topic, dict_to_json_string(payload), timestamp
        else:
            SOPLOG_DEBUG(f'Unexpected mode!!! : {mode}', 'red')
    except Exception as e:
        print_error(e)
        raise e


def encode_MQTT_message(topic: str, payload: str, timestamp: float = None) -> mqtt.MQTTMessage:
    try:
        msg = mqtt.MQTTMessage()
        msg.topic = bytes(topic, encoding='utf-8')
        msg.payload = dict_to_json_string(
            payload) if type(payload) == dict else payload
        msg.timestamp = timestamp

        return msg
    except Exception as e:
        print_error(e)
        raise e


def topic_split(topic: str):
    return topic.split('/')


def topic_join(topic: List[str]):
    return '/'.join(topic)


def unpack_mqtt_message(msg: mqtt.MQTTMessage) -> Tuple[List[str], str]:
    topic, payload, timestamp = decode_MQTT_message(msg, dict)
    topic = topic_split(topic)

    return topic, payload, timestamp


def pack_mqtt_message(topic_list: List[str], payload: str) -> mqtt.MQTTMessage:
    topic = topic_join(topic_list)
    msg = encode_MQTT_message(topic, payload)

    return msg
