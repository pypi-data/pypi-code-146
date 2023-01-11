# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
class UserInput:
    PARAMETER_VALUE = 6
    QUERYSTRING = 7
    METHOD = 22
    UNKNOWN = 99

    _TYPE_TO_STR = {
        PARAMETER_VALUE: "PARAMETER_VALUE",
        QUERYSTRING: "QUERYSTRING",
        METHOD: "METHOD",
        UNKNOWN: "UNKNOWN",
    }

    def __init__(self, input_type, key, value, path="", matcher_ids=None,
                 document_type=0):
        self.input_type = input_type
        self.key = key
        self.value = value
        self.path = path
        self.matcher_ids = [] if matcher_ids is None else matcher_ids

        self.document_type = document_type

    @classmethod
    def type_to_str(cls, intput_type: int) -> str:
        """
        Convert int to str input type
        """
        return cls._TYPE_TO_STR.get(intput_type, "")

