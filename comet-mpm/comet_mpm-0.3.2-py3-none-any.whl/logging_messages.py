# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.ml
#  Copyright (C) 2021 Comet ML INC
#  This file can not be copied and/or distributed without the express
#  permission of Comet ML Inc.
# *******************************************************

BATCH_SENDING_ERROR = "Error sending batch data to the backend"

BATCH_SENDING_EXCEPTION = "Unknown exception happened when sending data to the backend"

GEVENT_NOT_SUPPORTED = (
    "Using the MPM SDK with gevent is not officially supported, data loss might occurs"
)

ASYNCIO_SENDER_HARD_SHUTDOWN = "There are still some data in-flight and might be missing. Make sure to call CometMPM.join() manually to guarantee that all data has been sent to the Backend"

ERROR_QUANTILES_LIST_EMPTY = (
    "Error cannot compute distribution summary because the quantiles list is empty."
)
ERROR_QUANTILES_INVALID_VALUE = (
    "The quantile must be within [0,1]. The current min value %f and max %f"
)

LOGGING_DIRECTORY_CREATION_ERROR = "Cannot create path to log file %r"

LOGGING_LOG_FILE_OPEN_ERROR = "Cannot open log file %r; file logging is disabled"

INVALID_SETTING_DEFAULT_FALLBACK = "Some MPM settings values were invalid, default values were used instead, see below for the list"
