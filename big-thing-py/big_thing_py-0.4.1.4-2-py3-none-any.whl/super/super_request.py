from big_thing_py.common.request import *
from big_thing_py.common.mqtt_message import *
from big_thing_py.super.super_service_utils import *


class SoPSuperScheduleRequest(SoPRequest):
    def __init__(self, trigger_msg: SoPSuperScheduleMessage = None,
                 result_msg: SoPSuperScheduleResultMessage = None) -> None:
        super().__init__(trigger_msg, result_msg)
        self._action_type = SoPActionType.SUPER_SCHEDULE

        self._trigger_msg: SoPSuperScheduleMessage
        self._result_msg: SoPSuperScheduleResultMessage
        self._check_duation: float = 0.0
        self._confirm_duation: float = 0.0
        self._status: SoPScheduleStatus = SoPScheduleStatus.INIT
        self._subfunction_reqline_table: Dict[str, SoPSubFunctionReqline] = {}

    def set_result_msg(self, result_msg: SoPSuperScheduleResultMessage):
        self._result_msg = result_msg

    def get_result_msg(self):
        return self._result_msg

    def is_completed(self):
        if self._result_msg:
            return True
        else:
            return False

    def check_duarion(self):
        return self._check_duation

    def confirm_duarion(self):
        return self._confirm_duation

    def put_subresult_msg(self, subrequest_key: str, result_msg: SoPSubScheduleResultMessage, timeout: float = None):
        target_subfunction_reqline = self._subfunction_reqline_table[subrequest_key]
        if target_subfunction_reqline == None:
            raise Exception(
                f'No subfunction {subrequest_key} found in _subfunction_reqline_table')

        found_request = None
        for candidate_request in target_subfunction_reqline._candidate_request_list:
            thing_check = (
                candidate_request._trigger_msg._target_thing_name == result_msg._target_thing_name)
            middleware_check = (
                candidate_request._trigger_msg._target_middleware_name == result_msg._target_middleware_name)
            request_ID_check = (
                candidate_request._trigger_msg._request_ID == result_msg._request_ID)
            if thing_check and middleware_check and request_ID_check:
                found_request = candidate_request
                break

        if found_request:
            found_request.put_result_msg(result_msg, timeout=timeout)
        else:
            raise Exception(
                f'No subfunction {subrequest_key} found in _subfunction_reqline_table')

        return

    def generate_subschedule_request(self, subfunction_reqline_list: List['SoPSubFunctionReqline'], hierarchical_function_service_table: List[SoPFunction]):
        for subfunction_reqline in subfunction_reqline_list:
            target_subfunction_reqline = SoPSubFunctionReqline(subfunction_type=subfunction_reqline._subfunction_type,
                                                               subrequest_order=subfunction_reqline._subrequest_order,
                                                               argument_list=subfunction_reqline._argument_list)
            # TODO: 해당 로직 부분 분리하기
            candidate_request_list = []
            for function_service in hierarchical_function_service_table:
                name_check = (target_subfunction_reqline._subfunction_type.get_name()
                              == function_service.get_name())
                tag_check = set(target_subfunction_reqline._subfunction_type.get_tag_list(string_mode=True)).issubset(
                    set(function_service.get_tag_list(string_mode=True)))
                if name_check and tag_check:
                    subschedule_msg = SoPSubScheduleMessage(function_service.get_name(),
                                                            function_service.get_thing_name(),
                                                            function_service.get_middleware_name(),
                                                            self._trigger_msg._requester_middleware_name,
                                                            self._trigger_msg._super_thing_name,
                                                            self._trigger_msg._super_function_name,
                                                            target_subfunction_reqline._subrequest_order,
                                                            self._trigger_msg._scenario,
                                                            self._trigger_msg._period,
                                                            request_ID=None)
                    subschedule_request = SoPSubScheduleRequest(trigger_msg=subschedule_msg,
                                                                subfunction=function_service)
                    candidate_request_list.append(subschedule_request)

            target_subfunction_reqline._candidate_request_list = candidate_request_list
            subreqeust_key = make_sub_request_key(
                target_subfunction_reqline._subfunction_type.get_name(), target_subfunction_reqline._subrequest_order)
            self._subfunction_reqline_table[subreqeust_key] = target_subfunction_reqline

            if len(target_subfunction_reqline._candidate_request_list) == 0:
                for function_service in hierarchical_function_service_table:
                    SOPLOG_DEBUG(
                        f'subfunction found! - {function_service.get_name()}|{function_service.get_thing_name()}|{function_service.get_middleware_name()}')
                raise Exception(
                    f'No candidate subfunction found in key:{subreqeust_key} {self._trigger_msg._super_function_name} super function')


class SoPSuperExecuteRequest(SoPRequest):
    def __init__(self, trigger_msg: SoPSuperExecuteMessage = None) -> None:
        super().__init__(trigger_msg, None)
        self._action_type = SoPActionType.SUPER_EXECUTE

        self._trigger_msg: SoPSuperExecuteMessage
        self._result_msg: SoPSuperExecuteResultMessage
        self._super_arg_list: List[SoPArgument] = None
        self._subfunction_reqline_table: Dict[str, SoPSubFunctionReqline] = {}
        self._current_reqline_num: int = 0

    def set_result_msg(self, result_msg: SoPSuperExecuteResultMessage):
        self._result_msg = result_msg

    def get_result_msg(self):
        return self._result_msg

    def get_arg_list(self):
        return self._super_arg_list

    def is_completed(self):
        if self._result_msg:
            return True
        else:
            return False

    def put_subresult_msg(self, subrequest_key: str, result_msg: SoPSubExecuteResultMessage, timeout: float = None):
        target_subfunction_reqline = self._subfunction_reqline_table[subrequest_key]
        if target_subfunction_reqline == None:
            raise Exception(
                f'No subfunction {subrequest_key} found in _subfunction_reqline_table')

        found_request = None
        for target_request in target_subfunction_reqline._target_request_list:
            thing_check = (
                target_request._trigger_msg._target_thing_name == result_msg._target_thing_name)
            middleware_check = (
                target_request._trigger_msg._target_middleware_name == result_msg._target_middleware_name)
            request_ID_check = (
                target_request._trigger_msg._request_ID == result_msg._request_ID)
            if thing_check and middleware_check and request_ID_check:
                found_request = target_request
                break

        if found_request:
            found_request.put_result_msg(result_msg, timeout=timeout)
        else:
            raise Exception(
                f'No subfunction {subrequest_key} found in _subfunction_reqline_table')

        return

    def get_subexecute_result_msg_list(self, subrequest_key: str, timeout: float = None) -> List[SoPSubExecuteResultMessage]:
        result_msg_list = []
        target_subfunction_reqline = self._subfunction_reqline_table[subrequest_key]
        for target_request in target_subfunction_reqline._target_request_list:
            result_msg_list.append(
                target_request.get_result_msg(timeout=timeout))
        return result_msg_list

    def make_real_subfunction_arguments(self, super_arg_list: List[SoPArgument], reqline_arg_list: Union[Tuple[SoPArgument], Tuple]):
        real_argument_list = []

        for i, reqline_arg in enumerate(reqline_arg_list):
            if isinstance(reqline_arg_list[i], SoPArgument):
                if reqline_arg in super_arg_list:
                    real_argument_list.append(dict(order=i,
                                                   value=self._trigger_msg._arguments[i]['value']))
            else:
                real_argument_list.append(dict(order=i, value=reqline_arg))
        return real_argument_list

    # def put_real_arguments(self, real_arguments: List[dict], subexecute_request: 'SoPSubExecuteRequest'):
    #     subexecute_request._trigger_msg._arguments = real_arguments
    #     for subexecute_request in self._subexecute_request_list:
    #         subexecute_msg = subexecute_request._trigger_msg
    #         subfunction_check = (
    #             subexecute_msg._subfunction_name == subexecute_request._subfunction.get_name())
    #         target_middleware_check = (
    #             subexecute_msg._target_middleware_name == subexecute_request._subfunction.get_middleware_name())
    #         target_thing_check = (
    #             subexecute_msg._target_thing_name == subexecute_request._subfunction.get_thing_name())
    #         if subfunction_check and target_middleware_check and target_thing_check:
    #             subexecute_msg._arguments = real_arguments

    def generate_subexecute_request_list(self, super_schedule_request: 'SoPSuperScheduleRequest' = None):
        # schedule 단계에서 SoPSuperExecuteRequest를 생성한다.
        if super_schedule_request:
            for subrequest_key, subfunction_reqline in super_schedule_request._subfunction_reqline_table.items():
                self._subfunction_reqline_table[subrequest_key] = SoPSubFunctionReqline(subfunction_type=subfunction_reqline._subfunction_type,
                                                                                        subrequest_order=subfunction_reqline._subrequest_order,
                                                                                        candidate_request_list=subfunction_reqline._candidate_request_list,
                                                                                        argument_list=subfunction_reqline._argument_list)
                target_request_list = []
                for candidate_request in subfunction_reqline._candidate_request_list:
                    if candidate_request._status == SoPScheduleStatus.CONFIRM:
                        target_request_list.append(
                            to_subexecute_request(candidate_request))
                self._subfunction_reqline_table[subrequest_key]._target_request_list = target_request_list

    def exchange_argument(self):
        # execute 단계에서 실제 execute를 하기 위해 argument를 추출한다.
        for subrequest_key, subfunction_reqline in self._subfunction_reqline_table.items():
            for target_request in subfunction_reqline._target_request_list:
                middleware_check = (target_request._trigger_msg._target_middleware_name ==
                                    target_request._subfunction.get_middleware_name())
                thing_check = (target_request._trigger_msg._target_thing_name ==
                               target_request._subfunction.get_thing_name())
                if thing_check and middleware_check:
                    real_subfunction_argument_list = self.make_real_subfunction_arguments(
                        self._super_arg_list, subfunction_reqline._argument_list)
                    target_request._trigger_msg._arguments = real_subfunction_argument_list


class SoPSubScheduleRequest(SoPRequest):
    def __init__(self, trigger_msg: SoPSubScheduleMessage = None,
                 result_mqtt_msg: SoPSubScheduleResultMessage = None, subfunction: SoPFunction = None) -> None:
        super().__init__(trigger_msg, result_mqtt_msg)
        self._action_type = SoPActionType.SUB_SCHEDULE

        self._trigger_msg: SoPSubScheduleMessage
        self._result_msg: SoPSubScheduleResultMessage
        self._subfunction = subfunction
        self._status: SoPScheduleStatus = SoPScheduleStatus.INIT
        self._result_queue = Queue()

    def put_result_msg(self, result_msg: SoPSubScheduleResultMessage, timeout: float = None):
        self._result_queue.put(result_msg, timeout=timeout)

    def get_result_msg(self, timeout: float = None):
        try:
            return self._result_queue.get(timeout=timeout)
        except Empty:
            raise FunctionTimedOut


class SoPSubExecuteRequest(SoPRequest):
    def __init__(self, trigger_msg: SoPSubExecuteMessage = None,
                 result_mqtt_msg: SoPSubExecuteResultMessage = None, subfunction: SoPFunction = None) -> None:
        super().__init__(trigger_msg, result_mqtt_msg)
        self._action_type = SoPActionType.SUB_EXECUTE

        self._trigger_msg: SoPSubExecuteMessage
        self._result_msg: SoPSubExecuteResultMessage
        self._subfunction = subfunction
        self._result_queue = Queue()

    def put_result_msg(self, result_msg: SoPSubExecuteResultMessage, timeout: float = None):
        self._result_queue.put(result_msg, timeout=timeout)

    def get_result_msg(self, timeout: float = None) -> SoPSubExecuteResultMessage:
        try:
            return self._result_queue.get(timeout=timeout)
        except Empty:
            raise FunctionTimedOut


class SoPSubFunctionReqline():
    def __init__(self, subfunction_type: SoPFunction, subrequest_order: int = None, candidate_request_list: List[SoPSubScheduleRequest] = [],
                 target_request_list: List[SoPSubExecuteRequest] = [], argument_list: Union[Tuple[SoPArgument], Tuple] = []) -> None:
        self._subfunction_type = subfunction_type
        self._subrequest_order = subrequest_order
        self._candidate_request_list = candidate_request_list
        self._target_request_list = target_request_list
        self._argument_list = argument_list

    def __deepcopy__(self, memodict={}):
        new_instance = SoPSubFunctionReqline(
            self._subfunction_type, self._subrequest_order, list(), list())
        new_instance.__dict__.update(self.__dict__)
        new_instance._subfunction_type = copy.deepcopy(
            self._subfunction_type, memodict)
        new_instance._subrequest_order = copy.deepcopy(
            self._subrequest_order, memodict)
        new_instance._candidate_request_list = list()
        new_instance._target_request_list = list()
        return new_instance


def to_subexecute_request(subschedule_request: SoPSubScheduleRequest) -> SoPSubExecuteRequest:
    subschedule_msg: SoPSubScheduleMessage = subschedule_request._trigger_msg
    subexecute_msg = SoPSubExecuteMessage(subschedule_msg._subfunction_name,
                                          subschedule_msg._target_thing_name,
                                          subschedule_msg._target_middleware_name,
                                          subschedule_msg._requester_middleware_name,
                                          subschedule_msg._super_thing_name,
                                          subschedule_msg._super_function_name,
                                          subschedule_msg._subrequest_order,
                                          subschedule_msg._scenario,
                                          request_ID=subschedule_msg._request_ID)
    subexecute_request = SoPSubExecuteRequest(
        trigger_msg=subexecute_msg, subfunction=subschedule_request._subfunction)
    return subexecute_request


def to_subschedule_request(subexecute_request: SoPSubExecuteRequest) -> SoPSubScheduleRequest:
    subexecute_msg: SoPSubExecuteMessage = subexecute_request._trigger_msg
    subschedule_msg = SoPSubScheduleMessage(subexecute_msg._subfunction_name,
                                            subexecute_msg._target_thing_name,
                                            subexecute_msg._target_middleware_name,
                                            subexecute_msg._requester_middleware_name,
                                            subexecute_msg._super_thing_name,
                                            subexecute_msg._super_function_name,
                                            subexecute_msg._subrequest_order,
                                            subexecute_msg._scenario,
                                            request_ID=subexecute_msg._request_ID)
    subschedule_request = SoPSubScheduleRequest(
        trigger_msg=subschedule_msg, subfunction=subexecute_request._subfunction)
    return subschedule_request
