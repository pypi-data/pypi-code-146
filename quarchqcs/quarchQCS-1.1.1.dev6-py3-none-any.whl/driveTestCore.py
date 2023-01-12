#!/usr/bin/env python
"""
This file contains the core functions for the drive test suite.
Functions are placed here for the core setup functions called during the init stage of a test (or CSV parsed test set)


########### VERSION HISTORY ###########

03/01/2019 - Andy Norrie        - First Version

########### INSTRUCTIONS ###########

N/A

####################################
"""
from __future__ import print_function
from sys import platform

import logging
import ctypes
import os
import ssl
import sys
import time
import traceback
import socket
from socket import error as socket_error
from xml.etree import cElementTree
import pkg_resources

from quarchpy.device import quarchQPS, quarchDevice, quarchArray
from quarchpy.device.scanDevices import scanDevices
from quarchpy.connection_specific.connection_QPS import QpsInterface
from quarchpy.user_interface.user_interface import is_user_admin, progressBar, printText

from QuarchpyQCS.Drive_wrapper import DriveWrapper
from QuarchpyQCS.dtsComms import DTSCommms
from QuarchpyQCS.dtsGlobals import dtsGlobals
from QuarchpyQCS.hostInformation import HostInformation
from QuarchpyQCS.testLine import testLine
from QuarchpyQCS._version import __version__ as quarchQCS_version

myHostInfo = HostInformation()
comms = DTSCommms()


def printToBackend(text=""):
    printText(text=text, terminalWidth=80, fillLine=True)


def sendMsgToGUI(toSend, timeToWait=5):
    comms.sendMsgToGUI(toSend, timeToWait)


def is_tool(name):
    """Check whether `name` is on PATH."""

    from distutils.spawn import find_executable

    return find_executable(name) is not None


def update_progress_bars(completion_value, is_document_mode):
    if is_document_mode == "document":
        return
    comms.sendMsgToGUI(comms.create_request_status(completion_value))
    printProgressBar(completion_value, 100)


def printProgressBar(iteration, total):
    iteration = float(iteration)
    total = float(total)
    progressBar(iteration, total, fullWidth=80)


def executeAndCheckCommand(myDevice, command):
    # Run the command
    result = myDevice.sendCommand(command)

    # Log the command data
    comms.create_request_log(time.time(), "quarchCommand", "Quarch Command: " + command + " - Response: " + result,
                             os.path.basename(__file__) + " - " + sys._getframe().f_code.co_name,
                             {"debugLevel": 1, "textDetails": "Executing command on module"}, uId="")

    # Verify that the command executed as expected
    if result == "OK":
        return True
    else:
        comms.create_request_log(time.time(), "error", "Error executing Torridon command",
                                 os.path.basename(__file__) + " - " + sys._getframe().f_code.co_name,
                                 {"debugLevel": 2, "response_type": str(type(result)), "response": result,
                                  "command": command}, uId="")
        return False


'''
Adds a newly defined quarch module to use during the test and stores it as a resource to use later
connection="USB:QTL1743" or "REST:192.168.1.12<7>"
moduleName="myModule1" (unique string to identify the resource later)
'''


def specifyQuarchModule(moduleName, interFaceType="PY", powerOnDevice=True, return_val=False, module_type="all",
                        report_dict=[]):
    # allow use to find device, then connect to it
    connection = None

    if "PY" in interFaceType:
        connection = chooseQuarchModule(moduleName, module_type)
    elif "QPS" in interFaceType:
        connection = chooseQuarchModuleQPS(moduleName)

    return get_module_from_choice(connection, powerOnDevice, report_dict, return_val)


def get_module_from_choice(connection, report_dict, return_val, is_qps=False): # powerOnDevice, report_dict, return_val, is_qps=False):
    if connection is None:
        logging.warning("No item selected, test aborted. Waiting for new test start..\n")
        # printText("No item selected, test aborted. Waiting for new test start..\n")
        return 0
    # If this is an array controller sub module
    str_pos = connection.find('<')
    if str_pos != -1:

        # Get the array part
        array_connection = connection[0:str_pos]
        # Get the sub module nubmber
        array_position = connection[str_pos + 1:]
        array_position = array_position.strip(' >')

        # Create the array controller connection
        try:
            my_quarch_device = quarchDevice(array_connection)
        except ValueError as e:
            # If the connection to device failed, rescan for actual devices
            comms.send_stop_test(reason="Could not establish connection to root device of array. Test aborted")
            logging.warning("Could not establish connection to root device of array. Test aborted")
            # printText("Could not establish connection to root device. Test aborted")
            return 0

        # Promote connection to array type
        my_array = quarchArray(my_quarch_device)
        # Get access to the sub-device
        my_sub_device = my_array.getSubDevice(array_position)
        module_response = my_sub_device.sendCommand("*TST?")

        # Test the connection
        if module_response != "OK":
            comms.create_request_log(time.time(), "error", "Quarch module not ready",
                                     os.path.basename(__file__) + " - " + sys._getframe().f_code.co_name,
                                     {"textDetails": "Module responded: " + module_response})
        else:
            # Add the item to the test resources dictionary
            if return_val:
                return_val = my_sub_device

    elif is_qps:
        # Splitting string 'USB::QTL1999-01-001=5v' into connection and output mode
        # connection, output_mode_value = connection.split("=")

        # Creating QPS connection with device  --  Uses GUI TCP
        my_quarch_device = quarchDevice(connection, ConType="QPS:" + dtsGlobals.GUI_TCP_IP + ":9822")

        # Create the device connection, as a QPS connected device
        my_qps_device = quarchQPS(my_quarch_device)
        my_qps_device.openConnection()

        if return_val:
            return_val = my_qps_device

    else:
        # Create the device connection
        try:
            my_quarch_device = quarchDevice(connection)
        except ValueError as e:
            # If the connection to device failed, rescan for actual devices
            connection = None
            comms.send_stop_test(reason="Could not establish connection to specified device. Is device still available?")
            logging.warning("Error while connecting to specified device, test aborted")
            # printText("Error while connecting to specified device, test aborted")
            return 0

        # Test the connection
        module_response = my_quarch_device.sendCommand("*TST?")
        if module_response is None or module_response == "":
            comms.create_request_log(time.time(), "error", "Quarch module did not respond",
                                     os.path.basename(__file__) + " - " + sys._getframe().f_code.co_name)
            return 0
        elif module_response != "OK":
            comms.create_request_log(time.time(), "warning", "Quarch module did not pass self test",
                                     os.path.basename(__file__) + " - " + sys._getframe().f_code.co_name,
                                     {"textDetails": "Module responded: " + module_response})
            return 0

        if return_val:
            return_val = my_quarch_device

    report_dict["quarch_module"] = str(my_quarch_device.ConString).upper()
    report_dict["module_firmware"] = my_quarch_device.sendCommand("version")
    return return_val


def check_programs_status():
    # If false is returned, we timed out trying to open socket connection to QPS
    if not check_qps_open():
        comms.send_stop_test(reason="Failed to start an instance of Quarch Power Studio (QPS). Please start this manually on client machine.")
        return None

    qps_instance = QpsInterface(host=dtsGlobals.GUI_TCP_IP)

    # If false is returned, we timed out checking for Qis Status via QPS
    if not check_qis_open(qps_instance):
        comms.send_stop_test(reason="Failed to start an instance of Quarch Instrument Server (QIS). Please start this manually on Client machine.")
        return None

    # Small pause for QIS to start finding devices
    time.sleep(3)

    return qps_instance


def get_quarch_modules_qps():
    qps_instance = check_programs_status()

    # Display and choose module from found modules
    qps_device_list = qps_instance.getDeviceList()

    return qps_device_list


def chooseQuarchModuleQPS(moduleName, myQps=None):
    dtsGlobals.choiceResponse = None

    qps_instance = None

    if not myQps:
        qps_instance = check_programs_status()
        if qps_instance is None:
            return None
    else:
        # Re-use QPS instance if it's already passed
        qps_instance = myQps

    # Display and choose module from found modules
    qps_device_list = qps_instance.getDeviceList()

    formatted_qps_modules_dict = {}
    for quarch_module in qps_device_list:
        if "rest" in quarch_module:
            continue
        connection_without_interface = quarch_module[quarch_module.rindex(":") + 1:]
        formatted_qps_modules_dict[quarch_module.replace("::", ":")] = connection_without_interface

    comms.sendMsgToGUI(comms.create_request_gui(title="user selection", description="Choose a QPS Quarch Module",
                                                window_type="SelectionGrid", window_mode="qps",
                                                dict_of_modules=formatted_qps_modules_dict))

    while dtsGlobals.choiceResponse is None and dtsGlobals.continueTest is True:
        time.sleep(0.25)

    # order should be choiceResponse::xyz
    choice = str(dtsGlobals.choiceResponse)
    selection = choice.replace("\r\n", "").split("::", 2)
    if "rescan" not in selection:  # rescan is the only responce we dont want printed at the moment. If others are needed make a global list.
        logging.debug("Response from module selection was : " + choice)
        # printText("Response from module selection was : " + selection[1], fillLine=True, terminalWidth=80)

    if "choice-abort" in choice:
        return None
    elif "rescan" in choice:
        return chooseQuarchModuleQPS(moduleName, qps_instance)

    # Obtain output from the quarchModule selection
    selection[1] = selection[1].replace(":", "::")
    logging.debug("Selection1 is now " + selection[1])

    # Resetting the device prior to any commands being sent
    qps_instance.sendCmdVerbose("selection[1] conf:def:state")

    outMode = qps_instance.sendCmdVerbose(selection[1] + " conf:out:mode?")
    logging.debug("Out mode for selection was " + outMode)

    # Closing the connection to QPS
    qps_instance.client.close()

    selection[1] = selection[1].replace("::", ":")
    selection = selection[1]

    # if user does not select an item, we abort
    ret_val = selection.strip() + "=" + outMode
    return ret_val


def check_qps_open(timeout=5000):
    time_start = time.time()
    while True and (time.time() - time_start < timeout):
        try:
            send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            send_sock.connect((dtsGlobals.GUI_TCP_IP, 9822))  # no longer throws error
            send_sock.close()
            return True
        except socket.error:
            time.sleep(1)
    logging.error("Timeout trying to connect to QPS port")
    return False


def check_qis_open(qps_instance, timeout=5000):
    status = qps_instance.sendCmdVerbose("$qis status")
    time_start = time.time()
    while "Not Connected" in status:
        if time.time() - time_start > timeout:
            logging.error("Time out - Could create qis connection")
            return False
        status = qps_instance.sendCmdVerbose("$qis status")
        time.sleep(0.2)

    return True


def chooseQuarchModule(module_name, module_type=None, ip_address_lookup=None, scan_dictionary=None):
    dtsGlobals.choiceResponse = None

    # Reset the variable so it's not searched for unless specified during same run of program.
    ip_address_lookup = None

    comms.sendMsgToGUI(comms.create_request_gui(title="user selection", description="Choose a Quarch Module",
                                                window_type="SelectionGrid", window_mode="py",
                                                dict_of_modules=scan_dictionary))

    while dtsGlobals.choiceResponse is None and dtsGlobals.continueTest is True:
        time.sleep(0.25)

    choice = str(dtsGlobals.choiceResponse)
    selection = choice.split("::")
    # order should be choiceResponse::xyz
    selection = selection[1]
    selection = selection.replace(":", "::")

    # if user does not select an item, we abort
    if "choice-abort" in selection:
        return None
    elif "rescan" in selection:
        if "==" in selection:
            ip_address_lookup = selection[selection.index("==") + 2:]
        return chooseQuarchModule(module_name, ip_address_lookup)
    else:
        logging.debug("Response from module selection was : " + choice)
        return selection.strip()


def resetTestResources():
    # resetting test variable
    dtsGlobals.continueTest = True
    dtsGlobals.validVersion = True
    dtsGlobals.choiceResponse = None
    dtsGlobals.runUntilFirstFailure = False
    dtsGlobals.send_to_gui = True


def setRunUntilFirstTestFailure():
    dtsGlobals.runUntilFirstFailure = True




'''
Callback: Run when a test invokes TEST_GETDISKSTATUS (Check the status of the drive).  This can use lspci or
be expanded to use any form of internal test tool
'''


def DiskStatusCheck(driveId, expectedState, check_lanes=True, mapping_mode=None, poll=False):
    # Check to see if the pcieMappingMode resource string is set
    if not mapping_mode:
        mapping_mode = False

    drive_state = False

    if isinstance(driveId, DriveWrapper):
        drive_state = myHostInfo.is_wrapped_device_present(driveId)
    else:
        logging.error("Drive pass was not of type DriveWrapper - disk status check")

    if expectedState != drive_state:
        # print("drive was not in expected state")
        if not poll:
            print("\nLast system scan returned :\n " + myHostInfo.last_scan_return)
        return False
    else:
        # print("drive was in expected state")
        return True


'''
Tries to get the local/network IP address of the server
'''


def getLocalIpAddress(first=True):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
        if ip == "127.0.0.1" and first is True:
            s.close()
            getLocalIpAddress(first=False)

    except socket_error:
        ip = None
    finally:
        s.close()
    return ip


def check_compatibility():
    comms.sendMsgToGUIwithResponse(
        comms.create_request_function(
            "server_version", function_value="QuarchQCS:" + str(quarchQCS_version)))

    # First check is to see if QCS accepts the quarchpy version sent
    if not dtsGlobals.validVersion:
        logging.warning("QuarchpyQCS version too low for this QCS version. Please upgrade Quarchpy.")
        return False
    # Second check is to see if the QCS version is accepted by this quarchpy
    if not dtsGlobals.QCSVersionValid:
        logging.warning("QCS client version too low for this Quarchpy version. Please upgrade QCS.")
        return False

    logging.debug("Compatible QCS and quarchpy")
    return True


'''
Activates a remote server at the given port number.  This function will not return until the server connection is closed

This is intended for use with a remote client (generally running a compliance test script).  This server takes in XML format command requests and executes local
test functions based on this.
'''


class QuarchComplianceSuite:

    def __init__(self, port_number=9742, development=False):
        # WorkloadType.SAS_DRIVE_DET = myHostInfo.get_sas_drive_det_cmd()
        # WorkloadType.PCIE_DRIVE_DET = "LSPCI"
        self.conn = None
        self.sock = None
        self.tcp_port = port_number
        self.server_name = None
        self.tcp_ip = '{address}'.format(address="127.0.0.1" if getLocalIpAddress() is None else getLocalIpAddress())
        self.test = None
        self.running = True
        self.dev = development

    def attempt_restart(self, reason=None):
        if reason is None:
            logging.debug("Java connection closed, attempting to recover ")
            self.show_server_Status(action="Client disconnected", status="IDLE")
            # printText("Java connection closed, attempting to recover ")
        else:
            logging.warning(reason)
            # printText(reason)
        self.conn.close()
        self.sock.close()
        # time.sleep(1)
        resetTestResources()
        self.activate_remote_server()

    def bind_socket_tls(self):
        # Setup and open the socket for connection
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Making the socket allow connections from any connection available...?
        self.sock.bind(('', self.tcp_port))
        self.sock.listen(1)
        # self.tcp_ip = '{address}'.format(address="127.0.0.1" if getLocalIpAddress() is None else getLocalIpAddress())
        logging.debug("Server IP: " + str(self.tcp_ip))

    def activate_remote_server(self):

        buffer_size = 64000
        mdns_info = None
        conn = None

        try:
            self.bind_socket_tls()
            # self.setup_mdns_server()

            # Wait for a connection
            self.conn, addr = self.sock.accept()

            # changing cwd to start
            certdir = os.path.dirname(os.path.abspath(__file__))
            certdir = os.path.join(certdir, "certs")
            current_direc = os.getcwd()
            os.chdir(certdir)

            try:
                self.sock = ssl.wrap_socket(self.conn, server_side=True, ca_certs="client_cert.pem",
                                            certfile="server_cert.pem",
                                            keyfile="server_key.key", cert_reqs=ssl.CERT_REQUIRED,
                                            ssl_version=ssl.PROTOCOL_TLSv1_2,
                                            ciphers="AES128-SHA")

                comms.sock = self.sock

            except Exception as e:
                logging.warning("Exception during TLs connection")
                print(e)
                traceback.print_exc()
                return

            os.chdir(current_direc)
            logging.debug("----Remote Server connection opened from: " + str(addr))
            self.show_server_Status(action="Client connected: "+ str(addr), status="CONNECTED")

            # layout = :<'x.x.x.x',xx>
            item = str(addr).split('\'')
            dtsGlobals.GUI_TCP_IP = item[1]

            # Checking to see Quarchpy and QCS are valid together - Exit if not.
            if not check_compatibility():
                # This return will jump to finally block
                return

            self.running = True

            try:
                # Loop while the server is to be active
                while self.running:
                    # Get data from the connection
                    # data = self.conn.recv(buffer_size)
                    self.read_socket(buffer_size)

            except KeyboardInterrupt:
                logging.warning("---Remote server shutdown request, user CTRL-C received")

        except ConnectionResetError:
            self.attempt_restart()
        except Exception as ex:
            logging.warning(traceback.print_exc())
            logging.warning("Remote server process exited with an exception : " + str(ex))
        finally:
            logging.warning(traceback.print_exc())
            if self.conn is not None:
                self.conn.close()
            self.sock.close()
            printText("----Remote server shutdown complete")

    def read_socket(self, buffer_size):
        recv = self.sock.read(buffer_size)
        if not recv:
            pass
        # data = data.replace(str.encode("\r\n"), b"")
        data = bytes.decode(recv)
        required = ["</request>", "</response>"]
        while not any(ext in data.lower() for ext in required):
            recv = self.sock.read(buffer_size)
            data += recv.decode('utf-8', 'ignore')
        # print(data)
        self.commandParser(data)

    def commandParser(self, data):
        # print("Request received : " + str(data))

        if len(data) == 0:
            # 0 data length means socket was closed by java
            self.attempt_restart()
            return

        try:
            # parse command passed
            myobj = testLine()
            if "</request>" in data.lower():
                if data.count("</Request>") > 1:
                    data = data.strip().split("</Request>")
                    for response in data:
                        if not response:
                            pass
                        response = response[: response.lower().index("</request>") + len("</request>")]
                        xml_root = cElementTree.fromstring(response)
                        self.parse_request(xml_root)
                else:
                    data = data[: data.lower().index('</request>') + len("</request>")]
                    xml_root = cElementTree.fromstring(data)
                    self.parse_request(xml_root)
            else:
                # print(data)
                data = data[: data.index('</Response>') + len("</Response>")]
                xml_tree = cElementTree.fromstring(data.replace("\n", ""))
                if not comms.parse_response(xml_tree, data):
                    logging.warning("Unknown response")

        except (NameError, ValueError, AttributeError, ModuleNotFoundError) as err:
            logging.warning("Issue encountered on test, please contact quarch with the following trace")
            traceback.print_exc()
            comms.send_stop_test("Error encountered with test, please report this to Quarch")
            self.sock.write(comms.create_response("false"))
            self.show_server_Status(action="Test suite halted: ERROR", status="CONNECTED")
            return
        except (ConnectionRefusedError, ConnectionResetError) as err:
            traceback.print_exc()
            if isinstance(err, ConnectionRefusedError):
                logging.warning("Could not send response to Java, aborting : " + str(traceback.print_exc()))
            else:
                logging.debug("Connection Reset, restarting server : " + str(traceback.print_exc()))
            self.attempt_restart()

        except Exception as e:
            logging.warning(traceback.print_exc())
            logging.error(e)
            if self.conn is not None:
                self.conn.close()
            self.sock.close()
            logging.error("ERROR - Unexpected failure. ")
            raise

    def parse_request(self, xml_tree):

        required_response = False
        if not xml_tree.find('ResponseRequired') == "":
            # print(xml_tree.find('ResponseRequired').text)
            required_response = xml_tree.find('ResponseRequired').text

        if xml_tree.find('poll'):
            if required_response == "false":
                return
            else:
                if xml_tree.find("poll"):
                    sub_elem = xml_tree.find("poll")
                    if sub_elem.find("scan_devices").text == "true":
                        module_dictionary = scanDevices()

                        if is_tool("smartctl"):
                            drive_dictionary = myHostInfo.return_wrapped_drives()

                            comms.sendMsgToGUI(
                                comms.create_request_gui(
                                    title="user selection", description="N/A", window_type="SelectionGrid",
                                    window_mode="system_devices", dict_of_drives=drive_dictionary, dict_of_modules=module_dictionary))

                        return

        if xml_tree.find('function'):
            sub_elem = xml_tree.find('function')

            resetTestResources()

            dtsGlobals.qcs_dir = sub_elem.find('function_dir').text

            if sub_elem.find('function_call').text == "disconnect":
                # self.show_server_Status(action="Client disconnected", status="IDLE")
                self.attempt_restart()
                return

            dtsGlobals.qcs_dir = sub_elem.find('function_dir').text

            if sub_elem.find('function_call').text == "shutdown":
                self.show_server_Status(action="Shutdown Recieved", status="SHUTDOWN")
                self.sock.write(comms.create_response("true"))
                self.running = False
                return

            # self.sock.write(comms.create_response("true"))

            # For reporting back what type of test is ended
            # function_type = sub_elem.find('function_call').text


            if sub_elem.find('function_call').text == "init_test":
                self.compile_test(sub_elem)

                # from QuarchpyQCS.Python_Files.test_unh import HotPlugTest
                # self.test = HotPlugTest()
                # from QuarchpyQCS.Python_Files.test_short_bounce import ShortBounceDuringPlug
                # self.test = ShortBounceDuringPlug()
                # from QuarchpyQCS.Python_Files.test_full_range import Full_Range_HotPlugTest
                # self.test = Full_Range_HotPlugTest()
                # from QuarchpyQCS.Python_Files.test_pcie_lane_reduction import Lane_Reduction_PCIe
                # self.test = Lane_Reduction_PCIe()
                # from QuarchpyQCS.Python_Files.test_ss import SignalSweep
                # self.test = SignalSweep()
                # from QuarchpyQCS.Python_Files.power_vs_perf_free import PowerVsPerformance
                # self.test = PowerVsPerformance()
                # from QuarchpyQCS.Python_Files.test_power_margining_fio import PowerMarginingTest
                # self.test = PowerMarginingTest()
                # from QuarchpyQCS.Python_Files.test_report import testReport
                # self.test = testReport()
                
                if not self.test.comms:
                    self.test.comms = comms

                # Check if the test has all features
                self.test.check_prerequisites()

                if self.test.test_errors:
                    missing_imports = ":".join(self.test.test_errors)
                    self.test.comms.send_stop_test(reason=str(missing_imports))

                self.test.test_name = sub_elem.find('test_name').text
                self.test.test_number = sub_elem.find('test_number').text

                comms.send_finish_test()
                self.sock.write(comms.create_response("true"))

                if self.dev:
                    from tkinter.filedialog import askopenfilename
                    filename = askopenfilename()
                    print(filename)

            if sub_elem.find('function_call').text == "custom_variables":
                self.test.ask_for_user_vars()
                comms.send_finish_test()
                self.sock.write(comms.create_response("true"))

            if sub_elem.find('function_call').text == "gen_report":
                self.test.report["custom_variables"] = self.test.user_vars
                self.test.comms.sendMsgToGUI(
                    comms.create_request_gui(title="report generation", description="Test Report",
                                             window_type="SelectionGrid", window_mode="report",
                                             report_dict=self.test.report))
                comms.send_finish_test()
                self.sock.write(comms.create_response("true"))

            if sub_elem.find('function_call').text == "document_mode":
                self.test.start_test(document_mode=True)
                comms.send_finish_test()
                self.sock.write(comms.create_response("true"))

            if sub_elem.find('function_call').text == "start_test":
                # For report generation about current test.
                self.test.gather_initial_report_values()

                try:
                    self.test.seek_test_values()
                    if self.test.test_errors:
                        missing_imports = ":".join(self.test.test_errors)
                        self.test.comms.sendMsgToGUI(self.test.comms.send_stop_test(reason=missing_imports))
                    else:
                        self.show_server_Status(action="Test suite started : {0} - {1}".format(self.test.test_number,
                                                                                               self.test.test_name),
                                                status="RUNNING")
                        self.test.start_test()
                        if not dtsGlobals.continueTest:
                            self.show_server_Status(action="Test suite halted: USER_TERMINATE", status="CONNECTED")
                        else:
                            self.show_server_Status(action="Test suite halted: COMPLETE", status="CONNECTED")
                except Exception as e:
                    traceback.print_exc()
                    print(e)

                comms.send_finish_test()
                self.sock.write(comms.create_response("true"))
                # self.conn.sendall(comms.create_response("True"))

    def compile_test(self, sub_elem):
        test = compile(sub_elem.find('function_value').text, "", 'exec')
        # find class name
        test_name = str(sub_elem.find('function_value').text).split("class")
        test_name = test_name[1][:test_name[1].index("(")].strip()
        temp_dict = {}
        # compile to dict
        exec(test, temp_dict)
        # set class variable to compiled test
        temp_test = temp_dict[test_name]
        self.test = temp_test()

    def setup_mdns_server(self):

        # Import zero conf only if available
        try:
            import zeroconf
            from zeroconf import ServiceInfo, Zeroconf

            zeroConfAvail = True
        except ImportError:
            logging.warning("Please install zeroconf using 'pip install zeroconf'")
            zeroConfAvail = False

        # Activates mDNS registration for the server, so it can be located remotely
        if zeroConfAvail:
            try:
                # Get the sensible server name
                if self.server_name is None:
                    try:
                        self.server_name = socket.gethostname()
                    except socket_error:
                        self.server_name = "QCS-no-name-server"

                # Register the service
                mdns_desc = {'version': '1.0', 'server-name': self.server_name}


                mdns_info = ServiceInfo(type_="_http._tcp.local.",
                                       name="quarchCS._http._tcp.local.",
                                       addresses=[socket.inet_aton(self.tcp_ip)],
                                       # Need to check this arg on windows
                                       weight=0, priority=0,
                                       port=self.tcp_port,
                                       properties=mdns_desc)

                # LEGACY
                # mdns_info = ServiceInfo(type_="_http._tcp.local.",
                #                         name="quarchCS._http._tcp.local.",
                #                         port=self.tcp_port,
                #                         properties=mdns_desc)

                """
                self,
                 type_: str,
                 name: str,
                 port: Optional[int] = None,
                 weight: int = 0,
                 priority: int = 0,
                 properties: Union[bytes, dict] = b'',
                 server: Optional[str] = None,
                 host_ttl: int = _DNS_HOST_TTL,
                 other_ttl: int = _DNS_OTHER_TTL,
                 *,
                 addresses: Optional[List[bytes]] = None,
                 parsed_addresses: Optional[List[str]] = None) -> None
                 """

                zero_conf = Zeroconf()
                zero_conf.register_service(mdns_info)

                # Print registration results
                logging.debug("Server Name: " + self.server_name)

            except Exception as e:
                print(e)
                logging.warning("mDNS error, Service not registered")
        else:
            self.server_name = "QCS-no-name-server"
            zero_conf = None
        printText("Server Name : " + self.server_name)
        printText("Server IP : " + self.tcp_ip)
        printText("Server Status : IDLE ( {0} )".format(time.strftime("%d/%m/%Y, %H:%M:%S", time.gmtime())))

    def show_server_Status(self, status, action):
        printText("")
        printText("Server Action : " + action)
        printText("Server Status : {0} ( {1} ) ".format(status, time.strftime("%d/%m/%Y, %H:%M:%S", time.gmtime())))




def setUpLogging(log_level):
    levels = {
        "CRITICAL": 50,
        "ERROR": 40,
        "WARNING": 30,
        "INFO": 20,
        "DEBUG": 10,
    }
    logging.basicConfig(level=levels.get(str(log_level).upper()))



def main(argstring):
    disable_quickedit()

    import argparse

    # Handle expected command line arguments here using a flexible parsing system
    parser = argparse.ArgumentParser(description='QCS parameters')
    parser.add_argument('-l', '--logLevel',
                        help='Logging level sets the base level of what is output. Defaults to warning and above',
                        choices=["debug", "info", "warning"], default="warning", type=str.lower)
    parser.add_argument('-d', help='Allow user to select non-encrypted file for testing', default=False, type=bool)
    parser.add_argument('-i', help='Show internal test variables', default=False, type=bool)

    args = parser.parse_args(argstring)

    setUpLogging(args.logLevel)

    dtsGlobals.show_internal_variables = True if args.i else False

    _is_development = True if args.d else False

    printText("\n################################################################################")
    printText("                                   Welcome to                                 ")
    printText("                               Quarch Technology's                            ")
    printText("                             Quarch Compliance Suite                          ")
    printText("                            QuarchQCS Version : " + str(quarchQCS_version))
    printText("################################################################################\n")

    check_requirements()

    qcs = QuarchComplianceSuite(development=_is_development)
    qcs.setup_mdns_server()
    qcs.activate_remote_server()
    if qcs.sock:
        qcs.sock.close()
    # Attempting to stop QCS server from locking sockets on exit..
    sys.exit()

def check_requirements():
    if not is_user_admin():
        logging.warning("Quarch Compliance Suite must be run from an elevated command prompt.")
        logging.warning("Please restart with administrator privileges")
        sys.exit()
    if not is_tool("smartctl"):
        logging.warning("Could not find smartctl program via command line")
        logging.warning("Please install smartmontools at https://www.smartmontools.org/wiki/Download")
        sys.exit()
    if not platform == "win32":
        if not is_tool("lspci"):
            self.test_errors.append("Missing LSPCI from command line.")
            logging.warning("Please install lspci and restart this server")
            sys.exit()


def disable_quickedit():
    '''
    Enable or disable quick edit mode to prevent system hangs, sometimes when using remote desktop
    Param (Enabled)
    enabled = 1(default), enable quick edit mode in python console
    enabled = 0, disable quick edit mode in python console
    '''
    # -10 is input handle => STD_INPUT_HANDLE (DWORD) -10 | https://docs.microsoft.com/en-us/windows/console/getstdhandle
    # default = (0x4|0x80|0x20|0x2|0x10|0x1|0x40|0x200)
    # 0x40 is quick edit, #0x20 is insert mode
    # 0x8 is disabled by default
    # https://docs.microsoft.com/en-us/windows/console/setconsolemode
    if platform == "win32":
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4 | 0x80 | 0x20 | 0x2 | 0x10 | 0x1 | 0x00 | 0x100))
        print("Console Quick Edit Disabled")


if __name__ == "__main__":
    main(sys.argv[1:])
