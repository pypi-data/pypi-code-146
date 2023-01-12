import sys
from tomwer.app.canvas_launcher.mainwindow import OMain as QMain
from tomwer.core.utils.resource import increase_max_number_file
import tomwer.version
import tomoscan.version
import platform
import psutil
import logging

_logger = logging.getLogger(__name__)

try:
    import nxtomomill.version
except ImportError:
    has_nxtomomill = False
else:
    has_nxtomomill = True
try:
    import nabu
except ImportError:
    has_nabu = False
else:
    has_nabu = True


def print_versions():
    print(f"tomwer version is {tomwer.version.version}")
    print(f"tomoscan version is {tomoscan.version.version}")
    if has_nxtomomill:
        print(f"nxtomomill version is {nxtomomill.version.version}")
    if has_nabu:
        print(f"nabu version is {nabu.version}")
    if platform.system() == "Linux":
        try:
            free_home_space = psutil.disk_usage("/home").free
        except OSError:
            pass
        else:
            if free_home_space < 100 * 1024 * 1024:
                # if no space Qt might fail to create the display and log file not be created
                _logger.warning(
                    f"only {free_home_space / 1024} ko available. Display might fail"
                )


def main(argv=None):
    print_versions()
    increase_max_number_file()
    return QMain().run(argv)


if __name__ == "__main__":
    sys.exit(main())
