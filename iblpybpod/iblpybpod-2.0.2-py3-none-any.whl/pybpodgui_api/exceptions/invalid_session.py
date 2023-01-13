# !/usr/bin/python3
# -*- coding: utf-8 -*-


from pybpodgui_api.exceptions.api_error import APIError


class InvalidSessionError(APIError):
    """ Exception raised when an invalid session is loaded"""

    def __init__(self, value, session_path=None, original_exception=None):
        APIError.__init__(self, value, original_exception)
        self.session_path = session_path
