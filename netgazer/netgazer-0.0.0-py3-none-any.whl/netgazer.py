#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
[options.entry_points] section in setup.cfg:

    console_scripts =
         fibonacci = netgazer.skeleton:run

Besides console scripts, the header (i.e. until logger...) of this file can
also be used as template for Python modules.


netgazer specific:
console_scripts =
    netgazer = netgazer.netgazer:main

Then run `python setup.py install` which will install the command `netgazer`
inside your current environment.
"""
from __future__ import print_function, unicode_literals
import argparse
import sys
import logging
import logging.handlers

import click
from napalm import get_network_driver
# from devices_ctil import device_list
from pprint import pprint
import json
import yaml
import inspect
import socket
from datetime import datetime
import re
from getpass import getpass

import pdb
# debug only - set the location of the trace set point with the command below
# pdb.set_trace()

# getting error message when trying to import __version__ from netgazer
# from netgazer import __version__

__author__ = "Tim Armstrong"
__copyright__ = "Tim Armstrong"
__license__ = "mit"

# added __version__ hear due to error in import above
__version__ = "0.0.1"


# Create a custom logger
logger = logging.getLogger("netgazer")
# logger = logging.getLogger(__name__)
# logger = logging.getLogger()
# https://stackoverflow.com/questions/4150148/logging-hierarchy-vs-root-logger


def setup_logging(logStreamLevel, logFileLevel):
    """Setup basic logging"""

    # use 'logger.info("Starting NetGazer Automation in INFO Mode...")' to log events in script

    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    # logpath = "./"
    logFilePath = "./netgazer.log"
    

    # Note:  setLevel for root logger must be lower or equal to lowest level 
    # you want any of the handelers, i.e. if file_handeler level is debug, 
    # then root logger level must be Debug also.  
    # initialize the root logger.  

    formatter = logging.Formatter('%(asctime)s | %(name)s |  %(levelname)s: %(message)s')
    logger.setLevel(logging.DEBUG)

    # setup the stream handler for console logging
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logStreamLevel)
    stream_handler.setFormatter(formatter)

    #  setup file handeler 
    file_handler = logging.handlers.TimedRotatingFileHandler(filename = logFilePath, when = 'midnight', backupCount = 30)
    file_handler.setLevel(logFileLevel)
    file_handler.setFormatter(formatter)

    # attach the stream and file handelers to the root logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    if logFileLevel == logging.INFO:
        logFileMode = "INFO"
    elif logFileLevel == logging.DEBUG:
        logFileMode = "DEBUG"
    elif logFileLevel == logging.WARNING:
        logFileMode = "WARNNING"

    if logStreamLevel == logging.INFO:
        logStreamMode = "INFO"
    elif logStreamLevel == logging.DEBUG:
        logStreamMode = "DEBUG"
    elif logStreamLevel == logging.WARNING:
        logStreamMode = "WARNNING"

    logger.info(f"Starting NetGazer Automation in File Logging Mode:  {logFileMode}")
    logger.info(f"Starting NetGazer Automation in Console Logging Mode:  {logStreamMode}")

    # # DEBUG ONLY
    # logger.info("Started");
    # try:
    #     x = 14
    #     y = 0
    #     z = x / y
    # except Exception as ex:
    #     logger.error("Operation failed.")
    #     logger.debug("Encountered {0} when trying to perform calculation.".format(ex))
    # logger.info("Ended");
    logger.error("error")
    logger.warning("warning")
    logger.info("info")
    logger.debug("debug")




@click.group()
# @click.option('--device-path', default=None,
#               help="Use a given path and device_list file.")
@click.option('-dp', '--device-path', default='./devices.yaml',
              help="Provide JSON/YAML device file.  Default is ./devices.yaml")
@click.option('-v', '--verbose', default=False, is_flag=True,
              help="set Console logging level to INFO")
@click.option('-vv', '--very-verbose', default=False, is_flag=True,
              help="set Console logging level to DEBUG")
@click.option('-fvv', '--file-very-verbose', default=False, is_flag=True,
              help="set Log File logging level to DEBUG")
# version option does not work, as it is looking for a command to execute
# created as a command below.
# @click.option('-version', 'version', default=False, is_flag=True,
#               help="Provides the NetGaZer Version")
def cli(device_path,verbose, very_verbose, file_very_verbose):
    """

    NetGaZer automates the process of pulling data from network environments

    """
    # pdb.set_trace()
    print(f"fvv is {file_very_verbose}")
    print(f"verbose is {verbose}")    
    # global variables go here
    global device_list, loglevel
    
    # Determine the File Logging Level to pass to Setup_Logging Function
    if file_very_verbose:
        logFileLevel = logging.DEBUG
    else:
        logFileLevel = logging.INFO


    # Determine The Console Logging Level to pass to Setup_Logging Function
    # Note that logFileLevel is changed to DEBUG is -vv flag is provided.
    if verbose:
        logStreamLevel = logging.INFO
        click.echo("NetGaZer is now in Verbose Mode")
        setup_logging(logStreamLevel, logFileLevel)
    elif very_verbose:
        logStreamLevel = logging.DEBUG
        logFileLevel = logging.DEBUG
        click.echo("NetGaZer is now in Very Verbose Mode")
        setup_logging(logStreamLevel, logFileLevel)
    else:
        logStreamLevel = logging.WARNING
        setup_logging(logStreamLevel, logFileLevel)

    print()


    # Determine the type of device file that has been provided (YAML or JSON)
    print(f"Device Path is set to the following: {device_path}")

    file_type = device_path.split('.')[1]

    if file_type == 'json':
        with open(device_path) as f:
            device_list = json.load(f)
    elif file_type == 'yaml' or 'yml':    # 'yml' or
        with open(device_path, 'r') as f:
            device_list = yaml.safe_load(f)
    else:
        print("""\nThe file type extention provided is not a supported format!
Please check extension and file format.  Must be .json, .yml, or .yaml""")
        sys.exit(0)


    get_std_creds(device_list)

    # debug only
    # pprint(device_list)
    # print(device_list[0]["device_type"])

    # setup_logging(loglevel)


def get_std_creds(device_list):
    # std_radius_user = 'tarmstrong'
    # std_local_user = 'admin'
    # std_radius_pwd = 'Milcom.123'
    # std_local_pwd = 'VTgroup2013'

    # debug only
    # pdb.set_trace()

    std_radius_user = getpass("Enter Radius username: ")
    std_radius_pwd = getpass("Enter Radius password: ")
    for a_device in device_list:
        a_device["username"] = std_radius_user
        a_device["password"] = std_radius_pwd


def get_device_props(a_device):
    """
    Gets device properties from the provided Device Data and
    creates associated variables that are passed to several functions
    """

    device_props = {}
    device_type = a_device["device_type"]
    device_name = a_device["device_name"]
    hostname = a_device["hostname"]
    device_props = {
        "device_type": device_type,
        "device_name": device_name,
        "hostname": hostname,
    }
    return device_props


def device_setup(a_device):
    """

    Performs NAPALM device driver setup and opens connections to devices

    """

    useRadius = a_device.pop('useRadius')
    device_type = a_device.pop("device_type")
    device_name = a_device.pop('device_name')
    driver = get_network_driver(device_type)
    device = driver(**a_device)
    try:
        device.open()
    except Exception as e: 
        print(e)

    return device  # testing w/ device_type return


def print_device_header(device_props):
    """

    Prints standard device header or opening

    """

    print()
    print()
    print(f">>>Opening Connection to {device_props['device_name']}...")
    print("#" * 85)
    print("IP Address:  {} ".format(device_props["hostname"]))
    print("Hostname:    {} ".format(device_props["device_name"]))
    print("Platform:    {}".format(device_props["device_type"]))
    print("#" * 85)
    return


def print_task_header(func_select):
    """

    Prints standard task header or opening

    """

    print("\n")
    print("+" * 60)
    print(f"++++  BEGIN TASK DATA GETTER:  {func_select}  ++++")
    print("+" * 60)
    print()
    return


def print_task_closing(func_select):
    """

    Prints standard task closing

    """

    print()
    print("-" * 60)
    print(f"----  END TASK DATA GETTER:  {func_select}  ----")
    print("-" * 60)
    return


def print_device_closing(device_props):
    """

    Prints standard device closing

    """
    print("\n")
    print(f">>>Closing Connection to {device_props['device_name']}...")
    print("#" * 60)
    print(
        f"####  END OF DEVICE OUTPUT:  \
        {device_props['device_name']}  ####  "
    )
    print()
    print()
    print()
    return


@cli.command("version")
def version():
    """

    Provides NetGaZer Version

    """

    print(f"Version is {__version__}!")
    sys.exit(0)


def lldp_parse_logic(device, device_props):
    """

    Runs specific NAPALM function call and performs
    custom parsing and processing of the NAPALM returned
    dictionary, and then creates output to STD_OUT

    """

    lldp_info = device.get_lldp_neighbors()
    lldp_list = []
    for key in lldp_info.keys():
        neighbor = lldp_info[key][0]["hostname"]
        port = lldp_info[key][0]["port"]

        """
        this creates a dict and appends to a list and
        allows for sorting later vice printing each line as it comes
        """
        d_entry = {}
        d_entry = {"neighbor": neighbor, "port": port}
        lldp_list.append(dict(d_entry))

    # allows a sort in a list of dicts based on key in dict ('intf')
    lldp_list = sorted(lldp_list, key=lambda k: k["port"])

    # printing Header
    print("Local Port            Neighbor")
    print("__________            ________")
    # printing loop
    for entry in lldp_list:
        port = entry["port"]
        neighbor = entry["neighbor"]
        # print(entry)
        print("{: <22}{: <30}".format(port, neighbor))

    return


@cli.command("get-lldp")
def get_lldp():
    """

    Get LLDP-Neighbors for  devices in device list.

    """

    func_select = inspect.currentframe().f_code.co_name.upper()

    logger.info("NetGaZer started the %s function", func_select)

    for a_device in device_list:
        device_props = {}
        device_props = get_device_props(a_device)
        device = device_setup(a_device)
        print_device_header(device_props)
        print_task_header(func_select)
        lldp_parse_logic(device, device_props)
        print_task_closing(func_select)
        print_device_closing(device_props)

    logger.info("NetGaZer completed the %s function", func_select)
    print()


def intf_counters_parse_logic(device, device_props):
    """

    Runs specific NAPALM function call and performs
    custom parsing and processing of the NAPALM returned
    dictionary, and then creates output to STD_OUT


    """

    intf_counters_info = device.get_interfaces_counters()
    intf_counters_list = []

    # DEBUG ONLY
    # pprint(intf_counters_info)

    for key in intf_counters_info.keys():
        # print(key)
        intf = key

        rx_bcst_pks = intf_counters_info[key]['rx_broadcast_packets']
        rx_discards = intf_counters_info[key]['rx_discards']
        rx_errors = intf_counters_info[key]['rx_errors']
        rx_multi_pks = intf_counters_info[key]['rx_multicast_packets']
        rx_uni_pks = intf_counters_info[key]['rx_unicast_packets']
        rx_octets = intf_counters_info[key]['rx_octets']
        tx_bcst_pks = intf_counters_info[key]['tx_broadcast_packets']
        tx_discards = intf_counters_info[key]['tx_discards']
        tx_errors = intf_counters_info[key]['tx_errors']
        tx_multi_pks = intf_counters_info[key]['tx_multicast_packets']
        tx_uni_pks = intf_counters_info[key]['tx_unicast_packets']
        tx_octets = intf_counters_info[key]['tx_octets']

        # this allows for sorting later vice printing each line as it comes
        d_entry = {
            "intf": intf,
            "rx_bcst_pks": rx_bcst_pks,
            "rx_discards": rx_discards,
            "rx_errors": rx_errors,
            "rx_multi_pks": rx_multi_pks,
            "rx_uni_pks": rx_uni_pks,
            "rx_octets": rx_octets,
            "tx_bcst_pks": tx_bcst_pks,
            "tx_discards": tx_discards,
            "tx_errors": tx_errors,
            "tx_multi_pks": tx_multi_pks,
            "tx_uni_pks": tx_uni_pks,
            "tx_octets": tx_octets
        }

        intf_counters_list.append(dict(d_entry))

    # allows a sort in a list of dicts based on key in dict
    intf_counters_list = sorted(intf_counters_list, key=lambda k: k["intf"])
    # pprint(intf_counters_list)

    print("Interface (TX/RX)        Disgards         Errors          Broadcast             Multicast                    Unicast")
    print("_________________        ________         ______          _________             _________                    ________")

    # printing loop
    for entry in intf_counters_list:
        intf = entry["intf"]
        rx_bcst_pks = entry["rx_bcst_pks"]
        rx_discards = entry["rx_discards"]
        rx_errors = entry["rx_errors"]
        rx_multi_pks = entry["rx_multi_pks"]
        rx_uni_pks = entry["rx_uni_pks"]
        # rx_octets = entry["rx_octets"]
        tx_discards = entry["tx_discards"]
        tx_bcst_pks = entry["tx_bcst_pks"]
        tx_discards = entry["tx_discards"]
        tx_errors = entry["tx_errors"]
        tx_multi_pks = entry["tx_multi_pks"]
        tx_uni_pks = entry["tx_uni_pks"]
        # tx_octets = entry["tx_octets"]

        # print(entry)
        print("{: <22}{: >6}/{: <6}{: >8}/{: <8}{: >8}/{: <8}{: >8}/{: <8}{: >16}/{: <16}".format(intf,
            tx_discards, rx_discards, rx_errors, rx_errors, tx_bcst_pks, rx_bcst_pks, tx_multi_pks, rx_multi_pks, tx_uni_pks, rx_uni_pks))

    return


@cli.command("get-intf-counters")
def get_intf_counters():
    """

    Get details on interface counters for devices in device list.

    """

    func_select = inspect.currentframe().f_code.co_name.upper()

    logger.info("NetGaZer started the %s function", func_select)

    for a_device in device_list:
        device_props = {}
        device_props = get_device_props(a_device)
        device = device_setup(a_device)
        print_device_header(device_props)
        print_task_header(func_select)
        intf_counters_parse_logic(device, device_props)
        print_task_closing(func_select)
        print_device_closing(device_props)

    logger.info("NetGaZer completed the %s function", func_select)
    print()


def config_parse_logic(device, device_props):
    """

    Runs specific NAPALM function call and performs
    custom parsing and processing of the NAPALM returned
    dictionary, and then creates output to STD_OUT

    """

    print()
    print(">>>> Writing Running-Config...")
    print()
    # configs = device.get_config(retrieve='running')
    configs = device.get_config(retrieve="all")

    running = configs["running"].rstrip("\r\n")
    startup = configs["startup"].rstrip("\r\n")

    file_prefix = datetime.now().strftime("%Y%m%d-%H%M%S")

    # Debug only
    # pprint(configs)

    """
    Using regular expression (re) logic to find the first occurance of 'version
    which is the first line of actual configuration.
    The result includes it, 'version' and everything after as result.
    Using multi-line flag to search multiple lines and select remaining lines.
    re result is held in group(1)
    Then we are striping off new line characters in the output
    """
    if device_props["device_type"] == "ios":
        running = re.search("(?=version)(?s)(.*$)", running).group(1).rstrip("\r\n")
        startup = re.search("(?=version)(?s)(.*$)", startup).group(1).rstrip("\r\n")
        with open(
            "./configs/startup-{}-{}.txt".format(
                file_prefix, device_props["device_name"]
            ),
            "w",
        ) as f:
            print(startup, file=f)
        with open(
            "./configs/running-{}-{}.txt".format(
                file_prefix, device_props["device_name"]
            ),
            "w",
        ) as f:
            print(running, file=f)
    elif device_props["device_type"] == "junos":
        # juniper does not support startup config option - no result in output
        running = re.search("(?=version)(?s)(.*$)", running).group(1).rstrip("\r\n")
        with open(
            "./configs/running-{}-{}.txt".format(
                file_prefix, device_props["device_name"]
            ),
            "w",
        ) as f:
            print(running, file=f)

    return


@cli.command("get-config")
def get_config():
    """

    Get running configuration for devices in device list.

    """

    func_select = inspect.currentframe().f_code.co_name.upper()

    logger.info("NetGaZer started the %s function", func_select)

    for a_device in device_list:
        device_props = {}
        device_props = get_device_props(a_device)
        device = device_setup(a_device)
        print_device_header(device_props)
        print_task_header(func_select)
        config_parse_logic(device, device_props)
        print_task_closing(func_select)
        print_device_closing(device_props)

    logger.info("NetGaZer completed the %s function", func_select)
    print()


def mac_parse_logic(device, device_props):
    """

    Runs specific NAPALM function call and performs
    custom parsing and processing of the NAPALM returned
    dictionary, and then creates output to STD_OUT

    """

    mac_info = device.get_mac_address_table()

    mac_list = []

    # data collection loop
    for mac in mac_info:
        intf = mac["interface"]
        mac_addr = mac["mac"]
        if mac["static"]:
            mac_type = "STATIC"
        else:
            mac_type = "DYNAMIC"
        vlan = mac["vlan"]

        # this allows for sorting later vice printing each line as it comes
        d_entry = {}
        d_entry = {"intf": intf,
                   "mac": mac_addr,
                   "vlan": vlan, "mac_type": mac_type}
        mac_list.append(dict(d_entry))

    # allows a sort in a list of dicts based on key in dict ('intf')
    mac_list = sorted(mac_list, key=lambda k: k["intf"])

    
    print("MAC                   Interface   VLAN  TYPE")
    print("___                   _________   ____  ____")
    # printing loop
    for entry in mac_list:
        if intf and len(intf) >= 2:
            intf = entry["intf"]
        else:
            intf = "Hardware"
        mac_addr = entry["mac"]
        vlan = entry["vlan"]
        mac_type = entry["mac_type"]
        # print(entry)
        print("{: <18}{: >12}{: >6}{: >10}".format(
            mac_addr, intf, vlan, mac_type))
    return


@cli.command("get-mac-table")
def get_mac_table():
    """Get get-mac-table for all devices in device list."""

    func_select = inspect.currentframe().f_code.co_name.upper()

    logger.info("NetGaZer started the %s function", func_select)

    for a_device in device_list:
        device_props = {}
        device_props = get_device_props(a_device)
        device = device_setup(a_device)
        print_device_header(device_props)
        print_task_header(func_select)
        mac_parse_logic(device, device_props)
        print_task_closing(func_select)
        print_device_closing(device_props)

    logger.info("NetGaZer completed the %s function", func_select)
    print()


def arp_parse_logic(device, device_props):
    """

    Runs specific NAPALM function call and performs
    custom parsing and processing of the NAPALM returned
    dictionary, and then creates output to STD_OUT

    """

    arp_info = device.get_arp_table()
    # pprint(arp_info)

    arp_list = []

    # data collection loop
    for arp in arp_info:
        d_entry = {}
        intf = arp["interface"]
        ip = arp["ip"]
        mac_addr = arp["mac"]

        # this allows for sorting later vice printing each line as it comes
        d_entry = {"ip": ip, "mac": mac_addr, "intf": intf}
        arp_list.append(dict(d_entry))

    # allows a sort in a list of dicts based on key in dict ('ip')
    arp_list = sorted(arp_list, key=lambda item: socket.inet_aton(item["ip"]))

    
    print("IP Address      MAC Address           Interface")
    print("__________      ___________           _________")

    # printing loop
    for entry in arp_list:
        intf = entry["intf"]
        mac_addr = entry["mac"]
        ip = entry["ip"]
        # print(entry)
        print("{: <16}{: <22}{: <16}".format(ip, mac_addr, intf))

    return


@cli.command("get-arp-table")
def get_arp_table():
    """Get get-arp-table for all devices in device list."""

    func_select = inspect.currentframe().f_code.co_name.upper()

    logger.info("NetGaZer started the %s function", func_select)

    for a_device in device_list:
        device_props = {}
        device_props = get_device_props(a_device)
        device = device_setup(a_device)
        print_device_header(device_props)
        print_task_header(func_select)
        arp_parse_logic(device, device_props)
        print_task_closing(func_select)
        print_device_closing(device_props)

    logger.info("NetGaZer completed the %s function", func_select)
    print()


def optics_parse_logic(device, device_props):
    """

    Runs specific NAPALM function call and performs
    custom parsing and processing of the NAPALM returned
    dictionary, and then creates output to STD_OUT

    """

    optics_info = device.get_optics()

    # DEBUG ONLY
    # pprint(optics_info)
    # print(optics_info.keys())

    optics_list = []

    for key in optics_info.keys():
        # print(key)
        intf = key
        input_pwr = optics_info[key]["physical_channels"]["channel"][0]["state"]["input_power"]["instant"]
        output_pwr = optics_info[key]["physical_channels"]["channel"][0]["state"]["input_power"]["instant"]

        # this allows for sorting later vice printing each line as it comes
        d_entry = {
            "interface": intf,
            "input_power": input_pwr,
            "output_power": output_pwr,
        }
        optics_list.append(dict(d_entry))

    # allows a sort in a list of dicts based on key in dict
    optics_list = sorted(optics_list, key=lambda k: k["interface"])
    
    print("Interface                Input PWR (dB)           Output PWR (dB)")
    print("_________                ______________           _______________")

    # printing loop
    for entry in optics_list:
        intf = entry["interface"]
        input_pwr = entry["input_power"]
        output_pwr = entry["output_power"]
        # print(entry)
        print("{: <25}{: <25}{: <25}".format(intf, input_pwr, output_pwr))

    return


@cli.command("get-optics")
def get_optics():
    """Get get-optics for all devices in device list."""

    func_select = inspect.currentframe().f_code.co_name.upper()

    logger.info("NetGaZer started the %s function", func_select)

    for a_device in device_list:
        device_props = {}
        device_props = get_device_props(a_device)
        device = device_setup(a_device)
        print_device_header(device_props)
        print_task_header(func_select)
        optics_parse_logic(device, device_props)
        print_task_closing(func_select)
        print_device_closing(device_props)

    logger.info("NetGaZer completed the %s function", func_select)
    print()


def facts_parse_logic(device, device_props):
    """

    Runs specific NAPALM function call and performs
    custom parsing and processing of the NAPALM returned
    dictionary, and then creates output to STD_OUT

    """

    facts_info = device.get_facts()

    print("Model:         {model}".format(**facts_info))
    print("Serial Number: {serial_number}".format(**facts_info))
    print("OS Version:    {os_version}".format(**facts_info))

    return


@cli.command("get-facts")
def get_facts():
    """Get Facts for devices in device list."""
    func_select = inspect.currentframe().f_code.co_name.upper()
    logger.info("NetGaZer started the %s function", func_select)

    for a_device in device_list:
        device_props = {}
        device_props = get_device_props(a_device)
        device = device_setup(a_device)
        print_device_header(device_props)
        print_task_header(func_select)
        facts_parse_logic(device, device_props)
        print_task_closing(func_select)
        print_device_closing(device_props)
    logger.info("NetGaZer completed the %s function", func_select)

    print()


def check_up_up(intf_data):
    if intf_data["is_enabled"] and intf_data["is_up"]:
        return True
    return False


def up_intf_parse_logic(device, device_props):
    """

    Runs specific NAPALM function call and performs
    custom parsing and processing of the NAPALM returned
    dictionary, and then creates output to STD_OUT

    """

    intf_info = device.get_interfaces()

    intf_list = []

    for intf_name, intf_data in intf_info.items():
        if check_up_up(intf_data):
            intf_list.append(intf_name)

    # Sort by nam
    intf_list.sort()

    for intf in intf_list:
        print(intf)

    return


@cli.command("get-up-intf")
def get_up_intf():
    """Get Up INTFs for devices in device list."""

    func_select = inspect.currentframe().f_code.co_name.upper()

    logger.info("NetGaZer started the %s function", func_select)

    for a_device in device_list:
        device_props = {}
        device_props = get_device_props(a_device)
        device = device_setup(a_device)
        print_device_header(device_props)
        print_task_header(func_select)
        up_intf_parse_logic(device, device_props)
        print_task_closing(func_select)
        print_device_closing(device_props)

    logger.info("NetGaZer completed the %s function", func_select)
    print()


def traceroute_parse_logic(device, device_props, destination):
    """

    Runs specific NAPALM function call and performs
    custom parsing and processing of the NAPALM returned
    dictionary, and then creates output to STD_OUT

    """

    troute_info = device.traceroute(destination)
    print(troute_info)
    return


# returning empty dict... something is wrong...
@cli.command("traceroute")
@click.argument("destination", default="google.com")
def traceroute(destination, source="", ttl=255, timeout=2, vrf=""):

    """Return traceroute details for a provided destination"""

    func_select = inspect.currentframe().f_code.co_name.upper()

    logger.info("NetGaZer started the %s function", func_select)

    for a_device in device_list:
        device_props = {}
        device_props = get_device_props(a_device)
        device = device_setup(a_device)
        print_device_header(device_props)
        print_task_header(func_select)
        traceroute_parse_logic(device, device_props, destination)
        print_task_closing(func_select)
        print_device_closing(device_props)

    logger.info("NetGaZer completed the %s function", func_select)
    print()


def env_parse_logic(device, device_props):
    """

    Runs specific NAPALM function call and performs
    custom parsing and processing of the NAPALM returned
    dictionary, and then creates output to STD_OUT

    """

    try:
        env_info = device.get_environment()
    except UnboundLocalError:
        print("Opps!  There is no data available for this device!!!")
        return

    # DEBUG ONLY
    # pprint(env_info)

    if device_props["device_type"] == "junos":
        cpu = env_info["cpu"]["0"]["%usage"]
        temp = env_info["temperature"]["FPC 0 CPU"]["temperature"]
        temp_alarm = env_info["temperature"]["FPC 0 CPU"]["is_alert"]
        fan_status = env_info["fans"]["FPC 0 Fan 0"]["status"]

    else:  # device_type == ios
        cpu = env_info["cpu"][0]["%usage"]
        fan_status = env_info["fans"]["invalid"]["status"]

        temp_key = "system"
        if temp_key in env_info["temperature"]:
            temp = env_info["temperature"]["system"]["temperature"]
            temp_alarm = env_info["temperature"]["system"]["is_alert"]
        else:
            temp = temp_alarm = "Not Available"

    used_ram = env_info["memory"]["used_ram"]
    avail_ram = env_info["memory"]["available_ram"]

    if fan_status:
        fan_status = "OK"
    else:
        fan_status = "FAIL"

    if temp_alarm is True:
        temp_alarm = "ACTIVE"
    elif temp_alarm is False:
        temp_alarm = "NOT ACTIVE"

    print(f"          CPU Usage (%):  {cpu: <10}")
    print(f"           Used RAM (B):  {used_ram: <10}")
    print(f"      Available RAM (B):  {avail_ram: <10}")
    print(f"      Temperature Alarm:  {temp_alarm: <10}")
    print(f"Current Temperature (C):  {temp: <10}")
    print(f"             Fan Status:  {fan_status: <10}")

    return


@cli.command("get-env")
def get_env():

    """
    Record and return traceroute information to a destination provided
    Providing results of show env all, show processes cpu,
    show processes memory
    """

    """
       ### sample result - env_info = device.get_environment() ###
       {
       'cpu': {0: {'%usage': 31.0}},
       'memory': {'used_ram': 64505660, 'available_ram': 447050548},
       'temperature': {'system': {'is_alert': False, 'is_critical': False, 'temperature': 41.0}},
       'power': {'invalid': {'status': True, 'output': -1.0, 'capacity': -1.0}},
       'fans': {'invalid': {'status': True}}
       }
    """

    func_select = inspect.currentframe().f_code.co_name.upper()

    logger.info("NetGaZer started the %s function", func_select)

    for a_device in device_list:
        device_props = {}
        device_props = get_device_props(a_device)
        device = device_setup(a_device)
        print_device_header(device_props)
        print_task_header(func_select)
        env_parse_logic(device, device_props)
        print_task_closing(func_select)
        print_device_closing(device_props)

    logger.info("NetGaZer completed the %s function", func_select)
    print()


@cli.command("get-all")
def get_all():

    """

    Use all getters to collect Information for devices in device list.
    Collects all getter data for each device and then moves on to the next.

    Calls all individual parse functions which run specific NAPALM function calls.
    Performs custom parsing and processing of the NAPALM returned
    dictionary, and then creates output to STD_OUT.

    """

    func_select = inspect.currentframe().f_code.co_name.upper()

    logger.info("NetGaZer started the %s function", func_select)

    for a_device in device_list:
        device_props = {}
        device_props = get_device_props(a_device)
        device = device_setup(a_device)
        print_device_header(device_props)

        # create list of function dicts for execution in loop below
        # did not include '(device, device_props)', as that actually
        # calls the function.
        # see loop below for how to call the function
        task_list = [
            {"task": facts_parse_logic, "task_str": "GET FACTS"},
            {"task": env_parse_logic, "task_str": "GET ENVIRONMENT"},
            {"task": lldp_parse_logic, "task_str": "GET LLDP NEIGHBORS"},
            {"task": optics_parse_logic, "task_str": "GET OPTIC POWER LEVELS"},
            {"task": arp_parse_logic, "task_str": "GET ARP TABLE"},
            {"task": mac_parse_logic, "task_str": "GET MAC ADDRESS TABLE"},
            {"task": up_intf_parse_logic, "task_str": "GET UP/UP INTERFACES"},
            {"task": config_parse_logic, "task_str": "GET CONFIGURATION"},
            # {'task': traceroute_parse_logic, 'task_str': 'PERFORM TRACEROUTE'},
        ]

        for task in task_list:
            func_select = task["task_str"]
            print_task_header(func_select)

            # run task in list adding '(device, device_props)',
            # making it callable
            task["task"](device, device_props)
            # HOW get this to work with tasks that require additional args????
            # - i.e traceroute 'destination'

            print_task_closing(func_select)

        print_device_closing(device_props)

    logger.info("NetGaZer completed the %s function", func_select)
    print()


def main():
    """Main entry point allowing external calls"""
    print()
    print(">>>> Starting NetGaZer...")
    cli()
    # logger.info("NetGaZer Script Execution Complete.")


# def run():
#     """Entry point for console_scripts
#     """
#     main(sys.argv[1:])


if __name__ == "__main__":
    main()
