"""
wia_scan/scan_functions.py: an accumulation of helper functions
"""

import win32com.client

import keyboard

# https://learn.microsoft.com/en-us/previous-versions/windows/desktop/wiaaut/-wiaaut-consts-misc
WIA_ID_UNKNOWN = '{00000000-0000-0000-0000-000000000000}'

# https://learn.microsoft.com/en-us/previous-versions/windows/desktop/wiaaut/-wiaaut-consts-formatid
WIA_FORMAT_BMP = '{B96B3CAB-0728-11D3-9D7B-0000F81EF32E}'
WIA_FORMAT_PNG = '{B96B3CAF-0728-11D3-9D7B-0000F81EF32E}'
WIA_FORMAT_GIF = '{B96B3CB0-0728-11D3-9D7B-0000F81EF32E}'
WIA_FORMAT_JPEG = '{B96B3CAE-0728-11D3-9D7B-0000F81EF32E}'
WIA_FORMAT_TIFF = '{B96B3CB1-0728-11D3-9D7B-0000F81EF32E}'

# https://learn.microsoft.com/en-us/previous-versions/windows/desktop/wiaaut/-wiaaut-consts-commandid
WIA_COMMAND_SYNCHRONIZE = "{AF933CAC-ACAD-11D2-A093-00C04F72DC3C}"
WIA_COMMAND_TAKE_PICTURE = "{AF933CAC-ACAD-11D2-A093-00C04F72DC3C}"
WIA_COMMAND_DELETE_ALL_ITEMS = "{E208C170-ACAD-11D2-A093-00C04F72DC3C}"
WIA_COMMAND_CHANGE_DOCUMENT = "{04E725B0-ACAE-11D2-A093-00C04F72DC3C}"
WIA_COMMAND_UNLOAD_DOCUMENT = "{1F3B3D8E-ACAE-11D2-A093-00C04F72DC3C}"


WIA_EXTENSION_TO_FORMAT = {
    'bmp': WIA_FORMAT_BMP,
    'png': WIA_FORMAT_PNG,
    'gif': WIA_FORMAT_GIF,
    'jpeg': WIA_FORMAT_JPEG,
    'tiff': WIA_FORMAT_TIFF,
}


class IndentPrinter:
    """ A class to help with indentation of output """

    def __init__(self, indent, print_function):
        self.indent = indent
        self.print_function = print_function

    def __call__(self, *args, **kwargs):
        total_indent = self.indent + kwargs.get('indent', 0)

        args_as_string = " ".join([str(x) for x in args])
        output = (' ' * total_indent) + args_as_string
        self.print_function(output)


def print_device_properties(device, print_function):
    print_function('Device Commands: ', indent=0)
    for command in device.Commands:
        print_function(f'{command.Name}: {command.Description}', indent=1)

    print_function('Device properties: ', indent=0)
    for property_ in device.Properties:
        readonly = ''
        if property_.IsReadOnly:
            readonly = '[Readonly]'
        print_function(
            f'{property_.Name}: {property_.Value} {readonly}', indent=1)
        if property_.Name in ['Format', 'Preferred Format']:
            print_function(
                f'Format extension: {format_id_to_extension(property_.Value)}', indent=2)


def press_any_key_to_continue(print_function):
    print_function("Press any key to continue....")
    keyboard.read_key()


def print_object_debug(name, obj, print_function):
    print_function(name, ' ', type(obj))
    for property_ in dir(obj):
        print_function('obj.property_ ', property_, indent=1)
    print_function(obj)


def format_id_to_extension(wia_id):
    for name, value in WIA_EXTENSION_TO_FORMAT.items():
        if value == wia_id:
            return name
    return 'UNKOWN_WIA_FORMAT'


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
                print_function(
                    f'{property_.Name}: {property_.Value}', indent=2)


def ask_for_an_int(prompt_message, default, valid_range):
    while True:
        answer = input(f'{prompt_message} [Default: {default}]: ')
        if len(answer) == 0:
            answer = default
        try:
            value = int(answer)
            if value < valid_range[0] or value > valid_range[1]:
                print(
                    f'Answer outside of valid range, valid range is {valid_range}')
            else:
                return value
        except ValueError:
            print('Could not understand answer, please try again')


def prompt_choose_device(device_manager, print_function):
    if device_manager.DeviceInfos.Count == 0:
        raise ValueError(
            "devices must be available to choose, but none is available")

    print_function('Available devices', indent=0)
    device_ids = []
    for item_index in range(1, device_manager.DeviceInfos.Count + 1):
        device_info = device_manager.DeviceInfos(item_index)
        print_function(item_index, device_info, indent=1)
        for property_ in device_info.Properties:
            print_function(property_.Name, ' ', property_.Value, indent=2)
            if property_.Name == 'Unique Device ID':
                device_ids.append(property_.Value)
    assert len(device_ids) == device_manager.DeviceInfos.Count, \
        'Require finding unique device ids, did not find them'

    index = ask_for_an_int('Choose a device number',
                           default=1, valid_range=(1, len(device_ids)))

    return device_ids[index - 1]


def get_device_info_by_unique_id(device_manager, unique_id):
    for device_info_ in device_manager.DeviceInfos:
        for property_ in device_info_.Properties:
            if property_.Name == 'Unique Device ID' and property_.Value == unique_id:
                return device_info_
    return None


def connect_device(device_manager, device_identifier, print_function):
    print_function('Entered device identifier', device_identifier)
    device_info = get_device_info_by_unique_id(
        device_manager, unique_id=device_identifier)
    if device_info is None:
        raise ValueError(f'Could not find device with id {device_identifier}')

    print_function('Connecting ... ')
    device = device_info.Connect()
    print_function('Connected ')

    assert device.Items.Count <= 1
    if device.Items.Count == 1:  # has sub item, i have no idea why though
        print_function('getting subdevice')
        device = device.Items(1)
        print_object_debug('device ', device, print_function=print_function)
        print_device_properties(device, print_function=print_function)

    return device


def set_property(device, property_name, value):
    for property_ in device.Properties:
        if property_.Name == property_name:
            property_.Value = value


DEFAULT_SCAN_SETTINGS = {
    'brightness': 0,
    'contrast': 0,
    'dpi': 200,
    'mode': 'RGB'
}


def scan_page(device, settings, print_function):
    """
    Scans a single page and returns the WIA Image

    Parameters
    ===========

    """
    set_property(device, 'Brightness', settings['brightness'])
    set_property(device, 'Contrast', settings['contrast'])
    set_property(device, 'Horizontal Resolution', settings['dpi'])
    set_property(device, 'Vertical Resolution', settings['dpi'])
    if settings['mode'] == 'RGB':
        set_property(device, 'Data Type', 3)
    elif settings['mode'] == 'L':
        set_property(device, 'Data Type', 2)
    else:
        raise ValueError('unsupported mode')

    print_device_properties(device, print_function=print_function)

    print('available transfer formats')
    for format_ in device.Formats:
        print('format ', format_)

    # device.ExecuteCommand(WIA_COMMAND_TAKE_PICTURE) # this doesnt work for some wierd reason
    for command in device.Commands:
        if command.CommandID == WIA_COMMAND_TAKE_PICTURE:
            device.ExecuteCommand(WIA_COMMAND_TAKE_PICTURE)

    # Warning: can return a different format since item.Formats returns actually
    # supported formats for transfer
    image = device.Transfer(WIA_FORMAT_BMP)
    return image
