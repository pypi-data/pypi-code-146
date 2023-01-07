#! /user/local/bin env

from getpass import getpass

std_radius_user = 'tarmstrong'
std_local_user = 'admin'
std_radius_pwd = 'Milcom.123'
std_local_pwd = 'VTgroup2013'

# std_radius_user = getpass("Enter Radius username: ")
# std_local_user = getpass("Enter local username: ")
# std_radius_pwd = getpass("Enter Radius password: ")
# std_local_pwd = getpass("Enter local password: ")

VAEITSW001 = {
    'device_type': 'ios',
    'device_name': 'VAEITSW001a',
    'useRadius': True,
    'hostname': '192.168.2.1',
    'username': std_radius_user,
    'password': std_radius_pwd,
    'optional_args': {'dest_file_system': 'flash:'},
}


VAEITSW002 = {
    'device_type': 'ios',
    'device_name': 'VAEITSW002a',
    'useRadius': True,
    'hostname': '192.168.2.2',
    'username': std_radius_user,
    'password': std_radius_pwd,
    'optional_args': {'dest_file_system': 'flash:'},
}


VAEITSW003 = {
    'device_type': 'ios',
    'device_name': 'VAEITSW003',
    'useRadius': True,
    'hostname': '192.168.2.3',
    'username': std_local_user,
    'password': std_local_pwd,
    'optional_args': {'dest_file_system': 'flash:'},
}

VAEITSW004 = {
    'device_type': 'ios',
    'device_name': 'VAEITSW004',
    'useRadius': True,
    'hostname': '192.168.2.4',
    'username': std_radius_user,
    'password': std_radius_pwd,
    'optional_args': {'dest_file_system': 'flash:'},
}

VAEITSW007 = {
    'device_type': 'ios',
    'device_name': 'VAEITSW007',
    'useRadius': True,
    'hostname': '192.168.2.7',
    'username': std_local_user,
    'password': std_local_pwd,
    'optional_args': {'dest_file_system': 'flash:'},
}

VTGROUP_SW101 = {
    'device_type': 'ios',
    'device_name': 'VTGROUP_SW101',
    'useRadius': True,
    'hostname': '192.168.2.101',
    'username': std_local_user,
    'password': std_local_pwd,
    'optional_args': {'dest_file_system': 'flash:'},
}

RRMCJSWY001 = {
    'device_type': 'junos',
    'device_name': 'RRMCJSWY001aabb',
    'useRadius': False,
    'hostname': '192.168.2.18',
    'username': std_local_user,
    'password': std_local_pwd,
    'optional_args': {},
}


device_list = [
        # VAEITSW001,
        # VAEITSW002,
        # VAEITSW003,
        # VAEITSW004,
        VAEITSW007,
        # VTGROUP_SW101,
        # RRMCJSWY001,
]
