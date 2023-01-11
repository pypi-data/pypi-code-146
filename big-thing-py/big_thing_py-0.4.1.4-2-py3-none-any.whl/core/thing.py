from big_thing_py.core.function import *
from big_thing_py.core.value import *


class SoPThing:

    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True):
        # base info
        self._name = name
        self._middleware_name = None
        self._alive_cycle = alive_cycle
        self._last_alive_time = 0
        self._registered = False
        self._subscribed_topic_set: Set[str] = set()
        self._function_list: List[SoPFunction] = []
        self._value_list: List[SoPValue] = []

        self._is_parallel = is_parallel
        self._is_super = is_super

        if service_list == None:
            service_list = []

        for service in service_list:
            if isinstance(service, (SoPFunction, SoPValue)):
                self._add_service(service)
            else:
                SOPLOG_DEBUG(
                    f'[SoPThing] Service type error -> service type - {type(service)}')

    # for add overriding
    def __eq__(self, o: object) -> bool:
        check_instance = isinstance(o, SoPThing)
        check_name = (o._name == self._name)
        check_middleware_name = (o._middleware_name == self._middleware_name)

        return check_instance and check_name and check_middleware_name

    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    def _add_service(self, service: SoPService) -> None:
        if isinstance(service, SoPFunction):
            service: SoPFunction = service
            service.set_thing_name(self.get_name())
            self._function_list.append(service)
            return True
        elif isinstance(service, SoPValue):
            service: SoPValue = service
            self.get_value_list().append(service)
            value_getter_function = SoPFunction(name=f'__{service.get_name()}',
                                                thing_name=self.get_name(),
                                                tag_list=service.get_tag_list(),
                                                desc=service.get_desc(),
                                                func=service.get_func(),
                                                arg_list=[],
                                                return_type=service.get_type())
            self._function_list.append(value_getter_function)
            return True

    def _find_function(self, function_name: str) -> SoPFunction:
        for function in self._function_list:
            if function.get_name() == function_name:
                return function

    def dump(self) -> Dict:
        return {
            "alive_cycle": self._alive_cycle,
            "is_super": self._is_super,
            "is_parallel": self._is_parallel,
            "values": [value.dump() for value in self._value_list],
            "functions": [function.dump() for function in self._function_list]
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

    def get_name(self) -> str:
        return self._name

    def get_middleware_name(self) -> str:
        return self._middleware_name

    def get_last_alive_time(self) -> float:
        return self._last_alive_time

    def get_alive_cycle(self) -> float:
        return self._alive_cycle

    def get_subscribed_topic_set(self) -> Set[str]:
        return self._subscribed_topic_set

    def get_registered(self) -> bool:
        return self._registered

    def get_function_list(self) -> List[SoPFunction]:
        return self._function_list

    def get_value_list(self) -> List[SoPValue]:
        return self._value_list

    # ==================================
    #             _    _
    #            | |  | |
    #  ___   ___ | |_ | |_   ___  _ __
    # / __| / _ \| __|| __| / _ \| '__|
    # \__ \|  __/| |_ | |_ |  __/| |
    # |___/ \___| \__| \__| \___||_|
    # ==================================

    def set_name(self, name: str) -> None:
        self._name = name

    def set_middleware_name(self, middleware_name: str) -> None:
        self._middleware_name = middleware_name

    def set_last_alive_time(self, last_alive_time: float) -> None:
        self._last_alive_time = last_alive_time

    def set_alive_cycle(self, alive_cycle: float) -> None:
        self._alive_cycle = alive_cycle

    def set_subscribe_topic_set(self, subscribe_topic_set: Set[str]) -> None:
        self._subscribed_topic_set = subscribe_topic_set

    def set_registered(self, registered: bool) -> None:
        self._registered = registered
