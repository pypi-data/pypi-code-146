from big_thing_py.big_thing import *
from big_thing_py.super import *


class SoPSuperThing(SoPBigThing):
    DUMMY_RESULT_LIST = [dict(error=SoPErrorType.UNDEFINED,
                              scenario=None,
                              return_type=SoPType.UNDEFINED,
                              return_value=None)]

    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True,
                 ip: str = None, port: int = None, ssl_ca_path: str = None, ssl_enable: bool = False, log_name: str = None, log_enable: bool = True, log_mode: SoPPrintMode = SoPPrintMode.ABBR, append_mac_address: bool = True,
                 refresh_cycle: float = 10):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, ip, port,
                         ssl_ca_path, ssl_enable, log_name, log_enable, log_mode, append_mac_address)

        self._hierarchical_service_table: Dict[str, List[SoPService]] = dict(
            value=[], function=[])

        self._last_refresh_time = 0
        self._last_available_time = 0

        self._refresh_cycle = refresh_cycle
        self._available_cycle = refresh_cycle / 2

        self._function_list: List[SoPSuperFunction] = self._function_list

        # Queue
        self._super_execute_queue: Queue = Queue()
        self._schedule_queue: Queue = Queue()
        self._subscribe_queue: Queue = Queue()
        self._unsubscribe_queue: Queue = Queue()

        self._thread_func_list += [
            self._refresh_thread_func,
            self._available_thread_func,
            self._subscribe_thread_func,
            self._unsubscribe_thread_func]

        self._extract_subfunction_reqline_info()

        for super_function in self._function_list:
            super_function.set_subscribe_queue(self._subscribe_queue)
            super_function.set_unsubscribe_queue(self._unsubscribe_queue)

    # ===========================================================================================
    #  _    _                             _    __                      _    _
    # | |  | |                           | |  / _|                    | |  (_)
    # | |_ | |__   _ __   ___   __ _   __| | | |_  _   _  _ __    ___ | |_  _   ___   _ __   ___
    # | __|| '_ \ | '__| / _ \ / _` | / _` | |  _|| | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|
    # | |_ | | | || |   |  __/| (_| || (_| | | |  | |_| || | | || (__ | |_ | || (_) || | | |\__ \
    #  \__||_| |_||_|    \___| \__,_| \__,_| |_|   \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/
    # ===========================================================================================

    def _refresh_thread_func(self, stop_event: Event):
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                if self._registered:
                    if (get_current_time() - self._last_refresh_time) > self._refresh_cycle:
                        self._send_SM_REFRESH()
                        self._last_refresh_time = get_current_time()
                        # time.sleep(self._refresh_cycle / 2)

        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    def _available_thread_func(self, stop_event: Event):
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                if self._registered:
                    if (get_current_time() - self._last_available_time) > self._available_cycle:
                        self._send_SM_AVAILABILITY()
                        self._last_available_time = get_current_time()
                        # time.sleep(self._available_cycle / 2)

        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    def _subscribe_thread_func(self, stop_event: Event):
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                if self._registered:
                    if not self._subscribe_queue.empty():
                        topic = self._subscribe_queue.queue[0]
                        self._subscribe(topic)
                        self._subscribe_queue.get()

        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    def _unsubscribe_thread_func(self, stop_event: Event):
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                if self._registered:
                    if not self._unsubscribe_queue.empty():
                        topic = self._unsubscribe_queue.queue[0]
                        self._unsubscribe(topic)
                        topic = self._unsubscribe_queue.get()

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

        if super()._handle_mqtt_message(msg):
            return True
        else:
            if topic[0] == 'MS':
                if topic[1] == 'RESULT':
                    if topic[2] == 'SCHEDULE':
                        self._handle_MS_RESULT_SCHEDULE(msg)
                    elif topic[2] == 'EXECUTE':
                        self._handle_MS_RESULT_EXECUTE(msg)
                    elif topic[2] == 'SERVICE_LIST':
                        self._handle_MS_RESULT_SERVICE_LIST(msg)
                    else:
                        SOPLOG_DEBUG(
                            '[handle_mqtt_message] Unexpected MS_RESULT topic!')
                elif topic[1] == 'SCHEDULE':
                    self._handle_MS_SCHEDULE(msg)
                elif topic[1] == 'EXECUTE':
                    self._handle_MS_EXECUTE(msg)
                else:
                    SOPLOG_DEBUG('[handle_mqtt_message] Unexpected MS topic!')

                return True
            elif topic[0] == 'ME':
                if topic[1] == 'NOTIFY_CHANGE':
                    self._handle_ME_NOTIFY(msg)
                else:
                    SOPLOG_DEBUG('[handle_mqtt_message] Unexpected ME topic!')

                return True
            else:
                SOPLOG_DEBUG('[handle_mqtt_message] Unexpected topic!')
                return False

    # ================
    # ___  ___ _____
    # |  \/  |/  ___|
    # | .  . |\ `--.
    # | |\/| | `--. \
    # | |  | |/\__/ /
    # \_|  |_/\____/
    # ================

    def _handle_MS_SUPER_ACTION(self, super_action_msg: Union[SoPSuperScheduleMessage, SoPSuperExecuteMessage]):
        target_super_function = self._find_function(
            super_action_msg._super_function_name)
        super_request_key = make_super_request_key(
            super_action_msg._requester_middleware_name, super_action_msg._scenario)
        if isinstance(super_action_msg, SoPSuperScheduleMessage):
            if super_request_key in target_super_function._temporary_scheduling_table:
                SOPLOG_DEBUG(
                    f'[handle_MS_SUPER_ACTION] Super request key {super_request_key} is already exist in temporary_scheduling_table!', 'red')
                return False

            super_schedule_request = SoPSuperScheduleRequest(
                trigger_msg=super_action_msg,)
            target_super_function._temporary_scheduling_table[
                super_request_key] = super_schedule_request
            super_action_request = super_schedule_request
        elif isinstance(super_action_msg, SoPSuperExecuteMessage):
            if super_request_key in target_super_function._temporary_scheduling_table:
                SOPLOG_DEBUG(
                    f'[handle_MS_SUPER_ACTION] Super request key {super_request_key} is already exist in mapping_table!', 'red')
                return False

            super_execute_request = target_super_function._mapping_table[super_request_key]
            super_execute_request._super_arg_list = target_super_function.get_arg_list()
            super_execute_request._trigger_msg = super_action_msg
            super_action_request = super_execute_request

        # super action 스레드 생성
        if target_super_function:
            super_action_request.timer_start()
            target_super_function.super_action(
                super_action_request, self._hierarchical_service_table)
            return True
        # 만약 타켓 함수가 없다면 에러를 출력한다.
        else:
            SOPLOG_DEBUG(
                f'Function {super_action_request._trigger_msg._super_function_name} is not exist', 'red')
            return False

    def _handle_MS_SUPER_RESULT_ACTION(self, subrequest_key: str, super_action_result_msg: Union[SoPSubScheduleResultMessage, SoPSubExecuteResultMessage]):
        target_super_function = self._find_function(
            super_action_result_msg._super_function_name)

        super_request_key = make_super_request_key(
            super_action_result_msg._requester_middleware_name, super_action_result_msg._scenario)
        target_super_function.put_subaction_result(
            super_request_key, subrequest_key, super_action_result_msg)

    def _handle_MS_SCHEDULE(self, msg: mqtt.MQTTMessage):
        super_schedule_msg = SoPSuperScheduleMessage(msg)
        super_schedule_msg.set_timestamp()
        self._handle_MS_SUPER_ACTION(super_schedule_msg)

    def _handle_MS_RESULT_SCHEDULE(self, msg: mqtt.MQTTMessage):
        subschedule_result_msg = SoPSubScheduleResultMessage(msg)
        subschedule_result_msg.set_timestamp()
        subrequest_key = make_sub_request_key(
            subschedule_result_msg._subfunction_name, subschedule_result_msg._subrequest_order)
        self._handle_MS_SUPER_RESULT_ACTION(
            subrequest_key, (subschedule_result_msg))

    def _handle_MS_EXECUTE(self, msg: mqtt.MQTTMessage):
        super_execute_msg = SoPSuperExecuteMessage(msg)
        super_execute_msg.set_timestamp()
        self._handle_MS_SUPER_ACTION(super_execute_msg)

    def _handle_MS_RESULT_EXECUTE(self, msg: mqtt.MQTTMessage):
        subexecute_result_msg = SoPSubExecuteResultMessage(msg)
        subexecute_result_msg.set_timestamp()
        subrequest_key = make_sub_request_key(
            subexecute_result_msg._subfunction_name, subexecute_result_msg._subrequest_order)
        self._handle_MS_SUPER_RESULT_ACTION(
            subrequest_key, subexecute_result_msg)

    def _handle_MS_RESULT_SERVICE_LIST(self, msg: mqtt.MQTTMessage):
        service_list = SoPServiceListResultMessage(msg)
        service_list.set_timestamp()

        try:
            for middleware in service_list.service_list():
                middleware_name = middleware['middleware']
                hierarchy_type = middleware['hierarchy']
                thing_list = middleware['things']
                for thing in thing_list:
                    is_alive = thing['is_alive']
                    if is_alive != 1:
                        continue
                    is_super = thing['is_super']
                    # alive_cycle = thing['alive_cycle']
                    thing_name = thing['id']
                    value_list = thing['values']
                    function_list = thing['functions']

                    # value 정보를 추출
                    for value_info in value_list:
                        value_tag_list = [SoPTag(tag['name'])
                                          for tag in value_info['tags']]

                        # TODO: energy, cycle info is omit in service list
                        value_service = SoPValue(name=value_info['name'],
                                                 thing_name=thing_name,
                                                 middleware_name=middleware_name,
                                                 tag_list=value_tag_list,
                                                 desc=value_info['description'],
                                                 func=None,
                                                 energy=None,
                                                 type=SoPType.get(
                            value_info['type']),
                            bound=(float(value_info['bound']['min_value']),
                                   float(value_info['bound']['max_value'])),
                            format=value_info['format'],
                            cycle=None)
                        if value_service not in self._hierarchical_service_table['value']:
                            self._hierarchical_service_table['value'].append(
                                value_service)

                    # function 정보를 추출
                    for function_info in function_list:
                        function_tag_list = [SoPTag(tag['name'])
                                             for tag in function_info['tags']]
                        arg_list = []
                        if bool(function_info['use_arg']):
                            for argument in function_info['arguments']:
                                arg_list.append(SoPArgument(name=argument['name'],
                                                            type=SoPType.get(
                                                                argument['type']),
                                                            bound=(float(argument['bound']['min_value']),
                                                                   float(argument['bound']['max_value']))))
                        function_service = SoPFunction(name=function_info['name'],
                                                       thing_name=thing_name,
                                                       middleware_name=middleware_name,
                                                       tag_list=function_tag_list,
                                                       desc=function_info['description'],
                                                       func=None,
                                                       energy=None,
                                                       arg_list=arg_list,
                                                       return_type=SoPType.get(
                                                           function_info['return_type']),
                                                       exec_time=function_info['exec_time'],
                                                       timeout=None)
                        if function_service not in self._hierarchical_service_table['function']:
                            self._hierarchical_service_table['function'].append(
                                function_service)

            self._last_refresh_time = get_current_time()
        except KeyError as e:
            print_error(e)
            SOPLOG_DEBUG('[handle_MS_RESULT_SERVICE_LIST] KeyError', 'red')
        except ValueError as e:
            print_error(e)
            SOPLOG_DEBUG('[handle_MS_RESULT_SERVICE_LIST] ValueError', 'red')
        except Exception as e:
            print_error(e)
            SOPLOG_DEBUG(
                '[handle_MS_RESULT_SERVICE_LIST] Unknown Exception', 'red')

    # ===================
    #   __  __   ______
    #  |  \/  | |  ____|
    #  | \  / | | |__
    #  | |\/| | |  __|
    #  | |  | | | |____
    #  |_|  |_| |______|
    # ===================

    def _handle_ME_NOTIFY(self, msg: mqtt.MQTTMessage):
        notify_msg = SoPNotifyMessage(msg)
        notify_msg.set_timestamp()
        self._send_SM_REFRESH()

    # ================
    #  _____ ___  ___
    # /  ___||  \/  |
    # \ `--. | .  . |
    #  `--. \| |\/| |
    # /\__/ /| |  | |
    # \____/ \_|  |_/
    # ================

    def _send_SM_SCHEDULE(self, subfunction_name: str, thing_name: str, middleware_name: str, super_thing_name: str,
                          scenario_name: str, period: float):
        self._publish_queue.put(SoPSubScheduleMessage(subfunction_name, thing_name,
                                middleware_name, super_thing_name, scenario_name, period).mqtt_message())

    # TODO: complete this function
    def _send_SM_EXECUTE(self, subfunction_name: str, target_thing_name: str, target_middleware_name: str, super_thing_name: str,
                         scenario_name: str, arguments: Tuple):
        self._publish_queue.put(SoPSubExecuteMessage(subfunction_name, target_thing_name,
                                target_middleware_name, super_thing_name, scenario_name, arguments).mqtt_message())

    def _send_SM_RESULT_SCHEDULE(self, super_function_name: str, super_thing_name: str, super_middleware_name: str, requester_middleware_name: str,
                                 scenario_name: str, error: SoPErrorType):
        self._publish_queue.put(SoPSuperScheduleResultMessage(super_function_name, super_thing_name, super_middleware_name, requester_middleware_name,
                                                              scenario_name, error).mqtt_message())

    def _send_SM_RESULT_EXECUTE(self, super_function_name: str, super_thing_name: str, super_middleware_name: str, requester_middleware_name: str,
                                scenario: str, return_type: SoPType, return_value: Union[int, float, bool, str], error: SoPErrorType):
        self._publish_queue.put(SoPSuperExecuteResultMessage(super_function_name, super_thing_name, super_middleware_name, requester_middleware_name,
                                                             scenario, return_type, return_value, error).mqtt_message())

    def _send_SM_AVAILABILITY(self):
        self._publish_queue.put(SoPAvailablityMessage(
            self._name, self._dump_availablity()).mqtt_message())

    def _send_SM_REFRESH(self):
        self._publish_queue.put(SoPRefreshMessage(self._name).mqtt_message())

    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    # def schedule(self, schedule_request: SoPScheduleRequest):
    #     self._thread = SoPThread(
    #         func=self.schedule_thread_func,
    #         daemon=True,
    #         arg_list=(schedule_request, ))
    #     self._thread.start()

    # def find_super_function_service(self, super_function_service_name):
    #     for function in self._function_list:
    #         if function.get_name() == super_function_service_name:
    #             return function

    # def _catch_subexecute_result_parallel(self, super_request_key: str, target_super_function: SoPSuperFunction, timeout: float = 10):
    #     result_list: List[dict] = []
    #     reqline_execution_result_list: List[List[SoPSubExecuteResultMessage]] = [
    #     ]
    #     super_execute_request = target_super_function._mapping_table[super_request_key]
    #     subrequest_key = make_sub_request_key(
    #         subfunction_name, super_execute_request._current_reqline_num)
    #     # TODO: 여기서 다 돌지마라.. 3개 다 뺴버리니까
    #     for subrequest_key, subfunction_reqline in super_execute_request._subfunction_reqline_table.items():
    #         reqline_execution_result_list.append(super_execute_request.get_subexecute_result_msg_list(
    #             subrequest_key, timeout))
    #         SOPLOG_DEBUG(f'get_subresult_msg: {reqline_execution_result_list}')

    #     for sub_execution_result_list in reqline_execution_result_list:
    #         for sub_execution_result in sub_execution_result_list:
    #             result_list.append(dict(scenario=sub_execution_result._scenario,
    #                                     return_type=sub_execution_result._return_type,
    #                                     return_value=sub_execution_result._return_value,
    #                                     error=sub_execution_result._error))
    #     return result_list

    def _find_function(self, function_name: str) -> SoPSuperFunction:
        for function in self._function_list:
            if function.get_name() == function_name:
                return function

    def _request_subexecute_nonparallel(self, subexecute_request_list, mapping_table: Dict[str, List[SoPFunction]], subfunction_name: str, arg_list: Tuple, result_list: List[dict]):
        for target_scenario, target_subfunction_list in mapping_table.items():
            for target_subfunction in target_subfunction_list:
                if subfunction_name == target_subfunction.get_name():
                    self._subscribe(SoPProtocolType.Super.MS_RESULT_EXECUTE.value % (target_subfunction.get_name(),
                                                                                     target_subfunction.get_thing_name(),
                                                                                     target_subfunction.get_middleware_name(),
                                                                                     self._name))
                    json_arg_list = [dict(order=i, value=arg)
                                     for i, arg in enumerate(arg_list)]
                    self._send_SM_EXECUTE(target_subfunction.get_name(),
                                          target_subfunction.get_thing_name(),
                                          target_subfunction.get_middleware_name(),
                                          self._name,
                                          target_scenario,
                                          json_arg_list)
                    # 하나의 subfunction의 subexecute 결과를 받을 때까지 기다린다. 이후 다음 subfunction에게 subexecute 요청을 보내고 받는 것을 반복.
                    self._catch_subexecute_result_nonparallel(
                        subexecute_request_list, target_subfunction, result_list)

    def _catch_subexecute_result_nonparallel(self, subexecute_request_list: List[dict], target_subfunction: SoPFunction, result_list: List[dict]):
        for subexecute_request in subexecute_request_list:
            subexecute_msg: SoPSubExecuteMessage = subexecute_request['subexecute_msg']
            subexecute_request['end_time'] = time.time()
            subfunction_check = subexecute_msg._subfunction_name == target_subfunction.get_name()
            target_thing_check = subexecute_msg._target_thing_name == target_subfunction.get_thing_name()
            target_middleware_check = subexecute_msg._target_middleware_name == target_subfunction.get_middleware_name()
            super_thing_check = subexecute_msg._super_thing_name == self._name
            # self._subexecute_request_list에 있는 request중에 target_subfunction에 해당하는 요청에 대한 결과를 찾는다.
            if subfunction_check and target_thing_check and target_middleware_check and super_thing_check:
                result_queue: Queue = subexecute_request['result_queue']
                subexecute_result_msg: SoPSubExecuteResultMessage = result_queue.get()
                SOPLOG_DEBUG(
                    f'[SUBEXECUTE END] {subexecute_result_msg._subfunction_name}|{subexecute_result_msg._target_thing_name} duration: {(subexecute_request["end_time"] - subexecute_request["start_time"]):.4f}', 'cyan')

                self._unsubscribe_queue.put(
                    subexecute_result_msg.topic())
                while not self._unsubscribe_queue.empty():
                    time.sleep(THREAD_TIME_OUT)

                result_list.append(dict(
                    scenario=subexecute_result_msg._scenario,
                    return_type=subexecute_result_msg._return_type,
                    return_value=subexecute_result_msg._return_value,
                    error=subexecute_result_msg._error))

    # def request_function_service(self, super_request_key: str, target_super_function: SoPSuperFunction, subfunction_name: str, timeout=10) -> Union[List[dict], bool]:
    #     result_list = []

    #     # 병렬 요청 옵션. _super_execute_wrapper안에서 병렬로 보냈던 subexecute 요청에 대한 결과를 수집한다.
    #     if target_super_function._request_parallel:
    #         result_list = self._catch_subexecute_result_parallel(
    #             super_request_key, target_super_function, timeout=timeout)

    #         if len(result_list) == 0:
    #             raise Exception('Result_list is empty')
    #         else:
    #             return result_list
    #     # 직렬 요청 옵션. 하나씩 subexecute요청을 보내고 그에 대한 결과를 받는다.
    #     else:
    #         # TODO: implement
    #         # mapping_table에 저장된 subfunction중 현재 request_function_service이 요청하고자하는 subfunction을 찾는다.
    #         pass

    #     return result_list

    # execute service via super service
    def req(self, super_request_key: str, subfunction_name: str = '', arg_list: Union[Tuple[SoPArgument], Tuple] = None, tag_list: List[str] = [],
            service_type: SoPServiceType = SoPServiceType.FUNCTION, policy: SoPPolicy = SoPPolicy.SINGLE,
            timeout=1000) -> Union[List[dict], bool]:
        super_function_name = inspect.currentframe().f_back.f_code.co_name
        target_super_function = self._find_function(super_function_name)
        # str 타입의 태그를 SoPTag로 변환
        tag_list = [SoPTag(str_tag) for str_tag in tag_list]

        try:
            if service_type == SoPServiceType.VALUE:
                subfunction_name = f'__{subfunction_name}'
            elif service_type == SoPServiceType.FUNCTION:
                pass
            else:
                SOPLOG_DEBUG(f'Invalid service type: {service_type}', 'red')
                raise Exception

            # super thing을 init할 때 자신이 가지고 있는 super function에 대한 정보를 추출한다.
            if target_super_function.get_first_execute():
                target_super_function.add_subfunction_reqline_info(
                    subfunction_name, arg_list, tag_list, policy)
            else:
                super_execute_request = target_super_function._mapping_table[super_request_key]
                subrequest_key = make_sub_request_key(
                    subfunction_name, super_execute_request._current_reqline_num)
                result_msg_list = super_execute_request.get_subexecute_result_msg_list(
                    subrequest_key=subrequest_key, timeout=timeout)
                super_execute_request._current_reqline_num += 1
                result_list = [dict(scenario=result_msg._scenario,
                                    return_type=result_msg._return_type,
                                    return_value=result_msg._return_value,
                                    error=result_msg._error) for result_msg in result_msg_list]
                return result_list
                # return self.request_function_service(super_request_key=super_request_key,
                #                                      target_super_function=target_super_function,
                #                                      subfunction_name=subfunction_name,
                #                                      timeout=timeout)

        except Exception as e:
            print_error(e)
            return False

    # execute scenario line
    def r(self, line: str = None, *arg_list) -> Union[List[dict], bool]:
        super_service_name = inspect.currentframe().f_back.f_code.co_name

        scope_policy = 'all' if 'all' in line else 'single'
        function_name = line.split('.')[1][0:line.split('.')[1].find('(')]
        braket_parse: List[str] = re.findall(r'\(.*?\)', line)
        tags = [tag[1:] for tag in braket_parse[0][1:-1].split(' ')]

        argments = []
        for braket_inner_element in braket_parse[1][1:-1].split(','):
            braket_inner_element = braket_inner_element.strip(' ')
            if braket_inner_element == '':
                continue
            else:
                argments.append(braket_inner_element)

        for i, arg in enumerate(argments):
            if '$' in arg:
                index = int(arg[1:])
                argments[i] = arg_list[index-1]

        argments = tuple(argments)

        # TODO: Update this function
        # result_list = self.request_function_service(tag_list=tags, subfunction_name=function_name, arg_list=argments,
        #                                             super_function_name=super_service_name, policy=scope_policy)
        # return result_list

    # override
    def _subscribe_init_topics(self, thing: SoPThing):
        super()._subscribe_init_topics(thing)

        topic_list = [SoPProtocolType.Super.MS_RESULT_SERVICE_LIST.value % "#"]

        for topic in topic_list:
            self._subscribe(topic)

    # override
    def _subscribe_service_topics(self, thing: SoPThing):
        for function in thing.get_function_list():
            topic_list = [SoPProtocolType.Super.MS_EXECUTE.value % (function.get_name(), thing.get_name(), thing.get_middleware_name(), '#'),
                          SoPProtocolType.Super.MS_SCHEDULE.value % (
                function.get_name(), thing.get_name(), thing.get_middleware_name(), '#')]

            for topic in topic_list:
                self._subscribe(topic)

    def _dump_availablity(self) -> Dict:
        super_function_list = []

        for function in self._function_list:
            subfunction_list = []

            for subfunction_reqline in function.get_subfunction_type_list():
                available_function_service_list = [
                    function_service for function_service in self._hierarchical_service_table['function']]
                subfunction_list.append(dict(name=subfunction_reqline._subfunction_type.get_name(),
                                             status=1 if subfunction_reqline._subfunction_type in available_function_service_list else 0))

            subfunction_status_list = [sub_function['status']
                                       for sub_function in subfunction_list]
            super_function_list.append(dict(name=function.get_name(),
                                            status=0 if 0 in subfunction_status_list else 1,
                                            sub_functions=subfunction_list))
        availablity_info = dict(super_functions=super_function_list)

        return availablity_info

    def generate_random_arg(self, arg_list: List[SoPArgument]):
        random_arg = []
        for arg in arg_list:
            if arg._type == SoPType.INTEGER:
                random_arg.append(random.randint(arg._min, arg._max))
            elif arg._type == SoPType.DOUBLE:
                random_arg.append(random.uniform(arg._min, arg._max))
            elif arg._type in [SoPType.STRING, SoPType.BINARY]:
                import string
                random_arg.append(''.join(random.choices(
                    string.ascii_uppercase + string.digits, k=random.randint(arg._min, arg._max))))
            elif arg._type == SoPType.BOOL:
                random_arg.append(random.choice([True, False]))
            else:
                SOPLOG_DEBUG('Unknown argument type')

        return random_arg

    def _extract_subfunction_reqline_info(self) -> None:
        for function in self._function_list:
            if self._is_super:
                arg_list = function.get_arg_list()
                try:
                    function._func(*tuple([None] + list(arg_list)))
                except Exception as e:
                    pass
                function.set_first_execute(False)

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
