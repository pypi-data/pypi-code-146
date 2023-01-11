#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by iprobeyang@gmail.com 2021/4/12
"""


class ReportStruct:
    def __init__(self):
        self.product_code = ""  # pc
        self.app_code = ""  # ac
        self.service_name = ""  # sn
        self.service_instance = "" # si
        self.env_code = ""  # e
        self.tenant_code = ""  # tn
        self.user_code = ""  # u
        self.trace_id = ""  # id
        self.parent_span_id = ""  # p
        self.span_id = ""  # s
        self.span_type = 0  # t
        self.span_layer = 0  # y
        self.start_time = 0  # ts
        self.end_time = 0  # te
        self.duration = 0  # d
        self.component = ""  # c
        self.operation_name = ""  # o
        self.peer = ""  # r
        self.is_error = False  # er
        self.tags = None  # g
        self.logs = None  # l

    @staticmethod
    def convert(obj):
        """
        将数据转成规定格式
        :param obj:
        :return:
        """
        data = {
            "pc": obj.product_code,
            "ac": obj.app_code,
            "sn": obj.service_name,
            "si": obj.service_instance,
            "e": obj.env_code,
            "tn": obj.tenant_code,
            "u": obj.user_code,
            "id": obj.trace_id,
            "p": obj.parent_span_id,
            "s": obj.span_id,
            "t": obj.span_type,
            "y": obj.span_layer,
            "ts": obj.start_time,
            "te": obj.end_time,
            "d": obj.duration,
            "c": obj.component,
            "o": obj.operation_name,
            "r": obj.peer,
            "er": obj.is_error,
            "g": obj.tags,
            "l": obj.logs,
            "tv": obj.tracker_version,
        }
        if not obj.logs:
            del data["l"]
        if not obj.tags:
            del data["g"]

        return data
