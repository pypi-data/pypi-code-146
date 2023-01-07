#! /user/local/bin env

from getpass import getpass

std_radius_user = 'ICS_Admin'
std_local_user = 'ICS_Admin'
std_radius_pwd = 'Access4JPO'
std_local_pwd = 'Access4JPO'

# std_radius_user = getpass("Enter Radius username: ")
# std_local_user = getpass("Enter local username: ")
# std_radius_pwd = getpass("Enter Radius password: ")
# std_local_pwd = getpass("Enter local password: ")

CORE_2_4507R_E = {
    'device_type': 'ios',
    'device_name': 'CORE-2-4507R+E',
    'useRadius': False,
    'hostname': '172.20.3.3',
    'username': std_local_user,
    'password': std_local_pwd,
    'optional_args': {'dest_file_system': 'bootflash:'},
    # 'optional_args': {},
}


ICS_B1_3560_X = {
    'device_type': 'ios',
    'device_name': 'ICS-B1-3560-X',
    'useRadius': False,
    'hostname': '172.20.3.4',
    'username': std_local_user,
    'password': std_local_pwd,
    'optional_args': {'dest_file_system': 'flash:'},
}


ICS_B2_3560_X = {
    'device_type': 'ios',
    'device_name': 'ICS-B2-3560-X',
    'useRadius': False,
    'hostname': '172.20.3.5',
    'username': std_local_user,
    'password': std_local_pwd,
    'optional_args': {'dest_file_system': 'flash:'},
}


POE_B19_120_1_3560X_48 = {
    'device_type': 'ios',
    'device_name': 'POE_B19-120-1_3560X-48',
    'useRadius': False,
    'hostname': '172.20.3.15',
    'username': std_local_user,
    'password': std_local_pwd,
    'optional_args': {'dest_file_system': 'flash:'},
}


POE_B19_034_3_3560X_24 = {
    'device_type': 'ios',
    'device_name': 'POE_B19-034-3_3560X-24',
    'useRadius': False,
    'hostname': '172.20.3.17',
    'username': std_local_user,
    'password': std_local_pwd,
    'optional_args': {'dest_file_system': 'flash:'},
}


POE_B18_001_1_3560X_24 = {
    'device_type': 'ios',
    'device_name': 'PPOE_B18-001-3560X-24',
    'useRadius': False,
    'hostname': '172.20.3.16',
    'username': std_local_user,
    'password': std_local_pwd,
    'optional_args': {'dest_file_system': 'flash:'},
}

###use for testing
POE_B17_13_122_1_3560X_24 = {
    'device_type': 'ios',
    'device_name': 'POE-B17-13-122-1_3560-X-24',
    'useRadius': False,
    'hostname': '172.20.3.18',
    'username': std_local_user,
    'password': std_local_pwd,
    'optional_args': {'dest_file_system': 'flash:'},
}

POE_B18_002_1_2960X_24PS = {
    'device_type': 'ios',
    'device_name': 'PPOE_B18-002-2960X-24PS',
    'useRadius': False,
    'hostname': '172.20.3.19',
    'username': std_local_user,
    'password': std_local_pwd,
    'optional_args': {'dest_file_system': 'flash:'},
}



device_list = [
        CORE_2_4507R_E,
        ICS_B1_3560_X,
        ICS_B2_3560_X,
        POE_B19_120_1_3560X_48,
        POE_B19_034_3_3560X_24,
        POE_B18_001_1_3560X_24,
        POE_B18_002_1_2960X_24PS,
        POE_B17_13_122_1_3560X_24
]

