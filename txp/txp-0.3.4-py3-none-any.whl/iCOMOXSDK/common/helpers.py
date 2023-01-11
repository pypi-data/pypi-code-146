import struct
import datetime
import os
import sys
import ipaddress


def u16s_to_str(arr, seperator, prefix=""):
    s = ""
    if len(arr) > 0:
        if 1 == (len(arr) % 2):
            arr += b"\x00"
        u16s = struct.unpack("<{:d}H".format(len(arr) / 2))
        for i in range(0, (len(arr) / 2) - 2):
            s += prefix + "{:04X}".format(u16s[i]) + seperator
        s += prefix + "{:04X}".format(u16s[-1])  # add the last element of u16s
    return s


def u8s_to_str(arr, separator, prefix=""):
    s = ""
    if len(arr) > 0:
        for i in range(0, len(arr) - 1):
            s += prefix + "{:02X}".format(arr[i]) + separator
        s += prefix + "{:02X}".format(arr[-1])  # add the last element of arr
    return s


def string_without(str, chars_to_remove):
    return str.translate({ord(c): None for c in chars_to_remove})


def bytearrayToString(bytes):
    index = bytes.find(b"\xFF")
    if index >= 0:
        bytes = bytes[:index]

    index = bytes.find(b"\x00")
    if index >= 0:
        bytes = bytes[:index]

    try:
        result = str(bytes, "utf8")
    except:
        result = ""
    finally:
        pass
    return result


def stringToIpAddress(ipaddress_str):
    try:
        ipaddress_obj = ipaddress.ip_address(ipaddress_str)
    except:
        ipaddress_obj = None
    finally:
        pass
    return ipaddress_obj


def OUT(outStr):
    s = str(datetime.datetime.now()) + " " + outStr
    print(s)


def resource_path(relative_path):
    try:
        # base_path = sys._MEIPASS
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)