from big_thing_py.common.request import *
from big_thing_py.core.thing import *

import paho.mqtt.client as mqtt
from paho.mqtt.client import Client as SoPClient
from zeroconf import IPVersion, ServiceBrowser, ServiceStateChange, Zeroconf, ZeroconfServiceTypes
import ssl
import argparse

# ======================================================================
#  _____        ______ ______  _         _____  _      _
# /  ___|       | ___ \| ___ \(_)       |_   _|| |    (_)
# \ `--.   ___  | |_/ /| |_/ / _   __ _   | |  | |__   _  _ __    __ _
#  `--. \ / _ \ |  __/ | ___ \| | / _` |  | |  | '_ \ | || '_ \  / _` |
# /\__/ /| (_) || |    | |_/ /| || (_| |  | |  | | | || || | | || (_| |
# \____/  \___/ \_|    \____/ |_| \__, |  \_/  |_| |_||_||_| |_| \__, |
#                                  __/ |                          __/ |
#                                 |___/                          |___/
# ======================================================================


class SoPBigThing(SoPThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True,
                 ip: str = None, port: int = None, ssl_ca_path: str = None, ssl_enable: bool = False, log_name: str = None, log_enable: bool = True, log_mode: SoPPrintMode = SoPPrintMode.ABBR, append_mac_address: bool = True):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel)

        self._log_mode = log_mode
        if log_enable:
            START_LOGGER(whole_log_path=log_name,
                         logging_mode=SoPLogger.LoggingMode.ALL)
        else:
            START_LOGGER(logging_mode=SoPLogger.LoggingMode.OFF)

        # MQTT
        self._connected = False
        self._ip: str = get_ip_from_url(ip.strip())
        self._port: int = port
        self._mac_address: str = get_mac_address()
        self._ssl_ca_path: str = ssl_ca_path
        self._ssl_enable: bool = ssl_enable
        self._avahi_discovered_middleware_list: List[str] = []
        self._avahi_middleware_name = None

        self._g_exit: Event = Event()
        self._g_comm_exit: Event = Event()
        self._comm_thread_list: List[SoPThread] = []
        self._thread_list: List[SoPThread] = []

        # Queue
        self._receive_queue: Queue = Queue()
        self._publish_queue: Queue = Queue()

        self._thread_comm_func_list: List[Callable] = [
            self._receive_message_thread_func,
            self._publish_message_thread_func,]
        self._thread_func_list: List[Callable] = [
            self._alive_thread_func,
            self._value_publish_thread_func,
        ]

        if append_mac_address:
            self._name = self._name + f'_{self._mac_address}'
        else:
            pass
        self._mqtt_client = SoPClient(userdata=None, client_id=self._name)

        for function in self._function_list:
            function.set_publish_queue(self._publish_queue)

    def __eq__(self, o: object) -> bool:
        is_parallel_check = (self._is_parallel == o._is_parallel)
        is_super_check = (self._is_super == o._is_super)

        return super().__eq__(o) and is_parallel_check and is_super_check

    def setup(self, avahi_enable=True):
        try:
            self._avahi_enable = avahi_enable
            self._avahi_init(avahi_enable)
            if self._ssl_enable == True:
                self._set_ssl_config()
            else:
                SOPLOG_DEBUG('SSL is not enabled...')
            self._connect()

            # receive, publish쓰레드는 나머지 쓰레드들과 분리하여 exit event를 설정
            # wrapup 할 때 나머지 쓰레드들은 한꺼번에 종료가 되어도 되지만, receive, publish 쓰레드는
            # receive, publish queue에 남아있는 메시지를 모두 전송, 처리하고 종료되어야 하기 때문에
            # exit event를 따로 설정하여 종료시킴
            for func in self._thread_comm_func_list:
                thread = SoPThread(func=func, arg_list=(self._g_comm_exit, ))
                self._comm_thread_list.append(thread)
            for func in self._thread_func_list:
                thread = SoPThread(func=func, arg_list=(self._g_exit, ))
                self._thread_list.append(thread)

            return True
        except KeyboardInterrupt:
            SOPLOG_DEBUG('Ctrl + C Exit', 'red')
            return self.wrapup()
        except ConnectionRefusedError:
            SOPLOG_DEBUG(
                'Connection error while connect to broker. Check ip and port', 'red')
            return self.wrapup()
        except Exception as e:
            print_error(e)
            return self.wrapup()

    def run(self):

        def try_register_once():
            SOPLOG_DEBUG(f'Register send', 'yellow')
            self._subscribe_init_topics(self)
            self._send_TM_REGISTER(
                thing_name=self._name, payload=self.dump())

            while not self._registered:
                time.sleep(THREAD_TIME_OUT)

        def try_register_cyclic(period: float = 10, retry: int = 5):
            while not self._registered and retry:
                SOPLOG_DEBUG(f'Register try {6-retry}', 'yellow')
                retry -= 1

                self._subscribe_init_topics(self)
                self._send_TM_REGISTER(
                    thing_name=self._name, payload=self.dump())

                current_time = get_current_time()
                while get_current_time() - current_time < period:
                    if self._registered:
                        break
                    else:
                        time.sleep(THREAD_TIME_OUT)

        try:
            # Start main threads
            for thread in self._comm_thread_list + self._thread_list:
                thread.start()

            try_register_cyclic(period=10, retry=5)
            # try_register_once()

            # Maintain main thread
            while not self._g_exit.wait(THREAD_TIME_OUT):
                time.sleep(1000)
        except KeyboardInterrupt as e:
            SOPLOG_DEBUG('Ctrl + C Exit', 'red')
            return self.wrapup()
        except ConnectionRefusedError as e:
            SOPLOG_DEBUG(
                'Connection error while connect to broker. Check ip and port', 'red')
            return self.wrapup()
        except Exception as e:
            print_error(e)
            return self.wrapup()

    def wrapup(self):
        try:
            self._send_TM_UNREGISTER(self._name)
            cur_time = get_current_time()

            self._g_exit.set()
            for thread in self._thread_list:
                thread.join()
                SOPLOG_DEBUG(f'{thread._name} is terminated', 'yellow')

            while not ((self._publish_queue.empty() and self._receive_queue.empty()) or (get_current_time() - cur_time > 3)):
                time.sleep(THREAD_TIME_OUT)

            self._g_comm_exit.set()
            for thread in self._comm_thread_list:
                thread.join()
                SOPLOG_DEBUG(f'{thread._name} is terminated', 'yellow')

            self._mqtt_client.disconnect()
            SOPLOG_DEBUG('Thing Exit', 'red')
            return True
        except Exception as e:
            print_error(e)
            return False

    def arg_parse():
        parser = argparse.ArgumentParser()
        parser.add_argument("--name", '-n', action='store', type=str,
                            required=False, default='big_thing', help="Thing name")
        parser.add_argument("--host", '-ip', action='store', type=str,
                            required=False, default='127.0.0.1', help="Thing host")
        parser.add_argument("--port", '-p', action='store', type=int,
                            required=False, default=1883, help="Thing port")
        parser.add_argument("--alive_cycle", '-alive', action='store', type=int,
                            required=False, default=60, help="Thing alive cycle. Thing will send alive message every alive cycle period")
        parser.add_argument("--auto_scan", '-auto', action='store_true', type=bool,
                            required=False, help="Enable auto middleware scan feature")
        parser.add_argument("--log_enable", '-log', action='store_true', type=bool,
                            required=False, help="Enable log save")
        parser.add_argument("--log_path",  action='store_true', type=str,
                            required=False, help="Specify log path")
        parser.add_argument("--ssl_enable", '-ssl', action='store_true', type=bool,
                            required=False, help="Enable ssl connection")
        parser.add_argument("--ssl_ca_path", action='store_true', type=bool,
                            required=False, help="Specify ssl CA file folder path")
        parser.add_argument("--append_mac_address", action='store_true', type=bool,
                            required=False, help="Whether to include a mac address in big thing name")
        args = parser.parse_args()

        return args

    # ===========================================================================================
    #  _    _                             _    __                      _    _
    # | |  | |                           | |  / _|                    | |  (_)
    # | |_ | |__   _ __   ___   __ _   __| | | |_  _   _  _ __    ___ | |_  _   ___   _ __   ___
    # | __|| '_ \ | '__| / _ \ / _` | / _` | |  _|| | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|
    # | |_ | | | || |   |  __/| (_| || (_| | | |  | |_| || | | || (__ | |_ | || (_) || | | |\__ \
    #  \__||_| |_||_|    \___| \__,_| \__,_| |_|   \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/
    # ===========================================================================================

    def _receive_message_thread_func(self, stop_event: Event):
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                if self._receive_queue.empty():
                    continue

                recv_msg = self._receive_queue.get()
                self._handle_mqtt_message(recv_msg)
        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    def _publish_message_thread_func(self, stop_event: Event):
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                if self._publish_queue.empty():
                    continue

                pub_msg = self._publish_queue.get()
                topic, payload, timestamp = decode_MQTT_message(
                    pub_msg, mode=str)
                self._publish(topic, payload)
        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    def _alive_thread_func(self, stop_event: Event) -> Union[bool, None]:
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                if self._registered:
                    current_time = get_current_time()
                    if current_time - self._last_alive_time > self._alive_cycle:
                        self._send_TM_ALIVE(thing_name=self._name)
                        self._last_alive_time = current_time
                else:
                    pass

        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    def _value_publish_thread_func(self, stop_event: Event) -> Union[bool, None]:
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                if not self._registered:
                    continue
                current_time = get_current_time()
                for value in self._value_list:
                    if not (current_time - value.get_last_update_time()) > value.get_cycle():
                        continue
                    arg_list = tuple(value.get_arg_list())
                    if value.update(*arg_list) is not None:
                        self._send_TM_VALUE_PUBLISH(
                            self._name, value.get_name(), value.dump_pub())
        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    # ====================================================================================================================
    #  _                        _  _        ___  ___ _____  _____  _____
    # | |                      | || |       |  \/  ||  _  ||_   _||_   _|
    # | |__    __ _  _ __    __| || |  ___  | .  . || | | |  | |    | |    _ __ ___    ___  ___  ___   __ _   __ _   ___
    # | '_ \  / _` || '_ \  / _` || | / _ \ | |\/| || | | |  | |    | |   | '_ ` _ \  / _ \/ __|/ __| / _` | / _` | / _ \
    # | | | || (_| || | | || (_| || ||  __/ | |  | |\ \/' /  | |    | |   | | | | | ||  __/\__ \\__ \| (_| || (_| ||  __/
    # |_| |_| \__,_||_| |_| \__,_||_| \___| \_|  |_/ \_/\_\  \_/    \_/   |_| |_| |_| \___||___/|___/ \__,_| \__, | \___|
    #                                                                                                         __/ |
    #                                                                                                        |___/
    # ====================================================================================================================

    def _handle_mqtt_message(self, msg: mqtt.MQTTMessage) -> None:
        topic, payload, timestamp = unpack_mqtt_message(msg)
        msg.timestamp = time.time()

        if topic[0] == 'MT':
            if topic[1] == 'RESULT':
                if topic[2] == 'REGISTER':
                    self._handle_MT_RESULT_REGISTER(msg)
                elif topic[2] == 'UNREGISTER':
                    self._handle_MT_RESULT_UNREGISTER(msg)
                elif topic[2] == 'BINARY_VALUE':
                    self._handle_MT_RESULT_BINARY_VALUE(msg)
                else:
                    SOPLOG_DEBUG(
                        f'[handle_mqtt_message] Unexpected MT_RESULT topic! topic: {topic}')
            elif topic[1] == 'EXECUTE':
                self._handle_MT_EXECUTE(msg)
            else:
                SOPLOG_DEBUG(
                    f'[handle_mqtt_message] Unexpected MT topic! topic: {topic}')

            return True
        else:
            return False

    # ===============
    # ___  ___ _____
    # |  \/  ||_   _|
    # | .  . |  | |
    # | |\/| |  | |
    # | |  | |  | |
    # \_|  |_/  \_/
    # ===============

    def _handle_MT_RESULT_REGISTER(self, msg: mqtt.MQTTMessage):
        register_result_msg = SoPRegisterResultMessage(msg)
        if not self._name == register_result_msg._thing_name:
            SOPLOG_DEBUG(
                f'Wrong payload arrive... {self._name} should be arrive, not {register_result_msg._thing_name}', 'red')
            raise

        if self._check_register_result(register_result_msg._error):
            self._middleware_name = register_result_msg._middleware_name
            self._registered = True
            self._subscribe_service_topics(self)
        else:
            SOPLOG_DEBUG(
                f'[handle_MT_RESULT_REGISTER] Register failed... error code : {register_result_msg._error}')

    def _handle_MT_RESULT_UNREGISTER(self, msg: mqtt.MQTTMessage):
        unregister_result_msg = SoPUnregisterResultMessage(msg)
        if not self._name == unregister_result_msg._thing_name:
            SOPLOG_DEBUG(
                f'Wrong payload arrive... {self._name} should be arrive, not {unregister_result_msg._thing_name}', 'red')
            raise

        if self._check_register_result(unregister_result_msg._error):
            self._registered = False
            self._unsubscrube_all_topics(self)
        else:
            SOPLOG_DEBUG(
                f'[handle_MT_RESULT_UNREGISTER] Unregister failed... error code : {unregister_result_msg._error}')

    def _handle_MT_EXECUTE(self, msg: mqtt.MQTTMessage):
        execute_msg = SoPExecuteMessage(msg)
        execute_request = SoPExecuteRequest(
            trigger_msg=execute_msg)
        execute_request.timer_start()

        # 만약 타켓 함수를 얻는데 성공했다면 병렬실행이 가능한지 옵션을 살펴보고, 이후에 실행 중인지 살펴본다.
        target_function = self._find_function(execute_msg._function_name)
        if target_function:
            if self._is_parallel:
                target_function.execute(execute_request)
                return True
            else:
                if not target_function._running:
                    target_function.execute(execute_request)
                    return True
                else:
                    # TODO: 계속 도는게 아니라 FAILED를 보내야함
                    while not target_function._running:
                        SOPLOG_DEBUG(
                            f'Wait for finish Function {execute_request._trigger_msg._function_name} execute...', 'yellow')
                        time.sleep(0.1)
                    target_function.execute(execute_request)
                    return True
        else:
            return False

    # TODO: complete this function
    def _handle_MT_RESULT_BINARY_VALUE(self, msg: mqtt.MQTTMessage) -> None:
        SOPLOG_DEBUG(
            '[handle_mqtt_message] MT_RESULT_BINARY_VALUE is not implemented yet!')

    ############################################################################################################

    # TODO: implement auto reregister feature
    # for middleware detect and reregister
    # def handle_ME_SERVICE_LIST(self, msg: mqtt.MQTTMessage) -> None:
    #     service_list_msg = SoPServiceListResultMessage(msg)

    #     self.send_TM_REGISTER(self._name, self.dump())

    # ===============
    #  _____ ___  ___
    # |_   _||  \/  |
    #   | |  | .  . |
    #   | |  | |\/| |
    #   | |  | |  | |
    #   \_/  \_|  |_/
    # ===============

    def _send_TM_REGISTER(self, thing_name: str, payload: dict) -> None:
        self._publish_queue.put(SoPRegisterMessage(
            thing_name, payload).mqtt_message())

    def _send_TM_UNREGISTER(self, thing_name: str):
        self._publish_queue.put(
            SoPUnregisterMessage(thing_name).mqtt_message())

    def _send_TM_ALIVE(self, thing_name: str):
        self._publish_queue.put(SoPAliveMessage(thing_name).mqtt_message())

    def _send_TM_VALUE_PUBLISH(self, thing_name, value_name: str, payload: dict) -> None:
        self._publish_queue.put(SoPValueMessage(
            thing_name, value_name, payload).mqtt_message())

    def _send_TM_RESULT_EXECUTE(self, function_name: str, thing_name: str,
                                return_type: SoPType, return_value: Union[str, float, bool], scenario: str, error: SoPErrorType,
                                middleware_name: str = '', request_ID: str = '') -> None:
        self._publish_queue.put(SoPExecuteResultMessage(
            function_name, thing_name, scenario, return_type, return_value, error, middleware_name=middleware_name, request_ID=request_ID).mqtt_message())

    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    def _subscribe_init_topics(self, thing: SoPThing):
        topic_list = [
            SoPProtocolType.Base.MT_RESULT_REGISTER.value % thing.get_name(),
            SoPProtocolType.Base.MT_RESULT_UNREGISTER.value % thing.get_name(),
            SoPProtocolType.Base.MT_RESULT_BINARY_VALUE.value % thing.get_name()]

        # TODO: implement auto reregister feature
        # for middleware detect
        # topic_list.append(
        #     SoPProtocolType.WebClient.ME_RESULT_SERVICE_LIST.value % ('#'))

        for topic in topic_list:
            self._subscribe(topic, thing=thing)

    def _subscribe_service_topics(self, thing: SoPThing):
        topic_list = []

        for function in thing.get_function_list():
            topic_list += [SoPProtocolType.Base.MT_EXECUTE.value % (function.get_name(), thing.get_name(), '+', '#'),
                           (SoPProtocolType.Base.MT_EXECUTE.value % (function.get_name(), thing.get_name(), '', '')).rstrip('/')]

        for topic in topic_list:
            self._subscribe(topic, thing=thing)

    def _unsubscrube_all_topics(self, thing: SoPThing):
        # whenever _unsubscribe function execute, it remove target topic from self._subscribed_topic_set
        # so it need to iterate with copy of self._subscribed_topic_set
        target_topic_list = list(thing.get_subscribed_topic_set())
        for topic in target_topic_list:
            self._unsubscribe(topic, thing=thing)

    def _check_register_result(self, error: SoPErrorType, thing: SoPThing = None):
        if not isinstance(error, SoPErrorType):
            error = SoPErrorType.get(error)
        if not thing:
            thing = self

        if error == SoPErrorType.NO_ERROR:
            SOPLOG_DEBUG(
                f'{PrintTag.GOOD} Thing {thing.get_name()} register success!')
            return True
        elif error == SoPErrorType.DUPLICATE:
            SOPLOG_DEBUG(
                f'{PrintTag.DUP} Thing {thing.get_name()} register success!')
            return True
        elif error == SoPErrorType.FAIL:
            SOPLOG_DEBUG(
                f'{PrintTag.ERROR} Thing {thing.get_name()} register packset was nonvaild')
            return False
        else:
            SOPLOG_DEBUG(
                f'[MT_message_parser] Unexpected error occured!!!', 'red')
            return False

    def _print_packet(self, msg: mqtt.MQTTMessage, mode: SoPPrintMode = SoPPrintMode.FULL):

        def mode_select(mode: SoPPrintMode, payload: str):
            if mode == SoPPrintMode.SKIP:
                return colored(f'skip... (print_packet mode={mode})', 'yellow'), payload
            elif mode == SoPPrintMode.ABBR:
                payload_raw = payload
                if payload.count('\n') > 10:
                    payload = '\n'.join(payload.split('\n')[:10]) + '\n' + \
                        colored(
                            f'skip... (print_packet mode={mode})', 'yellow')
                    return payload, payload_raw
                elif len(payload) > 1000:
                    payload = payload[:1000] + '\n' + \
                        colored(
                            f'skip... (print_packet mode={mode})', 'yellow')
                    return payload, payload_raw
                else:
                    return payload, payload_raw
            elif mode == SoPPrintMode.FULL:
                return payload, payload
            else:
                SOPLOG_DEBUG(
                    f'[print_packet] Unknown mode!!! mode should be [skip|abbr|full] mode : {mode}', 'red')

        def print_result_topic(topic, payload):
            topic_str = topic_join(topic)
            topic_indicator = f'{topic[0]}_{topic[1]}_{topic[2]}'

            payload, payload_raw = mode_select(mode, payload)
            payload = colored(payload, attrs=['bold'])

            SOPLOG_DEBUG(
                f'[{topic_indicator:20}] topic : {topic_str} payload : {payload}')

        def print_topic(topic, payload):
            topic_str = topic_join(topic)
            topic_indicator = f'{topic[0]}_{topic[1]}'

            payload, payload_raw = mode_select(mode, payload)
            payload = colored(payload, attrs=['bold'])

            SOPLOG_DEBUG(
                f'[{topic_indicator:20}] topic : {topic_str} payload : {payload}')

        topic, payload, timestamp = decode_MQTT_message(msg, str)
        topic = topic_split(topic)

        payload = dict_to_json_string(payload)

        if topic[0] == 'MT':
            if topic[1] == 'RESULT':
                if topic[2] in ['REGISTER', 'UNREGISTER', 'BINARY_VALUE']:
                    print_result_topic(topic, payload)
                else:
                    SOPLOG_DEBUG(
                        f'[print_packet] Unknown {topic[0]}_{topic[1]} Topic!!!', 'red')
            else:
                if topic[1] in ['EXECUTE']:
                    print_topic(topic, payload)
                else:
                    SOPLOG_DEBUG(
                        f'[print_packet] Unknown {topic[0]} Topic!!!', 'red')
        elif topic[0] == 'TM':
            if topic[1] == 'RESULT':
                if topic[2] in ['EXECUTE']:
                    print_result_topic(topic, payload)
                else:
                    SOPLOG_DEBUG(
                        f'[print_packet] Unknown {topic[0]}_{topic[1]} Topic!!!', 'red')
            else:
                if topic[1] in ['REGISTER', 'UNREGISTER', 'ALIVE', 'VALUE_PUBLISH']:
                    print_topic(topic, payload)
                else:
                    SOPLOG_DEBUG(
                        f'[print_packet] Unknown {topic[0]} Topic!!!', 'red')
        elif topic[0] == 'MS':
            if topic[1] == 'RESULT':
                if topic[2] in ['SCHEDULE', 'EXECUTE', 'SERVICE_LIST']:
                    print_result_topic(topic, payload)
                else:
                    SOPLOG_DEBUG(
                        f'[print_packet] Unknown {topic[0]}_{topic[1]} Topic!!!', 'red')
            else:
                if topic[1] in ['SCHEDULE', 'EXECUTE']:
                    print_topic(topic, payload)
                else:
                    SOPLOG_DEBUG(
                        f'[print_packet] Unknown {topic[0]} Topic!!!', 'red')
        elif topic[0] == 'SM':
            if topic[1] == 'RESULT':
                if topic[2] in ['SCHEDULE', 'EXECUTE']:
                    print_result_topic(topic, payload)
                else:
                    SOPLOG_DEBUG(
                        f'[print_packet] Unknown {topic[0]}_{topic[1]} Topic!!!', 'red')
            else:
                if topic[1] in ['SCHEDULE', 'EXECUTE', 'AVAILABILITY', 'REFRESH']:
                    print_topic(topic, payload)
                else:
                    SOPLOG_DEBUG(
                        f'[print_packet] Unknown {topic[0]} Topic!!!', 'red')
        elif topic[0] == 'ME':
            if topic[1] == 'NOTIFY_CHANGE':
                print_topic(topic, payload)
            else:
                SOPLOG_DEBUG(
                    f'[print_packet] Unknown {topic[0]} Topic!!!', 'red')
        elif topic[0] == self._name:
            if topic[1] in [value.get_name() for value in self._value_list]:
                print_topic(topic, payload)
            else:
                SOPLOG_DEBUG(
                    f'[print_packet] Unknown VALUE PUBLISH Topic!!!, topic : {topic}', 'red')
        else:
            topic = topic_join(topic)
            SOPLOG_DEBUG(
                f'[print_packet] Unexpected topic!!! : {topic} ', 'red')

    # MQTT utils
    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    def _connect(self):
        self._mqtt_client.on_connect = self._on_connect
        self._mqtt_client.on_disconnect = self._on_disconnect
        self._mqtt_client.on_publish = self._on_publish
        self._mqtt_client.on_subscribe = self._on_subscribe
        self._mqtt_client.on_unsubscribe = self._on_unsubscribe
        self._mqtt_client.on_message = self._on_message

        self._mqtt_client.connect(self._ip, self._port)
        self._mqtt_client.loop_start()

    def _disconnect(self):
        self._mqtt_client.loop_stop()
        ret = self._mqtt_client.disconnect()

        SOPLOG_DEBUG(
            f'{PrintTag.DISCONNECT} disconnect from Host: {self._ip}:{self._port}', 'red')

    def _subscribe(self, topic: str, qos: int = 2, thing: SoPThing = None):
        if topic not in self._subscribed_topic_set:
            ret = self._mqtt_client.subscribe(topic, qos=qos)
            if not ret[0] == 0:
                SOPLOG_DEBUG(
                    f'{PrintTag.SUBSCRIBE} subscribe failed!!!', 'red')
                return False
            if not thing:
                self.get_subscribed_topic_set().add(topic)
            else:
                thing.get_subscribed_topic_set().add(topic)

        SOPLOG_DEBUG(f'{PrintTag.SUBSCRIBE} {topic}')
        return True

    def _unsubscribe(self, topic: str, thing: SoPThing = None):
        if topic in self._subscribed_topic_set:
            ret = self._mqtt_client.unsubscribe(topic)
            if not ret[0] == 0:
                SOPLOG_DEBUG(
                    f'{PrintTag.UNSUBSCRIBE} unsubscribe failed!!!', 'red')
                return False
            if not thing:
                self.get_subscribed_topic_set().add(topic)
            else:
                thing.get_subscribed_topic_set().add(topic)

        SOPLOG_DEBUG(f'{PrintTag.UNSUBSCRIBE} {topic}')
        return True

    def _publish(self, topic: str, payload, qos: int = 2):
        cnt = 3
        send_time = 0
        while cnt:
            ret = self._mqtt_client.publish(topic, payload, qos=qos)
            if ret.rc != 0:
                SOPLOG_DEBUG('Publish failed!!!', 'red')
                SOPLOG_DEBUG(f'Topic : {topic}', 'red')
                SOPLOG_DEBUG(f'Payload : {payload}', 'red')
                SOPLOG_DEBUG(f'Retry {4-cnt}', 'red')
                cnt -= 1
                time.sleep(0.2)
            else:
                send_time = time.time()
                break
        else:
            SOPLOG_DEBUG(
                'Publish mqtt is not work... exit program', 'red')
            self._publish_queue.queue.clear()
            # self.wrapup()

        msg = encode_MQTT_message(topic, payload, send_time)
        self._print_packet(msg, mode=self._log_mode)

    # Avahi feature (WARNING: not work on python3.6<)
    def _avahi_discover(self, MQTT_SOPIOT_AVAHI_LIST=["_mqtt_sopiot._tcp.local.", "_mqtt_ssl_sopiot._tcp.local."]):

        def on_service_state_change(zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange) -> None:
            # SOPLOG_DEBUG(
            #     f"Service {name} of type {service_type} state changed: {state_change}")

            if state_change is ServiceStateChange.Added:
                info = zeroconf.get_service_info(
                    service_type, name)
                # SOPLOG_DEBUG("Info from zeroconf.get_service_info: %r" % (info))

                if info:
                    addresses = ["%s:%d" % (addr, cast(int, info.port))
                                 for addr in info.parsed_scoped_addresses()]
                    ipv4_address = addresses[0]
                    ipv6_address = addresses[1]
                    ip = ipv4_address.split(':')[0]
                    port = int(ipv4_address.split(':')[1])

                    discovered_middleware = {
                        'ip': ip,
                        'port': port,
                        'name': info.server,
                    }

                    SOPLOG_DEBUG(f"Server name: {info.server}")
                    SOPLOG_DEBUG(f"Address: {ip}")
                    SOPLOG_DEBUG(
                        f"Weight: {info.weight}, priority: {info.priority}")
                    if info.properties:
                        for key, value in info.properties.items():
                            SOPLOG_DEBUG(
                                f"Properties -> {key.decode('utf-8')}: {value.decode('utf-8')}")
                    else:
                        SOPLOG_DEBUG("No properties", 'yellow')

                    self._avahi_discovered_middleware_list.append(
                        discovered_middleware)
                    self._avahi_middleware_name = info.server
                else:
                    SOPLOG_DEBUG("No info")

        zeroconf = Zeroconf(ip_version=IPVersion.V4Only)
        services = MQTT_SOPIOT_AVAHI_LIST
        # services = list(ZeroconfServiceTypes.find(zc=zeroconf))
        browser = ServiceBrowser(zeroconf, services, handlers=[
                                 on_service_state_change])
        time.sleep(3)
        browser.cancel()
        zeroconf.close()

    def _set_ssl_config(self):
        SOPLOG_DEBUG('SSL enabled...')
        try:
            self._mqtt_client.tls_set(
                ca_certs=f'{self._ssl_ca_path}/ca.crt',
                certfile=f'{self._ssl_ca_path}/client.crt',
                keyfile=f'{self._ssl_ca_path}/client.key',
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLSv1_2,
                ciphers=None)
            self._mqtt_client.tls_insecure_set(True)
        except ValueError as e:
            SOPLOG_DEBUG('SSL/TLS has already been configured.', 'yellow')

    def _avahi_init(self, avahi_enable):

        def save_middleware_info():
            middleware_info = {
                "middleware_list": [
                    {
                        "name": self._avahi_middleware_name,
                        "ip": self._ip,
                        "port": self._port,
                        "lastest_connect_time": time.time()
                    }
                ]
            }
            json_file_write('middleware_info.json',
                            middleware_info)

        def set_connect_info(selected_middleware: dict):
            self._ip = selected_middleware['ip']
            self._port = selected_middleware['port']

        if avahi_enable:
            if sys.version_info[0] <= 3 and sys.version_info[1] < 6:
                raise Exception(
                    'Avahi feature is not supported on python3.6<. try python3.7 or higher. or disable avahi feature. (avahi_enable=False)')

            self._avahi_discover(MQTT_SOPIOT_AVAHI_LIST=[
                "_mqtt_sopiot._tcp.local.",
                "_mqtt_ssl_sopiot._tcp.local."])
            if len(self._avahi_discovered_middleware_list) > 1:
                SOPLOG_DEBUG('More than 2 avahi_enable host searched...')
                middleware_info = json_file_read('middleware_info.json')

                if middleware_info:
                    middleware_list = sorted(
                        middleware_info['middleware_list'], key=lambda x: x['lastest_connect_time'])
                    set_connect_info(middleware_list[0])
                    SOPLOG_DEBUG(
                        'Connect to lastest connected middleware...')
                else:
                    SOPLOG_DEBUG('middleware_info.json is empty...:')
                    for i, discovered_middleware in enumerate(self._avahi_discovered_middleware_list):
                        ip = discovered_middleware['ip']
                        port = discovered_middleware['port']
                        middleware_name = discovered_middleware['name']
                        SOPLOG_DEBUG(
                            f'{i}: {ip}:{port} ({middleware_name})')
                    while True:
                        user_input = int(input('select middleware : '))
                        if user_input not in range(len(self._avahi_discovered_middleware_list)):
                            SOPLOG_DEBUG(
                                'Invalid input...', 'red')
                        else:
                            break
                    set_connect_info(
                        self._avahi_discovered_middleware_list[user_input])
                    save_middleware_info()

                if self._ssl_enable == True:
                    self._set_ssl_config()
                elif self._port == 8883:
                    self._set_ssl_config()
                else:
                    SOPLOG_DEBUG('SSL is not enabled...')

            elif len(self._avahi_discovered_middleware_list) == 1:
                set_connect_info(self._avahi_discovered_middleware_list[0])
                save_middleware_info()
            else:
                SOPLOG_DEBUG(
                    'avahi_enable search failed... connect to default ip...')
        else:
            SOPLOG_DEBUG('Skip avahi_enable search...')

# ===================================================================================
# ___  ___ _____  _____  _____   _____         _  _  _                   _
# |  \/  ||  _  ||_   _||_   _| /  __ \       | || || |                 | |
# | .  . || | | |  | |    | |   | /  \/  __ _ | || || |__    __ _   ___ | | __ ___
# | |\/| || | | |  | |    | |   | |     / _` || || || '_ \  / _` | / __|| |/ // __|
# | |  | |\ \/' /  | |    | |   | \__/\| (_| || || || |_) || (_| || (__ |   < \__ \
# \_|  |_/ \_/\_\  \_/    \_/    \____/ \__,_||_||_||_.__/  \__,_| \___||_|\_\|___/
# ===================================================================================

    # for MQTT version<5.0
    def _on_connect(self, client: SoPClient, userdata, flags, result):
        if result == 0:
            self._connected = True
            SOPLOG_DEBUG(
                f'{PrintTag.CONNECT} Connect to Host: {self._ip}:{self._port}')
            # TODO: implement auto reregister feature
            if self._registered:
                pass
        else:
            SOPLOG_DEBUG(
                f'{PrintTag.ERROR} Bad connection... Returned code: {result}', 'red')

    def _on_disconnect(self, client: SoPClient, userdata, rc):
        if rc == 0:
            self._connected = False
            SOPLOG_DEBUG(
                f'{PrintTag.DISCONNECT} Disconnect from Host: {self._ip}:{self._port}')
        else:
            SOPLOG_DEBUG(
                f'{PrintTag.ERROR} Bad disconnection... Returned code: {rc}', 'red')

    def _on_subscribe(self, client: SoPClient, userdata: str, mid, granted_qos):
        pass

    def _on_unsubscribe(self, client: SoPClient, userdata: str, mid):
        pass

    def _on_publish(self, client: SoPClient, userdata: mqtt.MQTTMessage, mid):
        pass

    def _on_message(self, client: SoPClient, userdata: Callable, msg: mqtt.MQTTMessage):
        self._print_packet(msg, mode=self._log_mode)
        self._receive_queue.put(msg)

    # TODO: test this functions
    # for MQTT version>=5.0
    def _on_connect_v5(self, client: SoPClient, userdata, flags, reason, properties):
        if reason == 0:
            self._connected = True
            SOPLOG_DEBUG(
                f'{PrintTag.CONNECT} Connect to Host: {self._ip}:{self._port}')
            # TODO: implement auto reregister feature
            if self._registered:
                pass
        else:
            SOPLOG_DEBUG(
                f'{PrintTag.ERROR} Bad connection... Returned code: {reason}', 'red')

    def _on_disconnect_v5(self, client: SoPClient, userdata, rc, properties):
        if rc == 0:
            self._connected = False
            SOPLOG_DEBUG(
                f'{PrintTag.DISCONNECT} Disconnect from Host: {self._ip}:{self._port}')
        else:
            SOPLOG_DEBUG(
                f'{PrintTag.ERROR} Bad disconnection... Returned code: {rc}', 'red')

    def _on_subscribe_v5(self, client: SoPClient, userdata: str, mid, reasoncodes, properties):
        pass

    def _on_unsubscribe_v5(self, client: SoPClient, userdata: str, mid,  properties, reasoncodes):
        pass

    def _on_publish_v5(self, client: SoPClient, userdata: mqtt.MQTTMessage, mid):
        pass

    def _on_message_v5(self, client: SoPClient, userdata: Callable, msg: mqtt.MQTTMessage):
        self._print_packet(msg, mode=self._log_mode)
        self._receive_queue.put(msg)

    # ====================================
    #               _    _
    #              | |  | |
    #   __ _   ___ | |_ | |_   ___  _ __
    #  / _` | / _ \| __|| __| / _ \| '__|
    # | (_| ||  __/| |_ | |_ |  __/| |
    #  \__, | \___| \__| \__| \___||_|
    #   __/ |
    #  |___/
    # ====================================

    # ==================================
    #             _    _
    #            | |  | |
    #  ___   ___ | |_ | |_   ___  _ __
    # / __| / _ \| __|| __| / _ \| '__|
    # \__ \|  __/| |_ | |_ |  __/| |
    # |___/ \___| \__| \__| \___||_|
    # ==================================
