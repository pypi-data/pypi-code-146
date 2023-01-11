from big_thing_py.common import *
from big_thing_py.common.request import *
from big_thing_py.common.mqtt_message import *
from big_thing_py.core.argument import *
from big_thing_py.core.service import *

from func_timeout import func_timeout, FunctionTimedOut


class SoPFunction(SoPService):
    def __init__(self, name: str = None, thing_name: str = None, middleware_name: str = None, tag_list: List[SoPTag] = [], desc: str = None, func: Callable = None, energy: float = None,
                 arg_list: List[SoPArgument] = [], return_type: SoPType = SoPType.UNDEFINED, exec_time: float = 10,
                 timeout: float = 10, policy: SoPPolicy = SoPPolicy.SINGLE) -> None:
        super().__init__(name=name, thing_name=thing_name,  middleware_name=middleware_name,
                         tag_list=tag_list, desc=desc, func=func, energy=energy)

        self._arg_list = arg_list
        self._return_type = return_type
        self._return_value = None
        self._exec_time = exec_time
        self._timeout = timeout

        self._running: bool = False
        self._policy = policy  # for super function feature

        # Queue
        self._publish_queue = None

    def __eq__(self, o: object) -> bool:
        arg_list_check = o._arg_list == self._arg_list
        return_type_check = o._return_type == self._return_type
        exec_time_check = o._exec_time == self._exec_time
        timeout_check = o._timeout == self._timeout

        return super().__eq__(o) and arg_list_check and return_type_check and exec_time_check and timeout_check

    # is_parallel은 현재 사용하지 않음 -> 추후에 사용할 수도 있음..
    def _wrapper(self, execute_request: SoPExecuteRequest) -> bool:
        execute_msg = execute_request._trigger_msg
        SOPLOG_DEBUG(
            f'[FUNC RUN] run {self._name} function by {execute_msg._scenario}', 'green')

        try:
            if not isinstance(execute_msg, SoPExecuteMessage):
                SOPLOG_DEBUG(
                    f'[FUNC ERROR] Wrong ExeucuteMessage type: {type(execute_msg)}', 'red')
                raise

            self._running = True
            error = None
            self._return_value = func_timeout(
                self._timeout, self._func, args=(*execute_msg.tuple_arguments(), ))
            execute_duration = execute_request.timer_end()
            result_msg = SoPExecuteResultMessage(execute_msg._function_name,
                                                 execute_msg._thing_name,
                                                 execute_msg._scenario,
                                                 self._return_type,
                                                 self._return_value,
                                                 error,
                                                 middleware_name=execute_request._trigger_msg._middleware_name,
                                                 request_ID=execute_request._trigger_msg._request_ID)
            execute_request.set_return_msg(result_msg)
        except KeyboardInterrupt as e:
            # TODO: for warpup main thread, but not test it yet
            print_error(e)
            SOPLOG_DEBUG('Function execution exit by user', 'red')
            raise e
        except FunctionTimedOut as e:
            # print_error(e)
            SOPLOG_DEBUG(
                f'[FUNC TIMEOUT] function {self._name} by scenario {execute_msg._scenario} was timeout!!!', 'yellow')
            error = SoPErrorType.TIMEOUT
        except Exception as e:
            print_error(e)
            SOPLOG_DEBUG(
                f'[FUNC ERROR] function {self._name} by scenario {execute_msg._scenario} is failed while executing!!!', 'red')
            error = SoPErrorType.FAIL
        else:
            SOPLOG_DEBUG(
                f'[FUNC FINISH] function {self._name} finish. -> return value : {self._return_value}, duration: {execute_duration:.4f} Sec', 'green')
            error = SoPErrorType.NO_ERROR
        finally:
            self._running = False
            self._send_TM_RESULT_EXECUTE(execute_msg._function_name,
                                         execute_msg._thing_name,
                                         self._return_type,
                                         self._return_value,
                                         execute_msg._scenario,
                                         error,
                                         middleware_name=execute_request._trigger_msg._middleware_name,
                                         request_ID=execute_request._trigger_msg._request_ID)

    def execute(self, execute_msg: SoPExecuteRequest) -> None:
        execute_thread = SoPThread(
            func=self._wrapper,
            name=f'{self._func.__name__}_thread',
            daemon=True,
            arg_list=(execute_msg, ))
        execute_thread.start()

    def _send_TM_RESULT_EXECUTE(self, function_name: str, thing_name: str,
                                return_type: SoPType, return_value: Union[str, float, bool], scenario: str, error: SoPErrorType,
                                middleware_name: str = '', request_ID: str = '') -> None:
        self._publish_queue.put(SoPExecuteResultMessage(
            function_name, thing_name, scenario, return_type, return_value, error, middleware_name=middleware_name, request_ID=request_ID).mqtt_message())

    def dump(self) -> Dict:
        return {
            "name": self._name,
            "description": self._desc,
            "exec_time": self._exec_time * 1000 if self._exec_time is not None else 0,
            "return_type": self._return_type.value,
            "energy": self._energy,
            "tags": [tag.dump() for tag in self._tag_list],
            "use_arg": 1 if self._arg_list else 0,
            "arguments": [argument.dump() for argument in self._arg_list] if self._arg_list else []
        }

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

    def get_exec_time(self) -> float:
        return self._exec_time

    def get_timeout(self) -> float:
        return self._timeout

    def get_arg_list(self) -> List[SoPArgument]:
        return self._arg_list

    def get_return_type(self) -> SoPType:
        return self._return_type

    def get_running(self) -> bool:
        return self._running

    def get_policy(self) -> SoPPolicy:
        return self._policy

    # ==================================
    #             _    _
    #            | |  | |
    #  ___   ___ | |_ | |_   ___  _ __
    # / __| / _ \| __|| __| / _ \| '__|
    # \__ \|  __/| |_ | |_ |  __/| |
    # |___/ \___| \__| \__| \___||_|
    # ==================================

    def set_exec_time(self, exec_time: float) -> None:
        self._exec_time = exec_time

    def set_timeout(self, timeout: float) -> None:
        self._timeout = timeout

    def set_arg_list(self, arg_list: List[SoPArgument]) -> None:
        self._arg_list = arg_list

    def set_return_type(self, return_type: SoPType) -> None:
        self._return_type = return_type

    def set_running(self, running: bool) -> None:
        self._running = running

    def set_policy(self, policy: SoPPolicy) -> None:
        self._policy = policy

    # for link to big_thing's publish_queue
    def set_publish_queue(self, queue: Queue):
        self._publish_queue = queue
