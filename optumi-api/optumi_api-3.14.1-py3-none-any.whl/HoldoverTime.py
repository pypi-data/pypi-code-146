##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi


class HoldoverTime:
    def __init__(self, minutes: int = 0, hours: int = 0):
        self._seconds = (60 * minutes) + (60 * 60 * hours)

    @property
    def seconds(self):
        return self._seconds

    def __str__(self):
        return str(self._seconds // 60) + " min"
