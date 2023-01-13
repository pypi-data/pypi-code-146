# !/usr/bin/python3
# -*- coding: utf-8 -*-

from pybpodgui_api.exceptions.api_error import APIError


class BoardError(APIError):
    """ Exception raised when a board operation fails"""
    pass
