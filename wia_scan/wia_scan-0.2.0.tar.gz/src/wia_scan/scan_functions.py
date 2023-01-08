"""
wia_scan/scan_functions.py: an accumulation of helper functions
"""

import win32com.client


class IndentPrinter:
    """ A class to help with indentation of output """

    def __init__(self, indent):
        self.indent = indent

    def __call__(self, *args, **kwargs):
        total_indent = self.indent + kwargs.get('indent', 0)

        args_as_string = " ".join([str(x) for x in args])
        output = (' ' * total_indent) + args_as_string
        print(output)


def get_device_manager():
    """ Returns the wia device manager """
    device_manager = win32com.client.Dispatch("WIA.DeviceManager")
    return device_manager


def list_devices(device_manager, print_function):
    """ Prints the available devices to print_function """

    if device_manager.DeviceInfos.Count == 0:
        print_function('No available devices found', indent=0)
    else:
        print_function('Available devices', indent=0)
        for item_index in range(1, device_manager.DeviceInfos.Count + 1):
            device = device_manager.DeviceInfos(item_index)
            print_function(f'Device {item_index}', indent=1)
            for property_ in device.Properties:
                print_function(f'{property_.Name}: {property_.Value}', indent=2)
