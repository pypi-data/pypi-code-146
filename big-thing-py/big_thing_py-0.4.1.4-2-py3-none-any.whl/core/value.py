from big_thing_py.core.service import *
import sys


class SoPValue(SoPService):

    def __init__(self, name: str = None, thing_name: str = None, middleware_name: str = None, tag_list: List[SoPTag] = [], desc: str = '', func: Callable = None, energy: float = None,
                 type: SoPType = SoPType.UNDEFINED, bound: Tuple[float, float] = (sys.float_info.min, sys.float_info.max), format: str = '', cycle: float = 10) -> None:
        super().__init__(name=name, thing_name=thing_name, middleware_name=middleware_name,
                         tag_list=tag_list, desc=desc, func=func, energy=energy)

        self._type: SoPType = type
        self._min: float = bound[0]
        self._max: float = bound[1]
        self._cycle: float = cycle

        # TODO: Add Enum class for format type in common.py
        self._format: str = format

        self._last_value: Union[float, str, bool] = None
        self._last_update_time: float = 0

        self._arg_list = []

    def __eq__(self, o: object) -> bool:
        type_check = (o._type == self._type)
        bound_check = (o._max == self._max and o._min == self._min)
        cycle_check = (o._cycle == self._cycle)
        format_check = (o._format == self._format)

        return super().__eq__(o) and type_check and bound_check and cycle_check and format_check

    def update(self, *arg_list, **kwargs) -> Union[float, bool]:
        try:
            new_value = self._func(*arg_list, **kwargs)
            self._last_update_time = get_current_time()

            if not self._last_value == new_value:
                self._last_value = new_value
                return new_value
            else:
                return None
        except Exception as e:
            print_error(e)
            return None

    def dump(self) -> Dict:
        return {
            "name": self._name,
            "description": self._desc,
            "tags": [tag.dump() for tag in self._tag_list],
            "type": self._type.value,
            "bound": {
                "min_value": self._min,
                "max_value": self._max
            },
            "format": self._format
        }

    def dump_pub(self) -> Dict:
        return {
            "type": self._type.value,
            "value": self._last_value
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

    def get_type(self) -> SoPType:
        return self._type

    def get_bound(self) -> Tuple[float, float]:
        return (self._min, self._max)

    def get_max(self) -> float:
        return self._max

    def get_min(self) -> float:
        return self._min

    def get_cycle(self) -> float:
        return self._cycle

    def get_format(self) -> str:
        return self._format

    def get_last_value(self) -> float:
        return self._last_value

    def get_last_update_time(self) -> float:
        return self._last_update_time

    def get_func(self) -> Callable:
        return self._func

    def get_arg_list(self) -> List:
        return self._arg_list

# ==================================
#             _    _
#            | |  | |
#  ___   ___ | |_ | |_   ___  _ __
# / __| / _ \| __|| __| / _ \| '__|
# \__ \|  __/| |_ | |_ |  __/| |
# |___/ \___| \__| \__| \___||_|
# ==================================

    def set_type(self, type: SoPType) -> None:
        self._type = type

    def set_bound(self, bound: Tuple[float, float]) -> None:
        self._min = bound[0]
        self._max = bound[1]

    def set_max(self, max: float) -> None:
        self._max = max

    def set_min(self, min: float) -> None:
        self._min = min

    def set_cycle(self, cycle: float) -> None:
        self._cycle = cycle

    def set_format(self, format: str) -> None:
        self._format = format

    def set_last_value(self, last_value: Union[float, str, bool]) -> None:
        self._last_value = last_value

    def set_last_update_time(self, last_update_time: float) -> None:
        self._last_update_time = last_update_time

    def set_func(self, func) -> None:
        self._func = func

    def set_arg_list(self, arg_list: List) -> None:
        self._arg_list = arg_list
