from enum import Enum


class SoPErrorType(Enum):
    NO_ERROR = 0
    FAIL = -1
    TIMEOUT = -2
    NO_PARALLEL = -3
    DUPLICATE = -4
    UNDEFINED = -5

    @classmethod
    def to_soperrortype(cls, type: int):
        if type is not None:
            for soperrortype in SoPErrorType:
                if soperrortype.value == type:
                    return soperrortype
        else:
            return SoPErrorType.get(type)

    @classmethod
    def get(cls, type: int):
        try:
            if type is not None:
                for soperrortype in SoPErrorType:
                    if soperrortype.value == type:
                        return soperrortype
            else:
                return SoPErrorType.get(type)
        except Exception:
            return cls.UNDEFINED

    def __str__(self):
        return self.name


class SoPNetworkType(Enum):
    MQTT = 0
    API = 1
    BLUETOOTH = 2
    BLE = 3
    RF = 4
    XBEE = 5


class SoPType(Enum):
    UNDEFINED = -1
    INTEGER = 'int'
    DOUBLE = 'double'
    BOOL = 'bool'
    STRING = 'string'
    BINARY = 'binary'
    VOID = 'void'

    def __str__(self):
        return str(self.name)

    @classmethod
    def get(cls, name: str):
        try:
            if name is not None:
                for soptype in SoPType:
                    if soptype.value == name:
                        return soptype
            else:
                return cls.UNDEFINED
        except Exception:
            return cls.UNDEFINED

    @classmethod
    def to_pytype(cls, type: str):
        if isinstance(type, str):
            soptype = SoPType.get(type)

        if soptype == SoPType.INTEGER:
            return int
        elif soptype == SoPType.DOUBLE:
            return float
        elif soptype == SoPType.BOOL:
            return bool
        elif soptype == SoPType.STRING:
            return str
        elif soptype == SoPType.BINARY:
            return str
        elif soptype == SoPType.VOID:
            return None

    @classmethod
    def to_soptype(cls, type: type):
        if type == int:
            return SoPType.INTEGER
        elif type == float:
            return SoPType.DOUBLE
        elif type == bool:
            return SoPType.BOOL
        elif type == str:
            return SoPType.STRING
        elif type == str:
            return SoPType.BINARY
        elif type is None:
            return SoPType.VOID


class SoPActionType(Enum):
    """Action type enum."""
    REGISTER = 'register'
    EXECUTE = 'execute'
    ALIVE = 'alive'
    VALUE_PUBLISH = 'value_publish'
    AVAILABILITY = 'availability'
    REFRESH = 'refresh'
    SUPER_SCHEDULE = 'super_schedule'
    SUPER_EXECUTE = 'super_execute'
    SUB_SCHEDULE = 'sub_schedule'
    SUB_EXECUTE = 'sub_execute'


class SoPProtocolType:
    class Base(Enum):
        # ===============
        # ___  ___ _____
        # |  \/  ||_   _|
        # | .  . |  | |
        # | |\/| |  | |
        # | |  | |  | |
        # \_|  |_/  \_/
        # ===============

        # MT/RESULT/REGISTER/[ThingName]
        MT_RESULT_REGISTER = 'MT/RESULT/REGISTER/%s'

        # MT/RESULT/UNREGISTER/[ThingName]
        MT_RESULT_UNREGISTER = 'MT/RESULT/UNREGISTER/%s'

        # MT/EXECUTE/[FunctionName]/[ThingName]/([MiddlewareName]/[Request_ID])
        # Request_ID = requester_middleware@super_thing@super_function@subrequest_order
        MT_EXECUTE = 'MT/EXECUTE/%s/%s/%s/%s'

        # MT/RESULT/BINARY_VALUE/[ThingName]
        MT_RESULT_BINARY_VALUE = 'MT/RESULT/BINARY_VALUE/%s'

        # ===============
        #  _____ ___  ___
        # |_   _||  \/  |
        #   | |  | .  . |
        #   | |  | |\/| |
        #   | |  | |  | |
        #   \_/  \_|  |_/
        # ===============

        # TM/RESULT/EXECUTE/[FunctionName]/[ThingName]/([MiddlewareName]/[Request_ID])
        # Request_ID = requester_middleware@super_thing@super_function@subrequest_order
        TM_RESULT_EXECUTE = 'TM/RESULT/EXECUTE/%s/%s/%s/%s'

        # TM/REGISTER/[ThingName]
        TM_REGISTER = 'TM/REGISTER/%s'

        # TM/UNREGISTER/[ThingName]
        TM_UNREGISTER = 'TM/UNREGISTER/%s'

        # TM/ALIVE/[ThingName]
        TM_ALIVE = 'TM/ALIVE/%s'

        # # TM/VALUE_PUBLISH/[ThingName]/[ValueName]
        # TM_VALUE_PUBLISH = 'TM/VALUE_PUBLISH/%s/%s'

        # [ThingName]/[ValueName]
        TM_VALUE_PUBLISH = '%s/%s'

        def get_prefix(self):
            topic_tree = self.value.split('/')
            result_topic = []
            for topic_part in topic_tree:
                if topic_part != '%s':
                    result_topic.append(topic_part)

            return '/'.join(result_topic)

    class Manager(Enum):
        pass

        def get_prefix(self):
            topic_tree = self.value.split('/')
            result_topic = []
            for topic_part in topic_tree:
                if topic_part != '%s':
                    result_topic.append(topic_part)

            return '/'.join(result_topic)

    class Super(Enum):

        # ===============
        # ___  ___ _____
        # |  \/  |/  ___|
        # | .  . |\ `--.
        # | |\/| | `--. \
        # | |  | |/\__/ /
        # \_|  |_/\____/
        # ===============

        # MS/SCHEDULE/[SuperFunctionName]/[SuperThingName]/[SuperMiddlewareName]/[RequesterMWName]
        MS_SCHEDULE = 'MS/SCHEDULE/%s/%s/%s/%s'

        # MS/EXECUTE/[SuperFunctionName]/[SuperThingName]/[SuperMiddlewareName]/[RequesterMWName]
        MS_EXECUTE = 'MS/EXECUTE/%s/%s/%s/%s'

        # MS/RESULT/SCHEDULE/[TargetFunctionName]/[TargetThingName]/[TargetMiddlewareName]/[Request_ID]
        # Request_ID = requester_middleware@super_thing@super_function@subrequest_order
        MS_RESULT_SCHEDULE = 'MS/RESULT/SCHEDULE/%s/%s/%s/%s'

        # MS/RESULT/EXECUTE/[TargetFunctionName]/[TargetThingName]/[TargetMiddlewareName]/[Request_ID]
        # Request_ID = requester_middleware@super_thing@super_function@subrequest_order
        MS_RESULT_EXECUTE = 'MS/RESULT/EXECUTE/%s/%s/%s/%s'

        # MS/RESULT/SERVICE_LIST/[SuperThingName]
        MS_RESULT_SERVICE_LIST = 'MS/RESULT/SERVICE_LIST/%s'

        # ================
        #  _____ ___  ___
        # /  ___||  \/  |
        # \ `--. | .  . |
        #  `--. \| |\/| |
        # /\__/ /| |  | |
        # \____/ \_|  |_/
        # ================

        # SM/SCHEDULE/[TargetFunctionName]/[TargetThingName]/[TargetMiddlewareName]/[Request_ID]
        # Request_ID = requester_middleware@super_thing@super_function@subrequest_order
        SM_SCHEDULE = 'SM/SCHEDULE/%s/%s/%s/%s'

        # SM/EXECUTE/[TargetFunctionName]/[TargetThingName]/[TargetMiddlewareName]/[Request_ID]
        # Request_ID = requester_middleware@super_thing@super_function@subrequest_order
        SM_EXECUTE = 'SM/EXECUTE/%s/%s/%s/%s'

        # SM/RESULT/SCHEDULE/[SuperFunctionName]/[SuperThingName]/[SuperMiddlewareName]/[RequesterMWName]
        SM_RESULT_SCHEDULE = 'SM/RESULT/SCHEDULE/%s/%s/%s/%s'

        # SM/RESULT/EXECUTE/[SuperFunctionName]/[SuperThingName]/[SuperMiddlewareName]/[RequesterMWName]
        SM_RESULT_EXECUTE = 'SM/RESULT/EXECUTE/%s/%s/%s/%s'

        # SM/AVAILABILITY/[SuperThingName]
        SM_AVAILABILITY = 'SM/AVAILABILITY/%s'

        # SM/REFRESH/[SuperThingName]
        SM_REFRESH = 'SM/REFRESH/%s'

        # ==================
        #   _____    _____
        #  |  __ \  / ____|
        #  | |__) || |
        #  |  ___/ | |
        #  | |     | |____
        #  |_|      \_____|
        # ==================

        # PC/SCHEDULE/[TargetFunctionName]/[TargetThingName]/[TargetMiddlewareName]/[Request_ID]
        PC_SCHEDULE = 'PC/SCHEDULE/%s/%s/%s/%s'

        # PC/RESULT/SCHEDULE/[SuperFunctionName]/[SuperThingName]/[SuperMiddlewareName]/[RequesterMWName]
        PC_RESULT_SCHEDULE = 'PC/RESULT/SCHEDULE/%s/%s/%s/%s'

        # PC/EXECUTE/[TargetFunctionName]/[TargetThingName]/[TargetMiddlewareName]/[Request_ID]
        PC_EXECUTE = 'PC/EXECUTE/%s/%s/%s/%s'

        # PC/RESULT/EXECUTE/[SuperFunctionName]/[SuperThingName]/[SuperMiddlewareName]/[RequesterMWName]
        PC_RESULT_EXECUTE = 'PC/RESULT/EXECUTE/%s/%s/%s/%s'

        # PC/SERVICE_LIST/#
        PC_SERVICE_LIST = 'PC/SERVICE_LIST/%s'

        # PC/TRAVERSE/#
        PC_TRAVERSE = 'PC/TRAVERSE/%s'

        # ==================
        #    _____  _____
        #   / ____||  __ \
        #  | |     | |__) |
        #  | |     |  ___/
        #  | |____ | |
        #   \_____||_|
        # ==================

        # CP/SCHEDULE/[SuperFunctionName]/[SuperThingName]/[SuperMiddlewareName]/[RequesterMWName]
        CP_SCHEDULE = 'CP/SCHEDULE/%s/%s/%s/%s'

        # CP/RESULT/SCHEDULE/[TargetFunctionName]/[TargetThingName]/[TargetMiddlewareName]/[Request_ID]
        CP_RESULT_SCHEDULE = 'CP/RESULT/SCHEDULE/%s/%s/%s/%s'

        # CP/EXECUTE/[SuperFunctionName]/[SuperThingName]/[SuperMiddlewareName]/[Requester MWName]
        CP_EXECUTE = 'CP/EXECUTE/%s/%s/%s/%s'

        # CP/RESULT/EXECUTE/[TargetFunctionName]/[TargetThingName]/[TargetMiddlewareName]/[Request_ID]
        CP_RESULT_EXECUTE = 'CP/RESULT/EXECUTE/%s/%s/%s/%s'

        # CP/SERVICE_LIST/#
        CP_SERVICE_LIST = 'CP/SERVICE_LIST/%s'

        def get_prefix(self):
            topic_tree = self.value.split('/')
            result_topic = []
            for topic_part in topic_tree:
                if topic_part != '%s':
                    result_topic.append(topic_part)

            return '/'.join(result_topic)

    class WebClient(Enum):

        # ==================
        #   ______  __  __
        #  |  ____||  \/  |
        #  | |__   | \  / |
        #  |  __|  | |\/| |
        #  | |____ | |  | |
        #  |______||_|  |_|
        # ==================

        # EM/VERIFY_SCENARIO/[ClientID]
        EM_VERIFY_SCENARIO = 'EM/VERIFY_SCENARIO/%s'

        # EM/ADD_SCENARIO/[ClientID]
        EM_ADD_SCENARIO = 'EM/ADD_SCENARIO/%s'

        # EM/RUN_SCENARIO/[ClientID]
        EM_RUN_SCENARIO = 'EM/RUN_SCENARIO/%s'

        # EM/STOP_SCENARIO/[ClientID]
        EM_STOP_SCENARIO = 'EM/STOP_SCENARIO/%s'

        # EM/UPDATE_SCENARIO/[ClientID]
        EM_UPDATE_SCENARIO = 'EM/UPDATE_SCENARIO/%s'

        # EM/DELETE_SCENARIO/[ClientID]
        EM_DELETE_SCENARIO = 'EM/DELETE_SCENARIO/%s'

        # EM/ADD_TAG/[ClientID]
        EM_ADD_TAG = 'EM/ADD_TAG/%s'

        # EM/DELETE_TAG/[ClientID]
        EM_DELETE_TAG = 'EM/DELETE_TAG/%s'

        # EM/SET_ACCESS/[ClientID]
        EM_SET_ACCESS = 'EM/SET_ACCESS/%s'

        # EM/GET_TREE/[ClientID]
        EM_GET_TREE = 'EM/GET_TREE/%s'

        # EM/REFRESH/[ClientID]
        EM_REFRESH = 'EM/REFRESH/%s'

        # ==================
        #   __  __  ______
        #  |  \/  ||  ____|
        #  | \  / || |__
        #  | |\/| ||  __|
        #  | |  | || |____
        #  |_|  |_||______|
        # ==================

        # ME/RESULT/VERIFY_SCENARIO/[ClientID]
        ME_RESULT_VERIFY_SCENARIO = 'ME/RESULT/VERIFY_SCENARIO/%s'

        # ME/RESULT/RUN_SCENARIO/[ClientID]
        ME_RESULT_RUN_SCENARIO = 'ME/RESULT/RUN_SCENARIO/%s'

        # ME/RESULT/STOP_SCENARIO/[ClientID]
        ME_RESULT_STOP_SCENARIO = 'ME/RESULT/STOP_SCENARIO/%s'

        # ME/RESULT/SCHEDULE_SCENARIO/[ClientID]
        ME_RESULT_SCHEDULE_SCENARIO = 'ME/RESULT/SCHEDULE_SCENARIO/%s'

        # ME/RESULT/SCHEDULE_SCENARIO/[ClientID]
        ME_RESULT_ADD_SCENARIO = ME_RESULT_SCHEDULE_SCENARIO

        # ME/RESULT/SCHEDULE_SCENARIO/[ClientID]
        ME_RESULT_UPDATE_SCENARIO = ME_RESULT_SCHEDULE_SCENARIO

        # ME/RESULT/DELETE_SCENARIO/[ClientID]
        ME_RESULT_DELETE_SCENARIO = 'ME/RESULT/DELETE_SCENARIO/%s'

        # ME/RESULT/ADD_TAG/[ClientID]
        ME_RESULT_ADD_TAG = 'ME/RESULT/ADD_TAG/%s'

        # ME/RESULT/DELETE_TAG/[ClientID]
        ME_RESULT_DELETE_TAG = 'ME/RESULT/DELETE_TAG/%s'

        # ME/RESULT/SET_ACCESS/[ClientID]
        ME_RESULT_SET_ACCESS = 'ME/RESULT/SET_ACCESS/%s'

        # ME/RESULT/GET_TREE/[ClientID]
        ME_RESULT_GET_TREE = 'ME/RESULT/GET_TREE/%s'

        # ME/RESULT/SERVICE_LIST/[ClientID]
        ME_RESULT_SERVICE_LIST = 'ME/RESULT/SERVICE_LIST/%s'

        # ME/RESULT/SCENARIO_LIST/[ClientID]
        ME_RESULT_SCENARIO_LIST = 'ME/RESULT/SCENARIO_LIST/%s'

        # ME/NOTIFY_CHANGE/[ClientID]
        ME_NOTIFY_CHANGE = 'ME/NOTIFY_CHANGE/%s'

        def get_prefix(self):
            topic_tree = self.value.split('/')
            result_topic = []
            for topic_part in topic_tree:
                if topic_part != '%s':
                    result_topic.append(topic_part)

            return '/'.join(result_topic)


class HierarchyType(Enum):
    LOCAL = 0
    PARENT = 1
    CHILD = 2


class SoPServiceType(Enum):
    VALUE = 0
    FUNCTION = 1
    SUPERFUNCTION = 2
