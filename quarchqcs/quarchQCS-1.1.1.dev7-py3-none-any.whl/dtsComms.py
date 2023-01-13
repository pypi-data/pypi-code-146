import platform
import time
import logging
import socket
import threading
from datetime import datetime
import traceback
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

import xml.etree.ElementTree as cElementTree

from QuarchpyQCS.Drive_wrapper import DriveWrapper
from QuarchpyQCS.testLine import testLine
from QuarchpyQCS.dtsGlobals import dtsGlobals


class DTSCommms:

    def __init__(self):
        # declaring variables used in sending messages at different sections of class
        self.versionNumber = "1.02"
        self.request_tag = "Request"
        self.response_tag = "Response"
        self.request_id_counter = 0

        self.sock = None

        self.time_since_last_send = None
        self.response = None

        self.comms_semaphore = threading.Semaphore()

    def comms_send(self, toSend, timeToWait=5):
        if dtsGlobals.send_to_gui:
            #print(toSend)
            self.sendMsgToGUI(toSend, timeToWait)
        else:
            print(toSend)

    """
    Function for any item being sent to GUI 
    Default is to wait 3 seconds, but can be set for longer / infinite
    """

    def sendMsgToGUIwithResponse(self, to_send, timeToWait=5):
        if not to_send:
            logging.warning("Passed a None item to send ")
            return


        # sending message
        self.send_item_to_java(to_send)

        # basically infinite wait
        if timeToWait is None:
            timeToWait = 999999

        self.response = None

        self.getReturnPacket(wait_time=timeToWait)

        # print(self.response)

        return self.response

    def sendMsgToGUI(self, to_send, timeToWait=5):

        if not to_send:
            logging.warning("Passed a None item to send ")
            return

        # printText("Item Sent across : " + toSend)
        # to_send = str.encode(to_send)

        self.send_item_to_java(to_send)

        self.getReturnPacket()


    def send_item_to_java(self, to_send):

        self.comms_semaphore.acquire()

        if self.time_since_last_send:
            time_dif = time.time() - self.time_since_last_send

        # print(to_send)

        if len(to_send) > 8000:
            n = 8000
            items_to_send = [to_send[i:i + n] for i in range(0, len(to_send), n)]
            for split_msg in items_to_send:
                # split_msg = str.encode(str(len(split_msg))) + b">" + split_msg
                self.sock.write(split_msg + b"\n")
        else:
            # sending message
            # s.sendall(str.encode(str(len(to_send))) + b">" + to_send + b"\n")
            self.sock.write(to_send + b"\n")

        self.time_since_last_send = time.time()

        self.comms_semaphore.release()

    """
    Starts a subprocess to attempt to receive a return packet from java
    if timeout of 3 seconds is exceeded, break
    """

    def processTimeoutAndResult(self, timeToWait, message_sent=""):

        process_object = threading.Thread(target=self.getReturnPacket(message_sent))
        process_object.start()
        # timeout of 5 seconds
        start = time.time()

        while time.time() - start <= (timeToWait*1000):
            print(time.time() - start)
            if process_object.is_alive():
                time.sleep(.1)  # Just to avoid hogging the CPU
            else:
                # All the processes are done, break now.
                break
        else:
            # We only enter this if we didn't 'break' above.
            logging.error("timed out whilst getting response")
            process_object.terminate()
            process_object.join()



    """
    reads data from socket passed
    """

    def getReturnPacket(self, message_sent="", wait_time=5):

        buffer_size = 4096
        data = ""
        have_response = False
        expected_responses = ["<Response>","</Response>"]

        start = time.time()

        while time.time() - start <= (wait_time):

            # if not received start and end of expected
            if not have_response:
                temp_data = self.sock.read(buffer_size)
                if not temp_data:
                    continue
                data += temp_data.decode("utf-8")
                found = True
                for r_string in expected_responses:
                    if not r_string in data:
                        found = False
                        if data:
                            logging.debug("current response = " + str(data))
                if found:
                    have_response = True

            else:
                # print(data)
                try:
                    data = data[data.index("<Response>"):]
                    if data.count("</Response>") > 1:
                        data = data.split("</Response>")
                        for response in data:
                            response = response[: response.index('</Response>') + len("</Response>")]
                            xml_tree = cElementTree.fromstring(response)
                            if not self.parse_response(xml_tree, response):
                                logging.warning("Unknown response")
                    else:
                        data = data[: data.index('</Response>') + len("</Response>")]
                        xml_tree = cElementTree.fromstring(data.replace("\n",""))
                        if not self.parse_response(xml_tree, data):
                            logging.warning("Unknown response")
                except cElementTree.ParseError as err:
                    logging.error("Error parsing Java response")
                except Exception as i:
                    traceback.print_exc()
                    logging.warning("Unknown exception caught reading response : " + str(i))
                    logging.debug("Recv buffer : " + str(data))
                    logging.debug("Sent cmd : " + str(message_sent))

                break

        return True

    def create_response(self, function_complete=False, function_type=None):
        response = testLine()
        response.function_complete = function_complete
        root_tag = Element(self.response_tag)
        response_function_complete_tag = SubElement(root_tag, 'function_complete')
        response_function_complete_tag.text = str(response.function_complete)
        if function_type:
            response_function_type_tag = SubElement(root_tag, 'function_type')
            response_function_type_tag.text = str(function_type)

        return tostring(root_tag)

    def create_request_root(self, root_tag, request_type, response_required=True):
        request_type_tag = SubElement(root_tag, 'RequestType')
        request_type_tag.text = str(request_type)

        request_id_tag = SubElement(root_tag, 'RequestID')
        self.request_id_counter += 1
        request_id_tag.text = str(self.request_id_counter)

        response_required_tag = SubElement(root_tag, 'ResponseRequired')
        response_required_tag.text = str(response_required)

    def create_request_poll(self, poll_type=None):

        root_tag = Element(self.request_tag)

        self.create_request_root(root_tag, request_type="Poll", response_required=False)

        poll_child = SubElement(root_tag, 'poll')

        if poll_type:
            child_tag = SubElement(poll_child, 'poll_type')
            child_tag.text = str(poll_type)

        return tostring(root_tag)

    def create_request_report(self, group="user group", text=None, table=[], table_name="User Table", image=None):

        root_tag = Element(self.request_tag)

        self.create_request_root(root_tag, request_type="report_function", response_required=False)

        report_child = SubElement(root_tag, 'report_function')

        child = SubElement(report_child, 'group')
        child.text = str(group)

        function_type = SubElement(report_child, 'function_type')


        if image:
            function_type.text = str("image")
            # TODO : Implement a way to send image
            # child = SubElement(function_child, 'function_value')
            # child.text = str(iamge)
            if text:
                pass
            pass

        elif table:
            function_type.text = str("TABLE")

            if not isinstance(table, list):
                logging.warning("Table not of type list")

            child = SubElement(report_child, 'table_name')
            child.text = table_name

            child = SubElement(report_child, 'list_table2')
            for list_element in table:
                if not isinstance(list_element, list):
                    logging.warning("Inner list not of type list")
                    break
                child2 = SubElement(child, 'inner_list')
                for inner_list_element in list_element:
                    child3 = SubElement(child2, 'strings')
                    child3.text = str(inner_list_element)

        elif text:
            function_type.text = str("text")
            child = SubElement(report_child, 'text')
            child.text = str(function_value)


        # print(tostring(root_tag))
        return tostring(root_tag)

    def create_chart(self, type, yaxis_name, xaxis_name, series_names, dataset_labels, dataset_data, group="user group"):
        """

        :param type:                ENUM (String)   : Type of chart to create
        :param yaxis_name:          String          : Name of yaxis
        :param xaxis_name:          String          :
        :param series_names:        List<Str>       : Names of the series in data
        :param dataset_labels:      List<Str>       : Dataset names
        :param dataset_data:        List<List<str>> : 2d array of data to show on graph
        :return:
        """
        root_tag = Element(self.request_tag)

        self.create_request_root(root_tag, request_type="report_function", response_required=False)

        report_child = SubElement(root_tag, 'report_function')

        child = SubElement(report_child, 'group')
        child.text = str(group)

        function_type = SubElement(report_child, 'function_type')
        function_type.text = "CHART"

        child = SubElement(report_child, 'type')
        child.text = str(type)
        child = SubElement(report_child, 'yaxis_name')
        child.text = str(yaxis_name)
        child = SubElement(report_child, 'xaxis_name')
        child.text = str(xaxis_name)
        for item in series_names:
            child = SubElement(report_child, 'series_names')
            child.text = str(item)
        for item in dataset_labels:
            child = SubElement(report_child, 'dataset_labels')
            child.text = str(item)

        # For future developers - List of list<string> needs to be done like this
        # Re-used the list format from tables
        child = SubElement(report_child, 'list_table2')
        for list_element in dataset_data:
            if not isinstance(list_element, list):
                logging.warning("Inner list not of type list")
                break
            child2 = SubElement(child, 'inner_list')
            for inner_list_element in list_element:
                child3 = SubElement(child2, 'strings')
                child3.text = str(inner_list_element)
        # child = SubElement(report_child, 'dataset_data')
        # child.text = str(dataset_data)


        print(tostring(root_tag))
        return tostring(root_tag)

    def create_request_function(self, function_call, function_value=None, requires_response=True):

        root_tag = Element(self.request_tag)

        self.create_request_root(root_tag, request_type="Function", response_required=requires_response)

        function_child = SubElement(root_tag, 'function')

        child = SubElement(function_child, 'function_call')
        child.text = str(function_call)

        # Additional info, Like a directory or version number
        if function_value:
            child = SubElement(function_child, 'function_value')
            child.text = str(function_value)

        return tostring(root_tag)

    def create_request_gui(self, title, description, window_type, window_mode="PY", dict_of_modules=None,
                           dict_of_drives=None, report_dict=None):

        root_tag = Element(self.request_tag)

        self.create_request_root(root_tag, request_type="GUI")

        gui_tag = SubElement(root_tag, 'gui')

        title_tag = SubElement(gui_tag, 'title')
        title_tag.text = str(title)

        description_tag = SubElement(gui_tag, 'description')
        description_tag.text = str(description)

        window_type_tag = SubElement(gui_tag, 'windowType')
        window_type_tag.text = str(window_type)

        if window_mode:
            window_mode_tag = SubElement(gui_tag, 'windowMode')
            window_mode_tag.text = str(window_mode)

        if dict_of_modules:
            for conn_string, qtl_num in dict_of_modules.items():
                self.add_xml_quarch_module(conn_string, qtl_num, gui_tag)

        if dict_of_drives:
            for device in dict_of_drives:
                self.add_xml_drive(device, gui_tag)

        if report_dict:
            self.add_report_item(report_dict, gui_tag)

        return tostring(root_tag)

    def create_request_log(self, logTime, messageType, messageText, messageSource, messageData=None, test_result=None,
                           uId="", group=None, sub_group=None, check_point_id=None):

        root_tag = Element(self.request_tag)

        self.create_request_root(root_tag, request_type="log", response_required=False)

        self.notifyTestLogEventXml(root_tag, uId, logTime, messageType, messageText, messageSource, test_result,
                                   messageData, group, sub_group, check_point_id)

        return tostring(root_tag)

    def create_request_status(self, number_of_test_points=None, add_test_points=None, completion_value=None):

        root_tag = Element(self.request_tag)

        self.create_request_root(root_tag, request_type="Status")

        status_child = SubElement(root_tag, 'status')

        if completion_value:
            child_tag = SubElement(status_child, 'completionValue')
            child_tag.text = str(completion_value)

        if number_of_test_points:
            child_tag = SubElement(status_child, 'num_of_test_points')
            child_tag.text = str(number_of_test_points)

        if add_test_points:
            child_tag = SubElement(status_child, 'add_test_points')
            child_tag.text = str(add_test_points)

        return tostring(root_tag)

    def create_request_variable(self, custom_variable_list, root_tag=None):

        # Id variables are being sent along
        if root_tag is None:
            root_tag = Element(self.request_tag)

            self.create_request_root(root_tag, request_type="variable")

        for custom_variable in custom_variable_list:
            top = SubElement(root_tag, "customVariables")

            child = SubElement(top, 'name')
            child.text = str(custom_variable.custom_name)
            child = SubElement(top, 'defaultVal')
            child.text = str(custom_variable.default_value)
            child = SubElement(top, 'customVal')
            # Send the file path as the custom value - instead of entire file content
            if "file" == str(custom_variable.type).lower():
                child.text = str(custom_variable.file_path)
            else:
                child.text = str(custom_variable.custom_value)

            child = SubElement(top, 'variableDesc')
            child.text = str(custom_variable.description)

            # if there is a choice of specific value, list them to user instead
            if custom_variable.acceptedVals:
                child = SubElement(top, 'acceptedVals')
                child.text = str(custom_variable.acceptedVals)

            if custom_variable.numerical_max:
                child = SubElement(top, 'numerical_max')
                child.text = str(custom_variable.numerical_max)

            if custom_variable.type:
                child = SubElement(top, 'type')
                child.text = str(custom_variable.type)

            # What group does the custom variable belong to?
            child = SubElement(top, 'group')
            child.text = str(custom_variable.var_group)

        return tostring(root_tag)

    def add_xml_drive(self, device, tree_tag):

        top = SubElement(tree_tag, "found_drives")

        if isinstance(device, DriveWrapper):
            child = SubElement(top, 'Name')
            child.text = str(device.description)

            child = SubElement(top, 'Standard')
            child.text = str(device.identifier_str)

            child = SubElement(top, 'ConnType')
            child.text = str(device.drive_type)

            child = SubElement(top, 'Drive_Path')
            child.text = str(device.drive_path)

            child = SubElement(top, 'Sys_Cmd')
            child.text = str(device.system_cmd)

            child = SubElement(top, 'itemType')
            child.text = str("Drive")

            child = SubElement(top, 'XmlVersion')
            child.text = str(self.versionNumber)

    def add_xml_quarch_module(self, dict_key, dict_value, tree_tag, output_mode=None):

        top = SubElement(tree_tag, "quarch_modules")

        indexOfColon = dict_key.find(":")
        conType = str(dict_key[:indexOfColon])
        IpAddress = str(dict_key[indexOfColon + 1:])

        child = SubElement(top, 'ConnType')
        child.text = str(conType)

        child = SubElement(top, 'QtlNum')
        child.text = str(dict_value)

        child = SubElement(top, 'itemType')
        child.text = str("Module")

        if output_mode is not None:
            child = SubElement(top, "OutputMode")
            child.text = str(output_mode)

        child = SubElement(top, 'IpAddress')
        child.text = str(IpAddress)

    def add_report_item(self, dictionary, tree_tag, output_mode=None):

        top = SubElement(tree_tag, "report_items")

        for key, val in dictionary.items():
            child = SubElement(top, key)

            if "custom_variables" in key:
                self.create_request_variable(custom_variable_list=val, root_tag=top)

            else:
                child = SubElement(top, str(key))
                child.text = str(dictionary[key])


    def notifyTestLogEventXml(self, tree_tag, unique_id, timeStamp, logType, logText, logSource, test_result=None,
                              log_details=None, group=None, sub_group=None, check_point_id=None):
        if unique_id == "" or unique_id is None:
            # quick check in place just to ensure the unique id of an object is not sent incorrectly
            unique_id = " "

        # Build main XML structure
        xml_object = cElementTree.SubElement(tree_tag, "log_object")
        cElementTree.SubElement(xml_object, "uniqueID").text = unique_id
        cElementTree.SubElement(xml_object, "timestamp").text = datetime.utcfromtimestamp(timeStamp).strftime(
            '%Y-%m-%d %H:%M:%S')
        cElementTree.SubElement(xml_object, "logType").text = logType
        cElementTree.SubElement(xml_object, "text").text = logText
        cElementTree.SubElement(xml_object, "messageSource").text = logSource
        if test_result is not None:
            cElementTree.SubElement(xml_object, "test_result").text = test_result
            cElementTree.SubElement(xml_object, "check_point_id").text = str(check_point_id)
        if group:
            cElementTree.SubElement(xml_object, "group").text = group
        if sub_group:
            cElementTree.SubElement(xml_object, "sub_group").text = sub_group

        # Add details dictionary if present
        if log_details is not None:
            xml_details = cElementTree.SubElement(xml_object, "logDetails")
            for k, v in log_details.items():
                xml_entry = cElementTree.SubElement(xml_details, "entry")
                cElementTree.SubElement(xml_entry, "key").text = str(k)
                cElementTree.SubElement(xml_entry, "value").text = str(v)

    def send_stop_test(self, reason=""):
        self.sendMsgToGUI(self.create_request_function(function_call="stop_test", function_value=reason,
                                                       requires_response=False))

    def send_finish_test(self):
        self.sendMsgToGUI(self.create_request_function(function_call="finished_test", requires_response=False))

    def send_start_timeout(self):
        self.sendMsgToGUI(self.create_request_function(function_call="start_timeout", requires_response=False))

    def send_stop_timeout(self):
        self.sendMsgToGUI(self.create_request_function(function_call="stop_timeout", requires_response=False))

    def parse_response(self, xml_tree, original_data):

        new_response = testLine()

        if str(xml_tree.tag).lower() == "response":
            new_response.parse_response(xml_tree, original_data)

        if new_response.qcs_version:
            dtsGlobals.QCSVersionValid = isVersionCompat(new_response.qcs_version)
            return True

        if new_response.user_choice:
            dtsGlobals.choiceResponse = new_response.user_choice
            return True

        if str(new_response.request_stop).lower() == "true":
            dtsGlobals.continueTest = False
            return True

        if new_response.qpy_version_valid and bool(new_response.qpy_version_valid) is False:
            dtsGlobals.validVersion = False
            return True

        if new_response.is_c_var_response:
            self.response = new_response.custom_variable_dict
            if not self.response:
                self.response = {}
            return True

        if new_response.qpy_installed:
            if str(new_response.qpy_installed).lower() == "true":
                dtsGlobals.quarchpy_installed = True
            else:
                dtsGlobals.quarchpy_installed = False
            return True

        if new_response.function_complete:
            return True

        return False

def isVersionCompat(version_number):
    # If the min version is current version, it is fine
    if version_number == dtsGlobals.minQCSVersion:
        return True
    if "dev" in version_number.lower():
        logging.warning("Using Dev version of quarchpy: Allowing continue")
        return True

    version_numbers_passed = version_number.split(".") if "." in version_number else [version_number]
    min_version_required = dtsGlobals.minQCSVersion.split(".") if "." in dtsGlobals.minQCSVersion else [dtsGlobals.minQCSVersion]
    # Iterate through each number to ensure compat
    for i, number in enumerate(version_numbers_passed):

        """
        min version         = 1.1
        verison passed      = 1.1.1
        Result              = Fail
        """
        if i == len(min_version_required) - 1:
            if not version_numbers_passed[i] >= min_version_required[i]:
                return False
            return True

        if i == len(version_numbers_passed) - 1:
            if not version_numbers_passed[i] > min_version_required[i]:
                return False
            return True



        # If same item is > it is a pass
        if version_numbers_passed[i] > min_version_required[i]:
            return True
        # If same item is < it is a fail
        if version_numbers_passed[i] < min_version_required[i]:
            return False

    return True


