from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from Logo.src.siemenslogo.exceptions import MaxCountException
from Logo.src.siemenslogo.modbus import CustomModbus
import logging

logger = logging.getLogger(__name__)


class Unit:
  modbus: ModbusClient = None

  def __init__(self, **kwargs):
    self.kwargs = dict(**kwargs)
    self.modbus = CustomModbus(**self.kwargs)
    logger.debug("init Siemens Logo unit")

  def __del__(self):
    self.modbus.close()

  def set_flag(self, number: int, value: bool):
    self.modbus.write_coil(address=8255 + number, value=value)

  def set_analog_flag(self, number: int, value: int):
    self.modbus.write_register(address=527 + number, value=value)

  def get_property(self, type: str, number: int = 0, count: int = 1):
    if type == "V":
      data = self.get_local_variable_state(number, count)
    elif type == "Q":
      data = self.get_outputs_state(number, count)
    elif type == "M":
      data = self.get_flags_state(number, count)
    elif type == "I":
      data = self.get_inputs_state(number, count)
    elif type == "VW":
      data = self.get_local_analog_variable_state(number, count)
    elif type == "AQ":
      data = self.get_analog_outputs_state(number, count)
    elif type == "AM":
      data = self.get_analog_flags_state(number, count)
    elif type == "AI":
      data = self.get_analog_inputs_state(number, count)
    else:
      data = None
    return data

  def get_local_variable_state(self, number: int = 1, count: int = 64) -> list:
    if number + count > 2000:
      raise MaxCountException('Maximum output number is 64')
    return self.modbus.read_coils(address=number - 1, count=count).bits

  def get_outputs_state(self, number: int = 1, count: int = 64) -> list:
    if number + count > 65:
      raise MaxCountException('Maximum output number is 64')
    return self.modbus.read_coils(address=8191+number, count=count).bits

  def get_flags_state(self, number: int = 1, count: int = 64) -> list:
    if number + count > 65:
      raise MaxCountException('Maximum flag number is 64')
    return self.modbus.read_coils(address=8255+number, count=count).bits

  def get_inputs_state(self, number: int = 1, count: int = 24) -> list:
    if number + count > 25:
      raise MaxCountException('Maximum input number is 24')
    a = self.modbus.read_discrete_inputs(address=number - 1, count=count)
    return a.bits

  def get_local_analog_variable_state(self, number: int = 1, count: int = 16) -> list:
    if number + count > 850:
      raise MaxCountException('Maximum input number is 849')
    a = self.modbus.read_holding_registers(address=number - 1, count=count).registers
    return a

  def get_analog_outputs_state(self, number: int = 1, count: int = 26) -> list:
    if number + count > 27:
      raise MaxCountException('Maximum analog input number is 26')
    a = self.modbus.read_holding_registers(address=512 + number - 1, count=count).registers
    return a

  def get_analog_flags_state(self, number: int = 1, count: int = 64) -> list:
    if number + count > 65:
      raise MaxCountException('Maximum analog flag number is 64')
    a = self.modbus.read_holding_registers(address=528+number - 1, count=count).registers
    return a

  def get_analog_inputs_state(self, number: int = 1, count: int = 16) -> list:
    if number + count > 17:
      raise MaxCountException('Maximum analog inputs number is 16')
    a = self.modbus.read_input_registers(address=number - 1, count=count).registers
    return a

