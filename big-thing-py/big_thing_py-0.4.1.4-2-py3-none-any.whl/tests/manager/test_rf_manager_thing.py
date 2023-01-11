import big_thing.utils as utils
from big_thing.utils import (
    encode_MQTT_message,
    decode_MQTT_message,
    dict_to_json_string,
    json_string_to_dict,
    get_current_time,
    type_converter,
    get_function_return_type,
    get_function_parameter,
    get_ip_from_url)

from big_thing.SoPTag import SoPTag
from big_thing.SoPArgument import SoPArgument
from big_thing.SoPFunction import SoPFunction
from big_thing.SoPValue import SoPValue
from big_thing.SoPThing import SoPThing
from sample_class.manager_client.HueManagerClient import SoPHueManagerClient

from typing import *
from threading import Thread, Event, current_thread
from functools import singledispatch
from queue import Queue
from time import sleep, time
import json

from termcolor import colored, cprint
import paho.mqtt.client as mqtt
import pytest


def test_manager_client_init():
    client = SoPHueManagerClient(ip='iotdev.snu.ac.kr', port=11883,
                                 bridge_ip='http://147.46.114.24/api/', bridge_port=80,
                                 user_key='L-idzo6XFfRVA-DzXyA66xKzi-KxIJA75neakYyS',
                                 refresh_cycle=5,)
    assert client.setup()
    assert client.run(timeout=5)
    assert client.wrapup()


cnt = 3


def test_manager_client_run():
    global cnt

    client = SoPHueManagerClient(ip='iotdev.snu.ac.kr', port=11883,
                                 bridge_ip='http://147.46.114.24/api/', bridge_port=80,
                                 user_key='L-idzo6XFfRVA-DzXyA66xKzi-KxIJA75neakYyS',
                                 refresh_cycle=5,)
    assert client.setup()

    execute_event: Event = Event()
    execute_thread: Thread = Thread(
        target=client.run, daemon=True, kwargs={'stop_event': execute_event, 'timeout': 20, })
    execute_thread.start()
    base_run_time = 2

    sleep(1)

    on_func_test = []
    for i in range(0, 3):
        on_func_test.append({'time': base_run_time,
                             'published': False,
                             'topic': f'MT/on/{client._thing_list[i].get_name()}',
                             'payload': dict_to_json_string(
                                 {
                                     "scenario": "scenario_name",
                                     "arguments":
                                     [
                                     ]
                                 })
                             })
    base_run_time += 0.5

    off_func_test = []
    for i in range(0, 3):
        off_func_test.append({'time': base_run_time,
                              'published': False,
                              'topic': f'MT/off/{client._thing_list[i].get_name()}',
                              'payload': dict_to_json_string(
                                  {
                                      "scenario": "scenario_name",
                                      "arguments":
                                      [
                                      ]
                                  })
                              })
    base_run_time += 0.5

    set_brightness_func_test = []
    for i in range(0, 3):
        set_brightness_func_test.append({'time': base_run_time,
                                         'published': False,
                                         'topic': f'MT/set_brightness/{client._thing_list[i].get_name()}',
                                         'payload': dict_to_json_string(
                                             {
                                                 "scenario": "scenario_name",
                                                 "arguments":
                                                 [
                                                     {
                                                         "order": 0,
                                                         "value": 50
                                                     }
                                                 ]
                                             })
                                         })
    base_run_time += 0.5

    # set_color_func_test = {'time': 3.5,
    #                        'published': False,
    #                        'topic': f'MT/set_color/{client._thing_list[5].get_name()}',
    #                        'payload': dict_to_json_string(
    #                            {
    #                                "scenario": "scenario_name",
    #                                "arguments":
    #                                [
    #                                    {
    #                                        "order": 0,
    #                                        "value": 50
    #                                    }
    #                                ]
    #                            })
    #                        }

    test_func_list: dict = on_func_test + off_func_test + set_brightness_func_test

    cnt = len(test_func_list)

    def on_message(client, userdata: Callable, msg: mqtt.MQTTMessage):
        global cnt
        topic, payload = decode_MQTT_message(msg)
        if 'TM/RESULT/FUNCTION/' in topic:
            cnt -= 1
            print(f'cnt : {cnt}')

    dummy_client = mqtt.Client(userdata=cnt)
    dummy_client.on_message = on_message
    dummy_client.connect(get_ip_from_url('iotdev.snu.ac.kr'), 11883)
    for func in test_func_list:
        function_name: str = func['topic']
        function_name = function_name.split('/')[1]
        for i in range(0, 3):
            dummy_client.subscribe(
                f'TM/RESULT/FUNCTION/{function_name}/{client._thing_list[i].get_name()}')
    dummy_client.loop_start()

    cur_time = get_current_time()
    timeout = 20

    while get_current_time() - cur_time < timeout:
        if client._alive_event.is_set():
            assert client.wrapup()
            assert False, 'alive_event set'
        if client._register_event.is_set():
            assert client.wrapup()
            assert False, 'register_event set'
        if client._value_publish_event.is_set():
            assert client.wrapup()
            assert False, 'value_publish_event set'
        if client._function_actuate_event.is_set():
            assert client.wrapup()
            assert False, 'function_actuate_event set'
        if client._function_actuate_result_event.is_set():
            assert client.wrapup()
            assert False, 'function_actuate_result_event set'
        if client._receive_message_event.is_set():
            assert client.wrapup()
            assert False, 'handle_recv_mqtt_event set'

        for func in test_func_list:
            if (get_current_time() - cur_time) > func['time'] and not func['published']:
                dummy_client.publish(
                    func['topic'], func['payload'])
                func['published'] = True

        if cnt == 0:
            print('function actuate test pass!!!')
            execute_event.set()
            assert client.wrapup()
            break
    else:
        assert False, 'timeout...'


def test_rf():
    radio = RF24(22, 0)

    if not radio.begin():
        raise RuntimeError("radio hardware is not responding")

    address = [0xFFFFFFFFFFF0, 0xFFFFFFFFFFF1]
    radio.setPALevel(RF24_PA_LOW)  # RF24_PA_MAX is default
    radio.payloadSize = 4
    radio.openWritingPipe(address[1])  # always uses pipe 0
    radio.openReadingPipe(1, address[0])  # using pipe 1
    radio.startListening()

    radio.printPrettyDetails()

    start_timer = time.time()
    while (time.time() - start_timer) < 5:
        has_payload, pipe = radio.available_pipe()
        if has_payload:
            length = radio.getDynamicPayloadSize()
            buffer = radio.read(length)
            print(f"Received {32} bytes on pipe 1: {buffer}")
            start_timer = time.monotonic()  # reset the timeout timer
    radio.stopListening()  # put the radio in TX mode

# def slave(timeout=5):
#     radio.startListening()

#     start_timer = time.monotonic()
#     while (time.monotonic() - start_timer) < timeout:
#         has_payload, pipe_number = radio.available_pipe()
#         if has_payload:
#             length = radio.getDynamicPayloadSize()
#             received = radio.read(length)
#             print(f"Received {received}")

#             if 'REG' in str(received):
#                 time.sleep(0.5)
#                 random_number = random.randint(0, 0xFFFF)
#                 random_number = hex(random_number)
#                 random_number = random_number[2:].upper()
#                 buffer = bytearray(f'RACK{random_number}'.encode('utf-8'))
#                 radio.stopListening()
#                 print('send REGACK')
#                 radio.write(buffer)
#                 radio.startListening()

#     print("Nothing received in", timeout, "seconds. Leaving RX role")
#     radio.stopListening()
