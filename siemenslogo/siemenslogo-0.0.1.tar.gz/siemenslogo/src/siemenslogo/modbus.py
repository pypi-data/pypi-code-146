from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.register_read_message import ReadInputRegistersResponse, ReadHoldingRegistersResponse

from Logo.src.siemenslogo.exceptions import MaxCountException


class CustomModbus(ModbusClient):

  def __init__(self, **kwargs):
    ModbusClient.__init__(self, **kwargs)

  def read_holding_register(self, address, count=1):
    try:
      return self.read_holding_registers(address=address, count=count, unit=self.unit)
    except:
      return None

  def fetch_holding_registers_data(self, address: int = 0, count: int = 1) -> list:
    i = 0
    while True:
      i = i + 1
      if (i > self.retries):
        raise MaxCountException('cannot fetch data')
      try:
        registers_data = self.read_holding_register(address=address, count=count)
        return registers_data.registers
      except Exception as e:
        print (e)
        pass

  def read_holding_register(self, address: int = 0, count: int = 1) -> ReadHoldingRegistersResponse:
      return self.read_holding_registers(address=address, count=count, unit=self.unit)

  def fetch_input_registers_data(self, address: int = 0, count: int = 1) -> list:
    i = 0
    while True:
      i = i + 1
      if (i > self.retries):
        raise MaxCountException('cannot fetch data')
      try:
        registers_data = self.read_input_register(address=address, count=count)
        return registers_data.registers
      except Exception as e:
        print(e)
        pass

  def read_input_register(self, address: int = 0, count = 1) -> ReadInputRegistersResponse:
      return self.read_input_registers(address=address, count=count, unit=self.unit)

  def write_registers(self, address: int, values ):
    return self.write_registers(address=address, values=values, unit=self.unit)