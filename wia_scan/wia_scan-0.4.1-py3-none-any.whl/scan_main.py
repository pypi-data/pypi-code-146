"""wia_scan 0.4.1.

Usage:
  wia_scan list_devices [-v]
  wia_scan single_side [-v]
  wia_scan many_flatbed [-v]
  wia_scan --help

Options:
  -h --help            Show this screen.
  --version            Show version.
  -v --verbose         Verbose output
"""

from docopt import docopt
from .scan_functions import list_devices, get_device_manager, IndentPrinter, \
    scan_single_side_main, scan_many_documents_flatbed


def main():
    arguments = docopt(__doc__, version='wia_scan 0.4.1')

    print_function = IndentPrinter(indent=0, print_function=print)
    verbose = arguments['--verbose']

    if arguments['list_devices']:
        device_manager = get_device_manager()
        list_devices(device_manager=device_manager,
                     print_function=print_function, verbose=verbose)
    elif arguments['single_side']:
        scan_single_side_main(print_function=print_function, verbose=verbose)
    elif arguments['many_flatbed']:
        scan_many_documents_flatbed(
            print_function=print_function, verbose=verbose)


if __name__ == '__main__':
    main()
