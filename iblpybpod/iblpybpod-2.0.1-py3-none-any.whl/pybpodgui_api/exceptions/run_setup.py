# !/usr/bin/python3
# -*- coding: utf-8 -*-

from pybpodgui_api.exceptions.api_error import APIError


class RunSetupError(APIError):
    """ Exception raised when a setup operation fails"""
    pass
