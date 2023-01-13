#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests


class ResponseInfo(object):

    def __init__(self):
        self.code = 500
        self.msg = ''
        self.data = None

    def __str__(self):
        return self.__class__.__name__ + '(' + ', '.join(['%s: %s' % item for item in self.__dict__.items()]) + ')'

    @staticmethod
    def success(data=''):
        success_info = ResponseInfo()
        success_info.code = 200
        success_info.msg = 'successfully'
        success_info.data = data
        return success_info

    @staticmethod
    def error(code: int = 500, msg: str = 'Server internal error'):
        error_info = ResponseInfo()
        error_info.code = code
        error_info.msg = msg
        return error_info


if __name__ == '__main__':
    pass
