"""wia_scan 0.4.0.

Usage:
  wia_scan list_devices
  wia_scan single_side
  wia_scan many_flatbed
  wia_scan --help

Options:
  -h --help                      Show this screen.
  --version                      Show version.
"""

from docopt import docopt
from .scan_functions import list_devices, get_device_manager, IndentPrinter, \
    scan_single_side_main, scan_many_documents_flatbed


def main():
    arguments = docopt(__doc__, version='wia_scan 0.4.0')

    print_function = IndentPrinter(indent=0, print_function=print)

    if arguments['list_devices']:
        device_manager = get_device_manager()
        list_devices(device_manager=device_manager,
                     print_function=print_function)
    elif arguments['single_side']:
        scan_single_side_main(print_function=print_function)
    elif arguments['many_flatbed']:
        scan_many_documents_flatbed(print_function=print_function)


if __name__ == '__main__':
    main()
