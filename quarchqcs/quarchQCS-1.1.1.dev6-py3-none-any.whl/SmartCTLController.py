'''
Implements basic control over SmartCTL utilities, so that we can identify and check the
status of all devices on the host system
'''

import subprocess
import logging
import time
import os
import re
import sys
import ctypes
from sys import platform
#from abc import ABC, abstractmethod
import abc
ABC = abc.ABCMeta('ABC', (object,), {})

from QuarchpyQCS.Drive_wrapper import DriveWrapper
from QuarchpyQCS.sasFuncs import WindowsSAS

class abstractSmartCTL(ABC):

    def __init__(self):
        self.is_windows = True if platform == "win32" else False

    @abc.abstractmethod
    def get_device_list(self):
        pass

    @abc.abstractmethod
    def get_device_verbose(self, deviceInfo, devicesToScan):
        pass

    @abc.abstractmethod
    def sort_list(self, err, out):
        pass

    def is_admin_mode(self):

        if platform == "win32":
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False
        else:
            self.is_windows = False
            if os.getuid() == 0:
                return True

        return False

class UniversalSmartCtl( abstractSmartCTL ):
    def __init__(self):
        super(UniversalSmartCtl, self).__init__()
        self.proc_err = None
        self.last_scan_return = None

    def get_device_list(self, verbose=False):

        self.proc_err = None

        """
        Gets list of devices from smartctl.

        :param verbose: Boolean
                        If verbose is True, look into every device individually with the command
                            "smartctl -a /dev/<path>"

                        default output :
                            /dev/sda : /dev/sda -d ata # /dev/sda, ATA device
                            /dev/sdb : /dev/sdb -d ata # /dev/sdb, ATA device
                            /dev/sdc : /dev/sdc -d nvme # /dev/sdc, NVMe device
                            /dev/nvme0 : /dev/nvme0 -d nvme # /dev/nvme0, NVMe device

                        Verbose output :
                        0 : { /dev/sda : { dict of information } }

        :return: dicts of devices.
        """

        command = ["smartctl", "--scan"]

        out, err = self.run_device_verbose_command(command)

        # Adding error to be reported later.
        if err:
            self.proc_err = err
            logging.warning("Smartctl proc err : " + err)

        self.last_scan_return = bytes.decode(out)

        if verbose:
            retValues = self.sort_list_verbose(err, out)
        else:
            retValues = self.sort_list(err, out)

        return retValues

    def sort_list(self, err, out):
        value = bytes.decode(out)
        devices = value.split("\n")
        device_wrappers = {}
        for info in devices:
            dev_info = info.split(" ")
            device_wrappers[dev_info[0]] = info

        return device_wrappers

    def sort_list_verbose(self, err, out):
        value = bytes.decode(out)
        devices = value.split("\n")
        device_wrappers = {}
        for info in devices:
            dev_info = info.split(" ")
            # /dev/sda -d ata # /dev/sda, ATA device
            device_wrappers[dev_info[0]] = self.get_device_verbose(dev_info[0], dev_info[len(dev_info) - 2])

        return device_wrappers


    def run_device_verbose_command(self, command):

        # Stopping the need for smartmontools installation on Windows
        if self.is_windows:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            smartctl_path = os.path.join(dir_path, "smartmontools", "bin", "smartctl.exe")
            # replace "smartctl" with "{path}\smartctl.exe" for distributed version in windows
            command[0] = smartctl_path

        print(command)
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        out, err = proc.communicate()

        return out, err

    def get_device_verbose(self, dev_path, drive_type):

        if dev_path == "":
            return {}

        command = ["smartctl", "-i", dev_path]

        out, err = self.run_device_verbose_command(command)

        if not bytes.decode(err) == "":
            self.proc_err = err
            logging.warning("Smartctl -i proc err : " + err)
        if not "=== START OF INFORMATION SECTION ===" in bytes.decode(out):
            return {}

        device_dict = {}

        device_dict["drive_type"] = drive_type

        lines = bytes(out).decode().split("\n")  # bytes.decode(out).split("\r")
        for line in lines:
            if ":" in line:
                key_value = line.split(":")
                if len(key_value) > 2:
                    key_value[1] += key_value[2]
                device_dict[key_value[0].strip().lower()] = key_value[1].strip()

        return device_dict


    def wrap_smartctl_devices(self):
        logging.debug("Retrieving smart devices")
        devices = self.get_device_list(verbose=True)

        # Dev path : /dev/sda  -  /dev/nvme0  e.t.c
        """

        Model Family:     Samsung based SSDs
        Device Model:     SAMSUNG SSD PM851 mSATA 256GB
        Serial Number:    S1EVNSAFC80717
        LU WWN Device Id: 5 002538 844584d30
        Firmware Version: EXT4AD0Q
        User Capacity:    256,060,514,304 bytes [256 GB]
        Sector Size:      512 bytes logical/physical
        Rotation Rate:    Solid State Device
        Device is:        In smartctl database [for details use: -P show]
        ATA Version is:   ACS-2, ATA8-ACS T13/1699-D revision 4c
        SATA Version is:  SATA 3.1, 6.0 Gb/s (current: 6.0 Gb/s)
        Local Time is:    Sun Jan 10 04:49:30 2021 GMTST
        SMART support is: Available - device has SMART capability.
        SMART support is: Enabled
        """

        if len(devices) == 1:
            logging.debug("No Smart devices discovered")
            return None

        wrapped_drives = []

        for device, device_info in devices.items():
            if not device_info:
                continue

            drive_wrap = DriveWrapper()

            drive_wrap.drive_path = device
            drive_wrap.all_info = device_info

            drive_wrap.drive_type = device_info["drive_type"]

            if "nvme" in device:
                # '/dev/nvme0'
                device_split = drive_wrap.drive_path.rsplit('/', 1)
                # 'nvme0'
                if len(str(device_split[1])) == 5:
                    drive_wrap.drive_path += "n1"

            for value_key in device_info.keys():
                if "model" in value_key.lower():
                    drive_wrap.description = device_info[value_key]
                    drive_wrap.identifier_str = device_info[value_key]
                    continue
                if "capacity" in value_key.lower():
                    drive_wrap.storage_capacity = device_info[value_key]
                    continue
                if "sata version is" in value_key.lower():
                    if "current" in device_info["sata version is"]:
                        link_speed = device_info["sata version is"].split("current")
                        drive_wrap.link_speed = link_speed[1].replace(")", "")
                    else:
                        link_speed = device_info["sata version is"].split(",")
                        drive_wrap.link_speed = link_speed[1].strip()
                    continue
                if "serial number" in value_key.lower():
                    drive_wrap.serial_number = device_info[value_key]
                    continue
                if "firmware version" in value_key.lower():
                    drive_wrap.firmware_version = device_info[value_key]
                    continue

            if platform == "win32":
                # parse wmic for device and wrap here > needs a \\.\physicaldrivex
                drive_wrap.FIO_path = self.return_physical_dev_from_serial_number(drive_wrap.serial_number)
            else:
                drive_wrap.FIO_path = drive_wrap.drive_path

            drive_wrap.system_cmd = "SmartCtl"

            wrapped_drives.append(drive_wrap)

            """
            All devices should in form:
            dev/path : { dict of device info } 
            """

        """
        drive = DriveWrapper(identifier=sas_device["Model"], drive_type="Unknown",
                     description="{0} : {1} {2}".format(sas_device["vendor"],
                                                        sas_device["Model"], sas_device["Rev"]),
                     drive_path=sas_device["drive_path"], all_info=sas_device)
        """

        return wrapped_drives


    def return_physical_dev_from_serial_number(self, serial_number):
        """
        Windows only.
        Returns a device's physical drive string if WMIC has drive with identical
        serial number as the parameter passed

        :return: String : \\PHYSICALDRIVEX
                 None   : If not found
        """

        x = WindowsSAS()
        wrapped_wmic_devices = x.wrap_sas_devices()

        for device in wrapped_wmic_devices:
            if serial_number in device.serial_number:
                return device.FIO_path

        return None


#
# x = UniversalSmartCtl()
# # dicts = x.get_device_list(verbose=True)
# x.wrap_smartctl_devices()