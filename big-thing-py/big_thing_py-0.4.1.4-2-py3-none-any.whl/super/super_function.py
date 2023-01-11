from big_thing_py.super.super_service_utils import *
from big_thing_py.super.super_request import *
import random
import threading


class SoPSuperFunction(SoPFunction):
    '''
        [Whole super function structure]
        super_thing┬── super_function1┬── subfunction1┬────── target_thing1(at Middleware1)
                   │                  │                ╲
                   │                  │                 ╲──── target_thing2(at Middleware1)
                   │                  │                  ╲
                   │                  │                   ╲── target_thing3(at Middleware2)
                   │                  │                    ╲
                   │                  ├── subfunction2      ╲ ....
                   │                  │
                   │                  ├── ...
                   │
                   │
                   └── super_function2 ── subfunction1(target Thing1, target Middleware2)
    '''

    def __init__(self, name: str = None, thing_name: str = None, middleware_name: str = None, tag_list: List[SoPTag] = ..., desc: str = None, func: Callable = None, energy: float = None,
                 arg_list: List[SoPArgument] = ..., return_type: SoPType = ..., exec_time: float = 10, timeout: float = 10, policy: SoPPolicy = ...) -> None:
        super().__init__(name, thing_name, middleware_name, tag_list, desc, func, energy,
                         arg_list, return_type, exec_time, timeout, policy)

        # 사용자가 super thing코드에 명세한 subfunction 조건에 맞는 subfunction 종류. 해당 조건에 맞는 subfunction들이 여러 디바이스에 여러 개 존재할 수 있다.
        # super function에 명세된 req() 라인 수 만큼 존재한다.
        self._subfunction_reqline_list: List[SoPSubFunctionReqline] = []

        # 처음 실행됬는지 여부를 나타낸다. 이는 super function을 처음 실행할 때, req()을 인식하여 _subfunction_type_list를 뽑아내는 동작을 위해 필요하다.
        self._first_execute: bool = True

        # scheduling에 대한 결과를 super thing이 넣어주기 위해 존재함
        # key: {requester_middleware}_{scenario}, value: SoPSuperScheduleActionRequest
        self._temporary_scheduling_table: Dict[str,
                                               SoPSuperScheduleRequest] = {}
        # scheduling이 끝나면 해당 scenario에 대해 어떤 subfunction_type에 대해 thing을 선택할 것인지 정해진다.
        # 이렇게 하는 이유는 scenario를 반복해서 돌릴 때마다 다른 thing을 선택하는 것이 아니라 전에 선택했던 thing에 있는 service를 실행하기 위함이다.
        # key: {requester_middleware}_{scenario}, value: SoPSuperExecuteActionRequest
        self._mapping_table: Dict[str, SoPSuperExecuteRequest] = {}

        # super function의 동작을 하는데 있어 필요한 subscribe, unsubscribe동작을 수행하기 위해 필요
        self._subscribe_queue: Queue = Queue()
        self._unsubscribe_queue: Queue = Queue()

        # super function의 동작을 하는데 소모된 시간을 측정하기 위해 필요
        # self.super_schedule_duration_list = []
        # self.super_execute_duration_list = []

        # for test super service request parallel feature
        self._request_parallel = True
        self._single_request_mode: SoPSingleSubRequestSendType = SoPSingleSubRequestSendType.PARALLEL

    def __eq__(self, o: object) -> bool:
        subfunction_list_check = self.get_subfunction_type_list(
        ) == o.get_subfunction_type_list()
        return super().__eq__(o) and subfunction_list_check

    def _add_subfunction_reqline(self, subfunction_reqline: SoPSubFunctionReqline):
        '''
            super function에 명세된 req() 라인 수 만큼 존재한다. 따라서 중복된 subfunction_type이 존재할 수 없다.
        '''
        subfunction_reqline._subrequest_order = len(
            self._subfunction_reqline_list)
        self._subfunction_reqline_list.append(subfunction_reqline)

    def _remove_subfunction_reqline(self, subfunction_reqline: SoPSubFunctionReqline):
        if subfunction_reqline in self._subfunction_reqline_list:
            self._subfunction_reqline_list.remove(subfunction_reqline)

    def _request_subaction(self, subaction_request: Union[SoPSubScheduleRequest, SoPSubExecuteRequest]) -> None:
        subaction_request.timer_start()
        subaction_msg = subaction_request._trigger_msg

        # 필요한 토픽을 구독한다.
        if isinstance(subaction_request, SoPSubScheduleRequest):
            subschedule_msg: SoPSubScheduleMessage = subaction_request._trigger_msg
            self._subscribe_queue.put(SoPProtocolType.Super.MS_RESULT_SCHEDULE.value % (subschedule_msg._subfunction_name,
                                                                                        subschedule_msg._target_thing_name,
                                                                                        subschedule_msg._target_middleware_name,
                                                                                        subschedule_msg._request_ID))
        elif isinstance(subaction_request, SoPSubExecuteRequest):
            subexecute_msg: SoPSubExecuteMessage = subaction_request._trigger_msg
            self._subscribe_queue.put(SoPProtocolType.Super.MS_RESULT_EXECUTE.value % (subexecute_msg._subfunction_name,
                                                                                       subexecute_msg._target_thing_name,
                                                                                       subexecute_msg._target_middleware_name,
                                                                                       subexecute_msg._request_ID))
        while self._subscribe_queue.empty():
            time.sleep(THREAD_TIME_OUT)

        if isinstance(subaction_request, SoPSubScheduleRequest):
            subschedule_msg: SoPSubScheduleMessage = subaction_request._trigger_msg
            self.send_SM_SCHEDULE(subschedule_msg)
        elif isinstance(subaction_request, SoPSubExecuteRequest):
            subexecute_msg: SoPSubExecuteMessage = subaction_request._trigger_msg
            self.send_SM_EXECUTE(subexecute_msg)
        SOPLOG_DEBUG(
            f'[{subaction_request._action_type.value.upper()} START] {subaction_msg._subfunction_name}|{subaction_msg._target_thing_name}|{subaction_msg._target_middleware_name}', 'cyan')

    def print_request_result(self, request: SoPRequest, color: str, duration: float = None):
        if isinstance(request, SoPSubScheduleRequest):
            SOPLOG_DEBUG(f'[{request._action_type.value.upper()} {request._status.value.upper()} END] {request._trigger_msg._subfunction_name}|{request._trigger_msg._target_thing_name}|{request._trigger_msg._target_middleware_name}, duration: {request.duration():.4f} Sec', color)
        elif isinstance(request, SoPSuperScheduleRequest):
            if request._status == SoPScheduleStatus.CHECK:
                SOPLOG_DEBUG(f'[{request._action_type.value.upper()} {request._status.value.upper()} END] {request._trigger_msg._super_function_name}|{request._trigger_msg._super_thing_name}|{request._trigger_msg._super_middleware_name}, duration: {request.check_duarion():.4f} Sec', color)
            elif request._status == SoPScheduleStatus.CONFIRM:
                SOPLOG_DEBUG(f'[{request._action_type.value.upper()} {request._status.value.upper()} END] {request._trigger_msg._super_function_name}|{request._trigger_msg._super_thing_name}|{request._trigger_msg._super_middleware_name}, duration: {request.confirm_duarion():.4f} Sec', color)
        elif isinstance(request, SoPSubExecuteRequest):
            SOPLOG_DEBUG(f'[{request._action_type.value.upper()} END] {request._trigger_msg._subfunction_name}|{request._trigger_msg._target_thing_name}|{request._trigger_msg._target_middleware_name}, duration: {request.duration():.4f} Sec', color)
        elif isinstance(request, SoPSuperExecuteRequest):
            pass

    def _subschedule_action_parallel(self, super_schedule_request: SoPSuperScheduleRequest, target_schedule_action: SoPScheduleStatus, result_schedule_action: SoPScheduleStatus, timeout: float = 3) -> List[SoPSubScheduleRequest]:
        '''
            subaction 요청을 병렬로 실행하는 함수.
            기존에 하나씩 요청을 보내고 응답을 기다리는 방식에서 모든 요청 패킷을 빠르게 먼저 보내고 응답을 기다리는 방식으로 변경.
        '''

        subschedule_action_start_time = get_current_time()
        # 병렬로 subschedule 요청을 보낸다.
        if self._single_request_mode == SoPSingleSubRequestSendType.PARALLEL:
            for subrequest_key, subfunction_reqline in super_schedule_request._subfunction_reqline_table.items():
                for candidate_request in subfunction_reqline._candidate_request_list:
                    if candidate_request._status != target_schedule_action:
                        continue

                    # 미들웨어에게 현재 요청인 check 인지 confirm인지 알려주기 위해 trigger_msg에 status를 추가함.
                    candidate_request._trigger_msg._status = result_schedule_action.value.lower()
                    self._request_subaction(candidate_request)

            # 해당 super function action에 대한 subfunction들에게 subschedule요청을 보낸 후, 모든 subschedule 결과를 받을 때까지 기다린다.
            for subrequest_key, subfunction_reqline in super_schedule_request._subfunction_reqline_table.items():
                for candidate_request in subfunction_reqline._candidate_request_list:
                    if candidate_request._status != target_schedule_action:
                        continue
                    candidate_request._result_msg = candidate_request.get_result_msg(
                        timeout=timeout)
                    candidate_request._status = result_schedule_action
                    subschedule_result_msg: SoPSubScheduleResultMessage = candidate_request._result_msg

                    candidate_request.timer_end()
                    self.print_request_result(candidate_request, 'cyan')

                    # 굳이 구독 해제를 할 필요가 없다. 재호출될 가능성이 높음.
                    # self._unsubscribe_queue.put(subschedule_result_msg.topic())
                    # while not self._unsubscribe_queue.empty():
                    #     time.sleep(THREAD_TIME_OUT)
        elif self._single_request_mode == SoPSingleSubRequestSendType.SERIAL:
            for subrequest_key, subfunction_reqline in super_schedule_request._subfunction_reqline_table.items():
                for candidate_request in subfunction_reqline._candidate_request_list:
                    if candidate_request._status != target_schedule_action:
                        continue

                    # 미들웨어에게 현재 요청이 check 인지 confirm인지 알려주기 위해 trigger_msg에 status를 추가함.
                    candidate_request._trigger_msg._status = result_schedule_action.value.lower()
                    self._request_subaction(candidate_request)

                    candidate_request._result_msg = candidate_request.get_result_msg(
                        timeout=timeout)
                    candidate_request._status = result_schedule_action
                    subschedule_result_msg: SoPSubExecuteResultMessage = candidate_request._result_msg

                    candidate_request.timer_end()
                    self.print_request_result(candidate_request, 'cyan')

                    # 굳이 구독 해제를 할 필요가 없다. 재호출될 가능성이 높음.
                    # self._unsubscribe_queue.put(subschedule_result_msg.topic())
                    # while not self._unsubscribe_queue.empty():
                    #     time.sleep(THREAD_TIME_OUT)

        if result_schedule_action == SoPScheduleStatus.CHECK:
            super_schedule_request._check_duation = get_current_time() - \
                subschedule_action_start_time
        elif result_schedule_action == SoPScheduleStatus.CONFIRM:
            super_schedule_request._confirm_duation = get_current_time() - \
                subschedule_action_start_time
        super_schedule_request._status = result_schedule_action
        self.print_request_result(
            super_schedule_request, 'green')

    def _select_target_subfunction_by_policy(self, super_action_request: SoPSuperScheduleRequest) -> SoPSubScheduleRequest:
        for subfunction_reqline in self._subfunction_reqline_list:
            reqline_policy = subfunction_reqline._subfunction_type.get_policy()
            subrequest_key = make_sub_request_key(
                subfunction_reqline._subfunction_type.get_name(), subfunction_reqline._subrequest_order)
            target_subfunction_reqline = super_action_request._subfunction_reqline_table[
                subrequest_key]

            if reqline_policy == SoPPolicy.ALL:
                for candidate_request in target_subfunction_reqline._candidate_request_list:
                    if candidate_request._status == SoPScheduleStatus.CHECK:
                        candidate_request._status = SoPScheduleStatus.SELECT
            elif reqline_policy == SoPPolicy.SINGLE:
                while True:
                    selected_request = random.choice(
                        target_subfunction_reqline._candidate_request_list)
                    if selected_request._status == SoPScheduleStatus.CHECK:
                        selected_request._status = SoPScheduleStatus.SELECT
                        break

    def _check_parallel(self, super_action_request: SoPSuperScheduleRequest, timeout: float = 3) -> List[SoPSubScheduleRequest]:
        self._subschedule_action_parallel(
            super_action_request, SoPScheduleStatus.INIT, SoPScheduleStatus.CHECK, timeout)

    def _confirm_parallel(self, super_action_request: SoPSuperScheduleRequest, timeout: float = 3) -> bool:
        self._subschedule_action_parallel(
            super_action_request, SoPScheduleStatus.SELECT, SoPScheduleStatus.CONFIRM, timeout)

    def _subexecute_parallel(self, super_execute_request: SoPSuperExecuteRequest, timeout: float = 3) -> List[Union[SoPSubScheduleRequest, SoPSubExecuteRequest]]:
        # 병렬로 subaction 요청을 보낸다.
        for subrequest_key, subfunction_reqline in super_execute_request._subfunction_reqline_table.items():
            for target_request in subfunction_reqline._target_request_list:
                self._request_subaction(target_request)

        # 해당 super function action에 대한 subfunction들에게 subaction요청을 보낸 후, 모든 subaction 결과를 받을 때까지 기다린다.
        for subrequest_key, subfunction_reqline in super_execute_request._subfunction_reqline_table.items():
            for target_request in subfunction_reqline._target_request_list:
                target_request._result_msg = target_request.get_result_msg(
                    timeout=timeout)
                subexecute_msg: SoPSubExecuteMessage = target_request._trigger_msg
                subaction_result_msg: SoPSubExecuteResultMessage = target_request._result_msg

                target_request.timer_end()
                SOPLOG_DEBUG(
                    f'[{target_request._action_type.value.upper()} END] {subexecute_msg._subfunction_name}|{subexecute_msg._target_thing_name} duration: {target_request.duration():.4f} Sec', 'cyan')

                # 굳이 구독 해제를 할 필요가 없다. 재호출될 가능성이 높음.
                # self._unsubscribe_queue.put(subaction_result_msg.topic())
                # while not self._unsubscribe_queue.empty():
                #     time.sleep(THREAD_TIME_OUT)

                # subexecute 결과를 받은 후, 다시 넣는다. req() 함수에서 꺼내어 사용하기 위함.
                target_request.put_result_msg(subaction_result_msg)

    # def _subschedule_nonparallel(self, target_subfunction_list: List[SoPFunction], subschedule_result_list: List[SoPErrorType], super_schedule_msg: SoPSuperScheduleMessage):
    #     '''
    #         subschedule 요청을 직렬로 실행하는 함수.
    #         기존에 방식처럼 하나씩 요청을 보내고 응답을 받으면 다음 요청으로 넘어가는 방식.
    #     '''
    #     for target_subfunction in target_subfunction_list:
    #         self._request_subschedule(target_subfunction, super_schedule_msg)

    #         # 하나의 subfunction의 subschedule 결과를 받을 때까지 기다린다. 이후 다음 subfunction에게 subschedule 요청을 보내고 받는 것을 반복.
    #         for subschedule_info in self._subschedule_request_list:
    #             subschedule_msg: SoPSubScheduleMessage = subschedule_info['subschedule_msg']
    #             subfunction_check = subschedule_msg._subfunction_name == target_subfunction.get_name()
    #             target_thing_check = subschedule_msg._target_thing_name == target_subfunction.get_thing_name()
    #             target_middleware_check = subschedule_msg._target_middleware_name == target_subfunction.get_middleware_name()
    #             super_thing_check = subschedule_msg._super_thing_name == super_schedule_msg._super_thing_name
    #             # self._subschedule_request_list에 있는 request중에 target_subfunction에 해당하는 요청에 대한 결과를 찾는다.
    #             if subfunction_check and target_thing_check and target_middleware_check and super_thing_check:
    #                 result_queue: Queue = subschedule_info['result_queue']

    #                 subschedule_result_msg: SoPSubScheduleResultMessage = result_queue.get()
    #                 SOPLOG_DEBUG(
    #                     f'[SUBSCHEDULE END] {subschedule_result_msg._subfunction_name}|{subschedule_result_msg._target_thing_name} duration: {(subschedule_info["end_time"] - subschedule_info["start_time"]):.4f}', 'cyan')

    #                 self._unsubscribe_queue.put(subschedule_result_msg.topic())
    #                 while not self._unsubscribe_queue.empty():
    #                     time.sleep(THREAD_TIME_OUT)

    #                 subschedule_result_list.append(
    #                     subschedule_result_msg._error)

    def check_reqline_confirm(self, super_action_request: SoPSuperScheduleRequest) -> SoPErrorType:
        # 스케쥴링 과정에서 super function의 reqline 중 confirm 된 request가 하나도 없는 reqline이 존재한다면 에러를 발생시킨다.
        for k, subfunction_reqline in super_action_request._subfunction_reqline_table.items():
            for candidate_request in subfunction_reqline._candidate_request_list:
                if candidate_request._status == SoPScheduleStatus.CONFIRM:
                    break
            else:
                return SoPErrorType.FAIL
        else:
            return SoPErrorType.NO_ERROR

    def _super_action_wrapper(self, super_action_request: Union[SoPSuperScheduleRequest, SoPSuperExecuteRequest], hierarchical_service_table: Dict[str, List[SoPService]]):
        '''
            super function의 하위 함수에 대한 정보를 추출한다.
            service_list 구조는
            ============================================
            super_function -> sub_function_type_list
                        -> sub_function_list
            ============================================
            로 이루어져있다.
            sub_function_type_list과 sub_function_list는 독립적인 공간을 가진다.
            super_function 내부에 req함수 가 존재하여 사용자가 요청하고 싶은 subfunction이 명세되어있는데 여기서 명세되어지는
            subfunction은 실제 타겟 subfunction이 아닌 subfunction_type이다. 실제 subfunction 정보는 middleware로 부터 받은
            service_list를 통해 추출한다. 그리고 해당 정보는 super_function의 subfunction_list에 저장된다.
        '''

        try:
            super_action_error = SoPErrorType.FAIL
            super_request_key = make_super_request_key(
                super_action_request._trigger_msg._requester_middleware_name, super_action_request._trigger_msg._scenario)

            # 만약 super_schedule_msg이 SoPSuperScheduleMessage이 아니라면 에러를 발생시킨다.
            if not isinstance(super_action_request, (SoPSuperScheduleRequest, SoPSuperExecuteRequest)):
                SOPLOG_DEBUG(
                    f'[SUPER_SCHEDULE ERROR] Wrong SoPSuperScheduleMessage type: {type(super_action_request)}', 'red')
                raise Exception

            SOPLOG_DEBUG(
                f'[{super_action_request._action_type.value.upper()} START] -------- Start {self._name} {super_action_request._action_type.value} by {super_action_request._trigger_msg._scenario} scenario --------', 'green')

            if isinstance(super_action_request, SoPSuperScheduleRequest):
                hierarchical_function_service_table: List[SoPFunction] = hierarchical_service_table["function"]

                # 후보 subfunction들에 대해서 스케쥴링을 진행한다.
                if self._request_parallel:
                    super_action_request.generate_subschedule_request(
                        self._subfunction_reqline_list, hierarchical_function_service_table)
                    # TODO: 각 reqline마다 check, confirm이 이루어지고 나서 다음 reqline으로 넘어가야한다. 그게 제대로된 스케쥴링이다.
                    # 어느 한 reqline이 confirm 됨으로 인해서 다음 reqline의 스케쥴링에 영향을 주기 때문임.
                    # self._dfddf() # reqline을 돌면서 _check_parallel + _confirm_parallel
                    self._check_parallel(super_action_request, timeout=10)
                    self._select_target_subfunction_by_policy(
                        super_action_request)
                    self._confirm_parallel(super_action_request, timeout=10)
                else:
                    # TODO: update nonparallel feature
                    pass

                # 만약 현재 super function의 subfunction_list가 비어있는 경우 에러를 발생시킨다.
                if len(super_action_request._subfunction_reqline_table) == 0:
                    raise Exception(
                        f'No target_subfunction_list found in {self._name} super function')
            elif isinstance(super_action_request, SoPSuperExecuteRequest):
                # self._scheduling_table에서 해당 항목을 제거한다.
                super_action_request.exchange_argument()

                if self._request_parallel:
                    super_action_request._current_reqline_num = 0
                    self._subexecute_parallel(
                        super_action_request, timeout=10)
                else:
                    # TODO: update nonparallel feature
                    pass

                self._running = True

                super_execute_result = func_timeout(
                    self._timeout / 1000, self._func, args=(*tuple([super_request_key] + list(super_action_request._trigger_msg.tuple_arguments())), ))
        except KeyboardInterrupt as e:
            print_error(e)
            SOPLOG_DEBUG('Function execution exit by user', 'red')
            raise e
        except FunctionTimedOut as e:
            # print_error(e)
            SOPLOG_DEBUG(
                f'[FUNC TIMEOUT] {super_action_request._action_type.value} of {self._name} by scenario {super_action_request._trigger_msg._requester_middleware_name}|{super_action_request._trigger_msg._scenario} timeout...', 'red')
            super_action_error = SoPErrorType.TIMEOUT
            self._temporary_scheduling_table.pop(super_request_key)
            return False
        except Exception as e:
            print_error(e)
            SOPLOG_DEBUG(
                f'[{super_action_request._action_type.value.upper()} FAILED] {super_action_request._action_type.value} of {self._name} by scenario {super_action_request._trigger_msg._requester_middleware_name}|{super_action_request._trigger_msg._scenario} failed...', 'red')
            super_action_error = SoPErrorType.FAIL

            self._temporary_scheduling_table.pop(super_request_key)
            return False
        else:
            if isinstance(super_action_request, SoPSuperScheduleRequest):
                super_action_error = self.check_reqline_confirm(
                    super_action_request)
                super_execute_request = SoPSuperExecuteRequest()
                super_execute_request.generate_subexecute_request_list(
                    super_action_request)
                # super_execute_request._subexecute_request_list = [to_subexecute_request(
                #     subschedule_request) for subschedule_request in super_action_request.subschedule_request_target_list()]
                self._temporary_scheduling_table.pop(super_request_key)
                self._mapping_table[super_request_key] = super_execute_request
                # self.super_schedule_duration_list.append(
                #     super_action_request.duration)
            elif isinstance(super_action_request, SoPSuperExecuteRequest):
                pass
                # self.super_execute_duration_list.append(
                #     super_action_request.duration)

            super_action_error = SoPErrorType.NO_ERROR
            return True
        finally:
            if isinstance(super_action_request, SoPSuperScheduleRequest):
                super_schedule_msg: SoPSuperScheduleMessage = super_action_request._trigger_msg
                self.send_SM_RESULT_SCHEDULE(super_schedule_msg._super_function_name,
                                             super_schedule_msg._super_thing_name,
                                             super_schedule_msg._super_middleware_name,
                                             super_schedule_msg._requester_middleware_name,
                                             super_schedule_msg._scenario,
                                             super_action_error)
            elif isinstance(super_action_request, SoPSuperExecuteRequest):
                super_execute_msg: SoPSuperExecuteMessage = super_action_request._trigger_msg
                self.send_SM_RESULT_EXECUTE(super_execute_msg._super_function_name,
                                            super_execute_msg._super_thing_name,
                                            super_execute_msg._super_middleware_name,
                                            super_execute_msg._requester_middleware_name,
                                            super_execute_msg._scenario,
                                            self._return_type,
                                            super_execute_result,
                                            super_action_error)
            super_action_request.timer_end()
            SOPLOG_DEBUG(
                f'[{super_action_request._action_type.value.upper()} FINISH] {super_action_request._action_type.value} of {self._name} by scenario {super_action_request._trigger_msg._requester_middleware_name}|{super_action_request._trigger_msg._scenario} finish. duration: {super_action_request.duration():.4f} Sec', 'green')

    def super_action(self, super_action_request: Union[SoPSuperScheduleRequest, SoPSuperExecuteRequest], hierarchical_service_table: Dict[str, List[SoPService]]) -> None:
        super_action_thread = SoPThread(
            func=self._super_action_wrapper,
            name=f'{self._func.__name__}_{super_action_request._action_type.value}_thread',
            daemon=True,
            arg_list=(super_action_request, hierarchical_service_table, ))
        super_action_thread.start()

    def add_subfunction_reqline_info(self, subfunction_name: str, arg_list: Union[Tuple[SoPArgument], Tuple], tag_list: List[SoPTag], policy: SoPPolicy):
        if not arg_list:
            arg_list = []
            sop_arg_list = []
        else:
            sop_arg_list = list(arg_list)
            for i, arg in enumerate(sop_arg_list):
                if not isinstance(arg, SoPArgument):
                    sop_arg_list[i] = SoPArgument(
                        name=f'FIXED_ARG({arg})',
                        type=SoPType.to_soptype(type(arg)))

        subfunction_type = SoPFunction(name=subfunction_name,
                                       arg_list=sop_arg_list,
                                       tag_list=tag_list,
                                       policy=policy)
        self._add_subfunction_reqline(
            SoPSubFunctionReqline(subfunction_type=subfunction_type, argument_list=arg_list))
        SOPLOG_DEBUG(
            f'Extract subfunction_reqline finish. super function: {self._name}, subfunction: {subfunction_name}, arg_list: [{", ".join([sop_arg._name for sop_arg in sop_arg_list])}] tag_list: [{", ".join([str(tag) for tag in tag_list])}]', 'green')
        return True

    def put_subaction_result(self, super_request_key: str, subrequest_key: str, subaction_result_msg: Union[SoPSubScheduleResultMessage, SoPSubExecuteResultMessage]) -> None:
        '''
            super thing에 의해 호출되어 super thing이 받은 subaction결과를 super function에게 전달한다.
        '''

        if isinstance(subaction_result_msg, SoPSubScheduleResultMessage):
            action_table = self._temporary_scheduling_table
        elif isinstance(subaction_result_msg, SoPSubExecuteResultMessage):
            action_table = self._mapping_table

        if super_request_key not in action_table:
            SOPLOG_DEBUG(
                f'Could not find key {super_request_key} in subexecute_request_list...', 'red')
            raise Exception

        super_action_request = action_table[super_request_key]
        super_action_request.put_subresult_msg(
            subrequest_key, subaction_result_msg)

    def send_SM_SCHEDULE(self, subschedule_msg: SoPSubScheduleMessage) -> None:
        self._publish_queue.put(subschedule_msg.mqtt_message())

    def send_SM_RESULT_SCHEDULE(self, super_function_name: str, super_thing_name: str, super_middleware_name: str, requester_middleware_name: str,
                                scenario: str, error: SoPErrorType) -> None:
        self._publish_queue.put(SoPSuperScheduleResultMessage(
            super_function_name, super_thing_name, super_middleware_name, requester_middleware_name, scenario=scenario, error=error).mqtt_message())

    def send_SM_EXECUTE(self, subexecute_msg: SoPSubExecuteMessage) -> None:
        self._publish_queue.put(subexecute_msg.mqtt_message())

    def send_SM_RESULT_EXECUTE(self, super_function_name: str, super_thing_name: str, super_middleware_name: str, requester_middleware_name: str,
                               scenario: str, return_type: SoPType, return_value: Union[int, float, bool, str], error: SoPErrorType) -> None:
        self._publish_queue.put(SoPSuperExecuteResultMessage(
            super_function_name, super_thing_name, super_middleware_name, requester_middleware_name,
            scenario=scenario, return_type=return_type, return_value=return_value, error=error).mqtt_message())

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

    def get_subfunction_type_list(self) -> List[SoPSubFunctionReqline]:
        return self._subfunction_reqline_list

    def get_first_execute(self) -> bool:
        return self._first_execute

    # ==================================
    #             _    _
    #            | |  | |
    #  ___   ___ | |_ | |_   ___  _ __
    # / __| / _ \| __|| __| / _ \| '__|
    # \__ \|  __/| |_ | |_ |  __/| |
    # |___/ \___| \__| \__| \___||_|
    # ==================================

    def set_subfunction_type_list(self, target_subfunction_reqline_list: List[SoPSubFunctionReqline]) -> None:
        self._subfunction_reqline_list = target_subfunction_reqline_list

    def set_first_execute(self, first_execute: bool) -> None:
        self._first_execute = first_execute

    # for super service
    def set_subscribe_queue(self, queue: Queue):
        self._subscribe_queue = queue

    def set_unsubscribe_queue(self, queue: Queue):
        self._unsubscribe_queue = queue
