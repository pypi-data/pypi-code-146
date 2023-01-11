# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import ctypes
from enum import IntEnum

from contrast.agent import agent_lib
from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")

__all__ = [
    "evaluate_header_input",
    "evaluate_input_by_type",
    "initialize_input_tracing",
    "check_sql_injection_query",
    "check_cmd_injection_query",
    "map_result_and_free_eval_result",
    "map_result_and_free_check_query_sink_result",
    "DBType",
    "BodyType",
]

# These are rules we do not have an implementation for yet
# Other rule IDs where added directly into the protect rule class
SSJS_INJECTION_RULE_ID = 1 << 7


class BodyType(IntEnum):
    JSON = 1
    XML = 2


class DBType(IntEnum):
    DB2 = 1
    MYSQL = 2
    ORACLE = 3
    POSTGRES = 4
    SQLITE = 5
    SQL_SERVER = 6
    UNKNOWN = 7

    @staticmethod
    def from_str(label):
        label = label.upper()
        try:
            return DBType[label]
        except KeyError:
            if label == "SQLITE3":
                return DBType.SQLITE
            if label == "POSTGRESQL":
                return DBType.POSTGRES
            if label in ("SQL SERVER", "SQL_SERVER", "SQLSERVER"):
                return DBType.SQL_SERVER

            return DBType.UNKNOWN


class CCheckQuerySinkResult(ctypes.Structure):
    _fields_ = [
        ("start_index", ctypes.c_ulonglong),
        ("end_index", ctypes.c_ulonglong),
        ("boundary_overrun_index", ctypes.c_ulonglong),
        ("input_boundary_index", ctypes.c_ulonglong),
    ]


class InputAnalysisResult:
    def __init__(self, input_value, value, ceval_results):
        self.rule_id = None
        self.input_type = None
        self.score = None
        self.key = None
        self.value = None
        self.path = None
        self.ids = None

        if (
            isinstance(ceval_results, agent_lib.CONSTANTS.CEvalResult)
            and input_value is not None
            and isinstance(value, str)
        ):
            self.rule_id = ceval_results.rule_id
            self.input_type = ceval_results.input_type
            self.score = ceval_results.score
            self.key = input_value
            self.value = value
            self.path = ""
            self.ids = []


class SQLInjectionResult:
    def __init__(self, sql_query, input_index, input_len, ccheck_query_sink_result):
        self.boundary_overrun_index = None
        self.end_index = None
        self.input_boundary_index = None
        self.start_index = None
        self.input_query = None
        self.input_index = None
        self.input_len = None

        if (
            isinstance(ccheck_query_sink_result, CCheckQuerySinkResult)
            and isinstance(sql_query, str)
            and isinstance(input_index, int)
            and isinstance(input_len, int)
        ):
            self.boundary_overrun_index = (
                ccheck_query_sink_result.boundary_overrun_index
            )
            self.end_index = ccheck_query_sink_result.end_index
            self.input_boundary_index = ccheck_query_sink_result.input_boundary_index
            self.start_index = ccheck_query_sink_result.start_index
            self.input_query = sql_query
            self.input_index = input_index
            self.input_len = input_len


def initialize_input_tracing():
    # This function is necessary for now because we have to conditionally import agent_lib.LIB_CONTRAST
    # When we get to the point where we always use agent lib we would define this outside of a function
    if agent_lib.LIB_CONTRAST is None:
        return

    agent_lib.LIB_CONTRAST.evaluate_header_input.argtypes = (
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_longlong,
        ctypes.c_longlong,
        ctypes.POINTER(ctypes.c_size_t),
        ctypes.POINTER(ctypes.POINTER(agent_lib.CONSTANTS.CEvalResult)),
    )

    agent_lib.LIB_CONTRAST.check_sql_injection_query.argtypes = (
        ctypes.c_uint32,
        ctypes.c_uint32,
        ctypes.c_uint32,
        ctypes.c_char_p,
        ctypes.POINTER(ctypes.POINTER(CCheckQuerySinkResult)),
    )

    agent_lib.LIB_CONTRAST.evaluate_header_input.restype = ctypes.c_int
    agent_lib.LIB_CONTRAST.check_sql_injection_query.restype = ctypes.c_int


def evaluate_header_input(header_name, header_value, rules, worth_watching):
    evaluations = []

    if agent_lib.LIB_CONTRAST is None:
        return evaluations

    if rules == 0:
        return evaluations

    def is_valid_return(code):
        return code == 0

    name = ctypes.c_char_p(bytes(header_name, "utf8"))
    value = ctypes.c_char_p(bytes(header_value, "utf8"))
    results_len = ctypes.c_size_t()
    results = ctypes.POINTER(agent_lib.CONSTANTS.CEvalResult)()

    ret = agent_lib.call(
        agent_lib.LIB_CONTRAST.evaluate_header_input,
        is_valid_return,
        name,
        value,
        rules,
        worth_watching,
        ctypes.byref(results_len),
        ctypes.byref(results),
    )

    map_result_and_free_eval_result(
        ret,
        results,
        results_len,
        header_name,
        header_value,
        is_valid_return,
        evaluations,
    )
    return evaluations


def evaluate_input_by_type(input_type, input_value, rules, worth_watching):
    evaluations = []

    if agent_lib.LIB_CONTRAST is None:
        return evaluations

    if rules == 0:
        return evaluations

    def is_valid_return(code):
        return code == 0

    name = ctypes.c_char_p(bytes(input_value, "utf8"))
    value = ctypes.c_long(input_type)
    results_len = ctypes.c_size_t()
    results = ctypes.POINTER(agent_lib.CONSTANTS.CEvalResult)()

    ret = agent_lib.call(
        agent_lib.LIB_CONTRAST.evaluate_input,
        is_valid_return,
        name,
        value,
        rules,
        worth_watching,
        ctypes.byref(results_len),
        ctypes.byref(results),
    )

    map_result_and_free_eval_result(
        ret, results, results_len, name, input_value, is_valid_return, evaluations
    )
    return evaluations


def check_sql_injection_query(
    user_input_start_index, user_input_len, db_type, built_sql_query
):
    if agent_lib.LIB_CONTRAST is None:
        return None

    def is_valid_return(code):
        return -1 <= code <= 0

    input_index = ctypes.c_uint32(user_input_start_index)
    input_len = ctypes.c_uint32(user_input_len)
    db_type = ctypes.c_uint32(db_type)
    sql_query = ctypes.c_char_p(bytes(built_sql_query, "utf8"))
    results = ctypes.POINTER(CCheckQuerySinkResult)()

    ret = agent_lib.call(
        agent_lib.LIB_CONTRAST.check_sql_injection_query,
        is_valid_return,
        input_index,
        input_len,
        db_type,
        sql_query,
        ctypes.byref(results),
    )

    evaluation = map_result_and_free_check_query_sink_result(
        ret,
        results,
        built_sql_query,
        user_input_start_index,
        user_input_len,
        is_valid_return,
    )
    return evaluation


def check_cmd_injection_query(user_input_start_index, user_input_len, user_input_txt):
    if agent_lib.LIB_CONTRAST is None:
        return None

    def is_valid_return(code):
        return -1 <= code <= 0

    input_index = ctypes.c_uint32(user_input_start_index)
    input_len = ctypes.c_uint32(user_input_len)
    cmd_text = ctypes.c_char_p(bytes(user_input_txt, "utf8"))
    results = ctypes.POINTER(CCheckQuerySinkResult)()

    ret = agent_lib.call(
        agent_lib.LIB_CONTRAST.check_cmd_injection_query,
        is_valid_return,
        input_index,
        input_len,
        cmd_text,
        ctypes.byref(results),
    )

    evaluation = map_result_and_free_check_query_sink_result(
        ret,
        results,
        user_input_txt,
        user_input_start_index,
        user_input_len,
        is_valid_return,
    )
    return evaluation


def map_result_and_free_eval_result(
    ret, results, results_len, name, value, is_valid_return, evaluations
):
    if ret == 0 and bool(results) and results_len.value > 0:
        for i in range(results_len.value):
            evaluations.append(InputAnalysisResult(name, value, results[i]))

        # ctypes does not have OOR (original object return), it constructs a new,
        # equivalent object each time you retrieve an attribute.
        # So we can free right after we create our list
        agent_lib.call(
            agent_lib.LIB_CONTRAST.free_eval_result,
            is_valid_return,
            results,
        )


def map_result_and_free_check_query_sink_result(
    ret, results, sql_query, input_index, input_len, is_valid_return
):
    if ret == 0 and bool(results):
        evaluation = SQLInjectionResult(
            sql_query, input_index, input_len, results.contents
        )

        # ctypes does not have OOR (original object return), it constructs a new,
        # equivalent object each time you retrieve an attribute.
        # So we can free right after we create our list
        agent_lib.call(
            agent_lib.LIB_CONTRAST.free_check_query_sink_result,
            is_valid_return,
            results,
        )

        return evaluation
    return None
