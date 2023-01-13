# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Custom logging formatters."""

from logging import Formatter

from flask import request
from flask_security import current_user

custom_format = """\
Message type:       %(levelname)s
Location:           %(pathname)s:%(lineno)d
Module:             %(module)s
Function:           %(funcName)s
Time:               %(asctime)s
User ID:            %(user_id)s
Request URL:        %(request_url)s


Message:

%(message)s
"""


class CustomFormatter(Formatter):
    """Custom logging formatter that provides more details."""

    def __init__(self, fmt=custom_format, **kwargs):
        super(CustomFormatter, self).__init__(fmt=fmt, **kwargs)

    def format(self, record):
        record.user_id = (
            current_user.id if current_user.is_authenticated else "Anonymous"
        )
        record.request_url = request.base_url
        return super(CustomFormatter, self).format(record)
