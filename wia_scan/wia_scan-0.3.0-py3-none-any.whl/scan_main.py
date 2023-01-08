"""wia_scan 0.3.0.

Usage:
  wia_scan list_devices
  wia_scan single_page
  wia_scan --help

Options:
  -h --help                      Show this screen.
  --version                      Show version.
"""

from docopt import docopt
from .scan_functions import list_devices, get_device_manager, IndentPrinter, prompt_choose_device, \
    scan_page, DEFAULT_SCAN_SETTINGS, connect_device

from datetime import datetime

def main():
    arguments = docopt(__doc__, version='wia_scan 0.3.0')

    print_function = IndentPrinter(indent=0, print_function=print)

    if arguments['list_devices']:
        device_manager = get_device_manager()
        list_devices(device_manager=device_manager,
                     print_function=print_function)
    elif arguments['single_page']:
        device_manager = get_device_manager()
        device_identifier = prompt_choose_device(
            device_manager=device_manager, print_function=print_function)
        device = connect_device(device_manager=device_manager,
                                device_identifier=device_identifier, print_function=print_function)
        wia_image = scan_page(device=device, settings=DEFAULT_SCAN_SETTINGS,
                              print_function=print_function)
        
        now = datetime.now()
        date_string = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f'scan_{date_string}.png'
        
        wia_image.SaveFile(filename)


if __name__ == '__main__':
    main()
