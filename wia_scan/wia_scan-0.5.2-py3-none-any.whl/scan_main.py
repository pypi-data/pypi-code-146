"""wia_scan 0.5.2.

Usage:
  wia_scan list_devices [-v]
  wia_scan single [--file=<output_file>] [--dpi=<dpi>] [--brightness=<brightness>] [--contrast=<contrast>] [--mode=<mode>] [-v] [--uid=<uid>] [-q]
  wia_scan many [--out=<output_folder>] [-v]
  wia_scan --help

Options:
  -h --help                    Show this screen.
  --version                    Show version.
  -v --verbose                 Verbose output
  -q --quiet                   Quiet=no output
  --dpi=<dpi>                  Dots per inch; the higher this setting the higher the output resolution
  --brightness=<brightness>    Brightness setting for the scanner, goes from -1000 to 1000
  --contrast=<contrast>        Contrast setting for the scanner, goes from -1000 to 1000
  --mode=<mode>                RGB for colored, L for grayscale
  --file=<output_file>         Image output file
  --out=<output_folder>        Scanned images output folder
"""

import sys

from docopt import docopt
from .scan_functions import list_devices, get_device_manager, IndentPrinter, \
    scan_single_side_main, scan_many_documents_flatbed, DEFAULT_SCAN_PROFILE


def main():
    arguments = docopt(__doc__, version='wia_scan 0.5.2')

    print_function = IndentPrinter(indent=0, print_function=print)
    verbose = arguments['--verbose']
    quiet = arguments['--quiet']
    device_uid = arguments['--uid']

    if arguments['list_devices']:
        device_manager = get_device_manager()
        list_devices(device_manager=device_manager,
                     print_function=print_function, verbose=verbose)
    elif arguments['single']:
        if quiet and device_uid is None:
            print('Invalid input: uid has to be provided when quiet is used')
            sys.exit(-1)
        scan_profile = DEFAULT_SCAN_PROFILE
        if arguments['--brightness']:
            scan_profile['brightness'] = arguments['--brightness']
        if arguments['--contrast']:
            scan_profile['contrast'] = arguments['--contrast']
        if arguments['--dpi']:
            scan_profile['dpi'] = arguments['--dpi']
        if arguments['--mode']:
            scan_profile['mode'] = arguments['--mode']

        scan_single_side_main(scan_profile=scan_profile, print_function=print_function, verbose=verbose,
                              quiet=quiet, device_uid=device_uid, output_file=arguments['--file'])
    elif arguments['many']:
        scan_many_documents_flatbed(
            print_function=print_function, verbose=verbose, output_folder=arguments['--out'])


if __name__ == '__main__':
    main()
