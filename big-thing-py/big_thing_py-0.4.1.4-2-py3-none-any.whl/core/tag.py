from big_thing_py.utils import *


class SoPTag:

    def __init__(self, name=''):
        self._name: str = name

    def __str__(self) -> str:
        return self._name

    def __eq__(self, o: object) -> bool:
        return isinstance(o, SoPTag) and o._name == self._name

    def dump(self):
        return {
            "name": self._name
        }

    # ====================================
    #               _    _
    #              | |  | |
    #   __ _   ___ | |_ | |_   ___  _ __
    #  / _` | / _ \| __|| __| / _ \| '__|
    # | (_| ||  __/| |_ | |_ |  __/| |
    #  \__, | \___| \__| \__| \___||_|
    #   __/ |
    #  |___/
    # ====================================

    def get_name(self):
        return self._name

    # ==================================
    #             _    _
    #            | |  | |
    #  ___   ___ | |_ | |_   ___  _ __
    # / __| / _ \| __|| __| / _ \| '__|
    # \__ \|  __/| |_ | |_ |  __/| |
    # |___/ \___| \__| \__| \___||_|
    # ==================================

    def set_name(self, name):
        self._name = name
