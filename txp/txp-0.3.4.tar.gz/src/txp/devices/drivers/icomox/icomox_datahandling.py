"""
This module contains the implementation of the data handling for the icomox.
Parsers and descriptor objects are implemented.
Technical details about the device can be found in the following document:
"""
# ============================ imports =========================================
import datetime
import logging
import struct
import time
from abc import abstractmethod, ABC
from enum import Enum
from common import iCOMOX_messages, messages_utils, helpers, common
from common.common import iCOMOXs
from common.iCOMOX_list import sCOMOX_TCPIP, sCOMOXs_list
from common.iCOMOX_messages import OUT_MSG_Hello, OUT_MSG_SetConfiguration, OUT_MSG_Reset
from txp.common.config import settings
import logging

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


# ==============================================================================
# Responses descriptors implementation
# ==============================================================================

SOFTWARE_RESET_TYPE=0

class IcomoxResponsesTypes(Enum):
    HELLO_MESSAGE_RESPONSE = "HELLO_MESSAGE_RESPONSE"
    CONFIGURATION_RESPONSE = "CONFIGURATION_RESPONSE"
    EEPROM_RESPONSE = "EEPROM_RESPONSE"
    EEPROM_VALUES_RESPONSE = "EEPROM_VALUES_RESPONSE"
    OK_RESPONSE = "OK_RESPONSE"


class IcomoxAPIMessageDescriptor(ABC):
    def __init__(self, type):
        self._messageType = type

    @staticmethod
    @abstractmethod
    def parseFromRawMessage(msg):
        pass


class IcomoxEEPROMValueResponseDescriptor(IcomoxAPIMessageDescriptor):

    @staticmethod
    def parseFromRawMessage(msg):
        # TODO: implement the message parsing and builder of the class
        return IcomoxEEPROMValueResponseDescriptor()

    def __init__(self):
        IcomoxAPIMessageDescriptor.__init__(IcomoxResponsesTypes.EEPROM_VALUES_RESPONSE)


class IcomoxEEPROMStatusResponseDescriptor(IcomoxAPIMessageDescriptor):
    def __init__(self):
        IcomoxAPIMessageDescriptor.__init__(IcomoxResponsesTypes.EEPROM_RESPONSE)
        self._resultValue = None

    def _setResultValue(self, result):
        self._resultValue = result

    def getResultValue(self):
        return self._resultValue

    def isEEMPROMStateOK(self):
        return self._resultValue == 0

    @staticmethod
    def parseFromRawMessage(msg):
        count, address, result = struct.unpack_from("<BHB", msg, 1)
        resultValue = "EEPROM_OK"
        if result != 0:
            resultValue = "ERROR"
        descriptor = IcomoxEEPROMStatusResponseDescriptor()
        descriptor._setResultValue(resultValue)
        return descriptor


class IcomoxOKResponseDescriptor(IcomoxAPIMessageDescriptor):
    def __init__(self):
        IcomoxAPIMessageDescriptor.__init__(IcomoxResponsesTypes.OK_RESPONSE)
        self._responseValue = None

    def getResponseValue(self):
        return "OK"

    @staticmethod
    def parseFromRawMessage(msg):
        # TODO: evaluate the value to implement the parser. Evaluate if not OK response is sent.
        descriptor = IcomoxOKResponseDescriptor()
        return descriptor


class IcomoxCongurationResponseDescriptor(IcomoxAPIMessageDescriptor):
    def __init__(self):
        IcomoxAPIMessageDescriptor.__init__(IcomoxResponsesTypes.CONFIGURATION_RESPONSE)
        self._common = None
        self._repetition = None
        self._intervalInMinutes = None
        self._activeModules = None
        self._rawDataSensors = None
        self._maintenanceModuleSensors = None
        self._maintenanceModuleFlags = None
        self._maintenanceModuleAlpha = None

    def getResponseType(self):
        return self._messageType

    def _setCommon(self, common):
        self._common = common

    def getCommon(self):
        return self._common

    def _setRepetition(self, repetition):
        self._repetition = repetition

    def getRepetition(self):
        return self._repetition

    def _setIntervalInMinutes(self, intervalInMinutes):
        self._intervalInMinutes = intervalInMinutes

    def getIntervalInMinutes(self):
        return self._intervalInMinutes

    def _setActiveModules(self, activeModules):
        self._activeModules = activeModules

    def getActiveModules(self):
        return self._activeModules

    def _setRawDataSensors(self, rawDataSensors):
        self._rawDataSensors = rawDataSensors

    def getRawDataSensors(self):
        return self._rawDataSensors

    def _setMaintenanceModuleSensors(self, maintenanceModuleSensors):
        self._maintenanceModuleSensors = maintenanceModuleSensors

    def getMaintenanceModuleSensors(self):
        return self._maintenanceModuleSensors

    def _setMaintenanceModuleFlags(self, maintenanceModuleFlags):
        self._maintenanceModuleFlags = maintenanceModuleFlags

    def getMaintenanceModuleFlags(self):
        return self._maintenanceModuleFlags

    def _setMaintenanceModuleAlpha(self, maintenanceModuleAlpha):
        self._maintenanceModuleAlpha = maintenanceModuleAlpha

    def getMaintenanceModuleAlpha(self):
        return self._maintenanceModuleAlpha

    @staticmethod
    def parseFromRawMassage(self, msg):
        """
        This static method is the entry point to build the IcomoxCongurationResponseDescriptor instance.
        :param msg: bytearray containing the raw data of a configuration message response from icomox
        :return: IcomoxConfigurationResponseDescriptor
        """
        descriptor = IcomoxCongurationResponseDescriptor()

        Common, \
        Repetition, IntervalInMinutes, \
        ActiveModules, \
        RawDataSensors, \
        ML1_target, ML1_selSensor, ML1_countLearned, ML1_modelLearned, \
        MaintenanceModule_sensors, MaintenanceModule_flags, MaintenanceModule_alpha = iCOMOX_messages.IN_MSG_GetConfiguration(
            msg)

        descriptor._setCommon(Common)
        descriptor._setRepetition(Repetition)
        descriptor._setIntervalInMinutes(IntervalInMinutes)
        descriptor._setActiveModules(ActiveModules)
        descriptor._setRawDataSensors(RawDataSensors)
        descriptor._setMaintenanceModuleSensors(MaintenanceModule_sensors)
        descriptor._setMaintenanceModuleFlags(MaintenanceModule_flags)
        descriptor._setMaintenanceModuleAlpha(MaintenanceModule_alpha)

        return descriptor


class IcomoxHelloMessageDescriptor:
    def __init__(self):
        self._boardType = None
        self._boardVersion = None
        self._mcuSerialNumber = None
        self._firmwareReleaseVersion = None
        self._bitStatus = None

    def _setBitStatus(self, bitStatus):
        self._bitStatus = bitStatus

    def getBitStatus(self):
        return self._bitStatus

    def _setBoardType(self, boardType):
        self._boardType = boardType

    def getBoardType(self):
        return self._boardType

    def _setBoardVersion(self, boardVersionMajor, boardVertionMinor):
        self._boardVersion = messages_utils.iCOMOX_BoardVersion_to_Str(board_version_major=boardVersionMajor,
                                                                       board_version_minor=boardVertionMinor)

    def getBoardVersion(self):
        return self._boardVersion

    def _setMcuSerialNumber(self, mcuSerialNumber):
        self._mcuSerialNumber = mcuSerialNumber

    def getMcuSerialNumber(self):
        return self._mcuSerialNumber

    def getMcuSerialNumberString(self):
        return helpers.u8s_to_str(arr=self._mcuSerialNumber, separator="")

    def _setFirmwareReleaseVersion(self, hello_firmware_release_version_major, hello_firmware_release_version_minor,
                                   hello_firmware_release_version_patch):
        self._firmwareReleaseVersion = (hello_firmware_release_version_major << 16) + (
                hello_firmware_release_version_minor << 8) + hello_firmware_release_version_patch

    def getFirmwareReleaseVersion(self):
        return self._firmwareReleaseVersion

    @staticmethod
    def parseFromRawData(msg):
        """
        This static method is the entry point to build the IcomoxHelloMessageDescriptor instance.
        :param msg: bytearray containing the raw data of a configuration message response from icomox
        :return: IcomoxHelloMessageDescriptor
        """
        hello_board_type, \
        hello_board_version_major, hello_board_version_minor, \
        hello_mcu_serial_number, \
        hello_firmware_release_version_major, hello_firmware_release_version_minor, hello_firmware_release_version_patch, hello_firmware_release_version_branch, \
        hello_firmware_build_version_date_year, hello_firmware_build_version_date_month, hello_firmware_build_version_date_day, \
        hello_firmware_build_version_time_hour, hello_firmware_build_version_time_minute, hello_firmware_build_version_time_second, \
        hello_bit_status, \
        hello_product_part_number, hello_production_serial_number, hello_name, \
        smip_swMajor, smip_swMinor, smip_swPatch, smip_swBuild = iCOMOX_messages.IN_MSG_Hello(msg=msg)

        descriptor = IcomoxHelloMessageDescriptor()
        descriptor._setFirmwareReleaseVersion(hello_firmware_release_version_major,
                                              hello_firmware_release_version_minor,
                                              hello_firmware_release_version_patch)
        descriptor._setBoardType(hello_board_type)
        descriptor._setBitStatus(hello_bit_status)
        descriptor._setBoardVersion(hello_board_version_major, hello_board_version_minor)
        descriptor._setMcuSerialNumber(hello_mcu_serial_number)

        return descriptor


# ==============================================================================
# Module Functions
# ==============================================================================
def sendGetHelloMessageCommand(icomox: sCOMOX_TCPIP):
    """
    :param icomox: icomox tcp instance
    """
    if icomox is not None:
        icomox.transmit_buffer = OUT_MSG_Hello()
    else:
        raise Exception("Not valid icomox instance")

def sendSetConfigurationCommand(uniqueId,enableTransmition):
    iComox = iCOMOXs.find_by_UniuqeID(uniqueId)
    if iComox is not None:
        ConfigBitmask = 3
        ConfigModulesBitmask = 1
        LocalTimestamp = int(time.time() + (datetime.datetime.now() - datetime.datetime.utcnow()).total_seconds())   # mktime(time.localtime()))
        IntervalInMinutes=0
        Repetition=0
        if enableTransmition:
            Common = 65
        else:
            Common = 0
        ActiveModules = 1
        RawData_Sensors = 31
        # Module_AnomalyDetection_Command, Module_AnomalyDetection_stateToTrain, Module_AnomalyDetection_Sensors = self.WindowToModuleAnomalyDetection()
        Module_AnomalyDetection_Sensors = iCOMOX_messages.cCOMOX_SENSOR_BITMASK_ADXL356
        Module_AnomalyDetection_stateToTrain = 0
        Module_AnomalyDetection_Command = iCOMOX_messages.cANOMALY_DETECTION_COMMAND_Reset

        iComoxMessage = OUT_MSG_SetConfiguration(ConfigBitmask=ConfigBitmask, ConfigModulesBitmask=ConfigModulesBitmask, \
                                                        LocalTimestamp=LocalTimestamp, \
                                                        Common=Common, \
                                                        Repetition=Repetition, IntervalInMinutes=IntervalInMinutes, \
                                                        ActiveModules=ActiveModules, \
                                                        RawData_Sensors=RawData_Sensors, \
                                                        AnomalyDetection_Command=Module_AnomalyDetection_Command, AnomalyDetection_Sensors=Module_AnomalyDetection_Sensors, AnomalyDetection_StateToTrain=Module_AnomalyDetection_stateToTrain)


        iComox.transmit_buffer = iComoxMessage
    else:
        raise Exception("Not valid icomox instance")

def resetIcomox(uniqueId):
    iComox = iCOMOXs.find_by_UniuqeID(uniqueId)
    if iComox is not None:
        log.info("{} icomox is being reseting".format(uniqueId))
        iComox.transmit_buffer = OUT_MSG_Reset(SOFTWARE_RESET_TYPE)
    else:
        log.error("{} icomox reset attemp error".format(uniqueId))

def getHelloMessage(msg, icomox):
    """
    This module funtion tries to get the hello message object to identify the connected icomox EDGE

    :param msg: raw data from icomox
    :param icomox: icomox TCP type object
    :return: IcomoxHelloMessageDescriptor if message contains hello info. None if message is not hello type
    """
    if msg[0] == iCOMOX_messages.cCOMOX_MSG_CODE_Hello:
        return IcomoxHelloMessageDescriptor.parseFromRawData(msg)
    else:
        return None

def processSDKCommandResponse(msg):
    """
    this funtion module takes care of processing an icomox message containing a response from the SDK available commands API
    :param msg: bytearray() raw data from icomox
    :return: IcomoxAPIMessageDescriptor.  None if message is not valid.
    """
    msg_code = msg[0]
    response = None
    if msg_code == iCOMOX_messages.cCOMOX_MSG_CODE_Reset:
        response = IcomoxOKResponseDescriptor.parseFromRawMessage(msg)
    elif msg_code == iCOMOX_messages.cCOMOX_MSG_CODE_GetConfiguration:
        response = IcomoxCongurationResponseDescriptor.parseFromRawMessage(msg)
    elif msg_code == iCOMOX_messages.cCOMOX_MSG_CODE_SetConfiguration:
        response = IcomoxOKResponseDescriptor.parseFromRawMessage(msg)
    elif msg_code == iCOMOX_messages.cCOMOX_MSG_CODE_ReadEEPROM:
        response = IcomoxEEPROMValueResponseDescriptor.parseFromRawMessage(msg)
    elif msg_code == iCOMOX_messages.cCOMOX_MSG_CODE_WriteEEPROM or iCOMOX_messages.cCOMOX_MSG_CODE_VerifyEEPROM:
        response = IcomoxEEPROMStatusResponseDescriptor.parseFromRawMessage(msg)
    elif msg_code == iCOMOX_messages.cCOMOX_MSG_CODE_Debug:
        log.error("Unsupported message response implementation for cCOMOX_MSG_CODE_Debug type")
        response = IcomoxOKResponseDescriptor.parseFromRawMessage(msg)
    else:
        # TODO: review the possibility to raise an exception for getting invalid message.
        log.error("Non supported message code for SDK. Message code received {}".format(msg_code))
    return response


class IcomoxMessageType(Enum):
    REPORT_MESSAGE = "REPORT_MESSAGE"
    API_MESSAGE = "API_MESSAGE"
    HELLO = "HELLO"
    INVALID = "INVALID"

def getIcomoxMessageType(msg):
    msg_code = msg[0]
    messageType = IcomoxMessageType.INVALID

    if msg_code == iCOMOX_messages.cCOMOX_MSG_CODE_Hello:
        messageType = IcomoxMessageType.HELLO
    elif msg_code == iCOMOX_messages.cCOMOX_MSG_CODE_Report:
        messageType = IcomoxMessageType.REPORT_MESSAGE
    elif (msg_code & 7) > 0: #this is a validation forced by SDK the supported messages are in that range.
        messageType = IcomoxMessageType.API_MESSAGE

    return messageType

class IcomoxSensorMassageType(Enum):
    VIBRATION_SENSOR_ADXL362 = "VIBRATION_SENSOR_ADXL362"
    VIBRATION_SENSOR_ADXL356 = "VIBRATION_SENSOR_ADXL356"
    MAGNETOMETER_SENSOR_BMM150 = "MAGNETOMETER_SENSOR_BMM150"
    TEMPERATURE_SENSOR_ADT7410 = "TEMPERATURE_SENSOR_ADT7410"
    MICROPHONE_SENSOR_IM69D130 = "MICROPHONE_SENSOR_IM69D130"
    INVALID_SENSOR = "INVALID_SENSOR"

def getSignalSamples(msg):
    module, sensor, axis, timestamp = iCOMOX_messages.IN_MSG_Report(msg=msg)
    payload = msg[10:]
    samples = None
    sensorType = IcomoxSensorMassageType.INVALID_SENSOR
    if module == iCOMOX_messages.cMODULE_RawData:
        if iCOMOX_messages.cCOMOX_SENSOR_ADXL362 == sensor:
            samples = getVibrationSignalSamplesFromADXL362(payload)
            sensorType = IcomoxSensorMassageType.VIBRATION_SENSOR_ADXL362
        elif iCOMOX_messages.cCOMOX_SENSOR_ADXL356 == sensor:
            acc_x_units_g, acc_y_units_g, acc_z_units_g = common.ADXL356.msg_bytes_to_samples_g(payload=payload)
            samples = list([acc_x_units_g, acc_y_units_g, acc_z_units_g])
            sensorType =  IcomoxSensorMassageType.VIBRATION_SENSOR_ADXL356
        elif iCOMOX_messages.cCOMOX_SENSOR_BMM150 == sensor:
            mag_x_data, mag_y_data, mag_z_data = common.BMM150.msg_bytes_to_samples_uTesla(payload=payload)
            samples = list([mag_x_data, mag_y_data, mag_z_data])
            sensorType = IcomoxSensorMassageType.MAGNETOMETER_SENSOR_BMM150
        elif iCOMOX_messages.cCOMOX_SENSOR_ADT7410 == sensor:
            temp_data = common.ADT7410.msg_bytes_to_sample_Celsius(payload=payload)
            samples = [temp_data]
            sensorType = IcomoxSensorMassageType.TEMPERATURE_SENSOR_ADT7410
        elif iCOMOX_messages.cCOMOX_SENSOR_IM69D130 == sensor:
            samples_SPL = common.IM69D130.msg_bytes_to_samples_SPL(payload=payload)
            samples = list([samples_SPL])
            sensorType = IcomoxSensorMassageType.MICROPHONE_SENSOR_IM69D130

    return sensorType,samples

def getVibrationSignalSamplesFromADXL362(payload):
    acc_x_units_g, acc_y_units_g, acc_z_units_g = common.ADXL362.msg_bytes_to_samples_g(payload=payload)
    return list([acc_x_units_g, acc_y_units_g, acc_z_units_g])
