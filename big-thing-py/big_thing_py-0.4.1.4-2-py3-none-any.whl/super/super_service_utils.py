from big_thing_py.utils import *
from big_thing_py.core.function import *


class SoPScheduleStatus(Enum):
    INIT = 'init'
    CHECK = 'check'
    SELECT = 'select'
    CONFIRM = 'confirm'


class SoPSingleSubRequestSendType(Enum):
    PARALLEL = 0
    SERIAL = 1


class SoPSubfunctionCandidate:
    def __init__(self) -> None:
        self.single_type: List[SoPFunction] = []
        self.all_type: List[SoPFunction] = []


class OccupancyScenario():
    # TODO: RequestMiddleware 정보도 같이 있어야 한다.
    def __init__(self, name: str, action_type: SoPActionType) -> None:
        self.name = name
        self.action_type = action_type
        self.subaction_request_list = []


def request_function_service():
    pass


def req():
    pass


def r():
    pass
