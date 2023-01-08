"""wia_scan 0.2.0.

Usage:
    wia_scan list_devices
    wia_scan --help

Options:
  -h --help                      Show this screen.
  --version                      Show version.
"""

from docopt import docopt
from .scan_functions import list_devices, get_device_manager, IndentPrinter


def main():
    arguments = docopt(__doc__, version='wia_scan 0.2.0')

    if arguments['list_devices']:
        device_manager = get_device_manager()
        list_devices(device_manager=device_manager,
                     print_function=IndentPrinter(indent=0))


if __name__ == '__main__':
    main()
