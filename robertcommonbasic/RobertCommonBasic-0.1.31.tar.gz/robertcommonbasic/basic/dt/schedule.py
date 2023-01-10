import copy
import re
from datetime import datetime
from enum import Enum
from functools import reduce, total_ordering
from typing import List, Tuple, Optional
from ..error.utils import InputDataError


class ScheduleTimeFormat(Enum):
    month = 'M'
    weekday = 'WD'
    day = 'D'
    hour = 'h'
    minute = 'm'


SCHEDULE_TIMEFORMAT_ORDER = ['weekday', 'day', 'hour', 'minute']


@total_ordering
class ScheduleTime:
    def __init__(self,
                 month: Optional[int] = None,
                 weekday: Optional[int] = None,
                 day: Optional[int] = None,
                 hour: Optional[int] = None,
                 minute: Optional[int] = None):
        self.weekday = weekday
        self.hour = hour
        self.minute = minute
        self.month = month
        self.day = day

    def compare(self, st2):
        fields = self.get_compare_fields()
        try:
            assert fields == st2.get_compare_fields()
        except Exception:
            raise InputDataError('schedule time compare fields must equal')
        for field in fields:
            st1_field = getattr(self, field)
            st2_field = getattr(st2, field)
            if st1_field == st2_field:
                continue
            elif st1_field > st2_field:
                return 1
            elif st1_field < st2_field:
                return -1
        return 0

    def __eq__(self, st2):
        return self.compare(st2) == 0

    def __lt__(self, st2):
        return self.compare(st2) < 0

    @classmethod
    def parse_from_datetime(cls, dt: datetime) -> 'ScheduleTime':
        args = {
            'weekday': dt.weekday() + 1,
            'hour': dt.hour,
            'day': dt.day,
            'minute': dt.minute
        }
        return cls(**args)

    @classmethod
    def parse_from_str(cls, s: str) -> 'ScheduleTime':
        ts = re.findall(r'[a-zA-Z]+\d+', s)
        args = {}
        for t in ts:
            m = re.search(r'([a-zA-Z]+)(\d+)', t)
            if m:
                tf = ScheduleTimeFormat(m.group(1))
                tv = int(m.group(2))
                args[tf.name] = tv
        return cls(**args)

    @classmethod
    def split_time_str_range_list(
            cls, s: str) -> List[Tuple['ScheduleTime', 'ScheduleTime']]:
        time_from_to_list = []
        parts = s.split('|')
        for part in parts:
            t_list = part.split('~')
            time_from = cls.parse_from_str(t_list[0])
            time_to = cls.parse_from_str(t_list[1])
            time_from_to_list.append((time_from, time_to))
        return time_from_to_list

    def get_compare_fields(self):
        fields = [k for k, v in self.__dict__.items() if v is not None]
        fields_existed_with_order = sorted(
            fields, key=lambda t: SCHEDULE_TIMEFORMAT_ORDER.index(t))
        return fields_existed_with_order


def is_time_in_schedule_list(
        time_input: ScheduleTime,
        time_from_to_list: List[Tuple['ScheduleTime', 'ScheduleTime']]) -> int:
    is_in_schedule_list = [
        is_time_in_schedule(time_input, time_from, time_to)
        for time_from, time_to in time_from_to_list
    ]
    return int(reduce(lambda x, y: x or y, is_in_schedule_list))


def is_time_in_schedule(time_input: ScheduleTime, time_from: ScheduleTime,
                        time_to: ScheduleTime) -> bool:
    this_time_input = copy.deepcopy(time_input)
    ensure_field = time_from.get_compare_fields()
    for field in this_time_input.get_compare_fields():
        if field not in ensure_field:
            setattr(this_time_input, field, None)
        elif getattr(this_time_input, field) is None:
            raise InputDataError('compare field must equal')
    try:
        assert time_from <= time_to
    except Exception:
        raise InputDataError('time_from must be less equal than time_to')
    return (time_from <= this_time_input) and (this_time_input <= time_to)


def is_time_in_schedule_str(time_input: datetime,
                            time_schedule_str: str) -> int:
    """
    time_schedule_str: WD1h2~WD1h12|WD2h1~WD2h13
    """
    time_from_to_list = ScheduleTime.split_time_str_range_list(
        time_schedule_str)
    time_input_schedule = ScheduleTime.parse_from_datetime(time_input)
    return is_time_in_schedule_list(time_input_schedule, time_from_to_list)
