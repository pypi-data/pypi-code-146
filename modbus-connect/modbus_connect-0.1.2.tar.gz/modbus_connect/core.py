from typing import List
from dataclasses import dataclass, field

import logging

import pymodbus
import pymodbus.register_read_message
import pymodbus.client.tcp
import pymodbus.payload
import pymodbus.constants

import modbus_connect.utils as utils
import modbus_connect.processors as processors


logger = logging.getLogger()


class ModbusGateway:
    def __init__(
        self,
        host: str,
        port: int,
        slave: int = 1,
        timeout: int = 3,
        tags_list: List[utils.ModbusRegister] = [],
        batch_size: int = 60,
        byteorder: pymodbus.constants.Endian = pymodbus.constants.Endian.Big,
        wordorder: pymodbus.constants.Endian = pymodbus.constants.Endian.Little,
    ):
        self.host = host
        self.port = port
        self.slave = slave
        self.timeout = timeout
        self.batch_size = batch_size
        self.tags_list = tags_list
        self.byte_order = byteorder
        self.word_order = wordorder

        # Create modbus server connections using pymodbus library, using the host and port parameters, using the ModbusTcpClient class¡
        self.client = pymodbus.client.tcp.ModbusTcpClient(
            self.host, self.port, timeout=self.timeout
        )
        self.tags_requests: utils.ModbusRegistersBatched = []

        if self.tags_list != []:
            self.configure_tags()

    def __del__(self):
        self.client.close()

    def connect(self):
        self.client.connect()

    def set_tags_list(self, tags_list: List[utils.ModbusRegister]):
        self.tags_list = tags_list
        self.tags_requests: utils.ModbusRegistersBatched = []
        self.configure_tags()

    def configure_tags(self):
        # For each tags_request, sort the list of dictionaries by address and the make batches of consecutive addresses with a maximum size of self.batch_size

        self.tags_requests = utils.make_batch_consecutive_bank_and_size(
            self.tags_list, self.batch_size
        )

    # Get variables values from modbus server
    # It gets the values in batches of 60 variables, using the address from the tags dictionary, and returns a dictionary with tha varibles names as keys and the server values
    def read_tags(self) -> utils.ModbusResults:
        # List to store the values of the results
        values: utils.ModbusResults = utils.ModbusResults([])

        # For each batch of tags, read the values from the modbus server and process them
        for batch in self.tags_requests:
            # Check if the batch is not empty
            if len(batch) == 0:
                continue

            batch_results = None

            # Check the memory bank of the batch and process the values accordingly
            # Holding registers
            if batch[0].memorybank == utils.MemoryBanks.HOLDING_REGISTERS:
                try:
                    batch_results = self.client.read_holding_registers(
                        batch[0].address,
                        count=utils.get_batch_memory_length(batch),
                        slave=self.slave,
                    )
                    if batch_results.isError():
                        raise Exception("Modbus error: " + str(batch_results))

                except Exception as e:
                    raise Exception(
                        "Error reading from modbus server from address "
                        + str(batch[0].address)
                        + " to address "
                        + str(batch[-1].address)
                    )
            elif batch[0].memorybank == utils.MemoryBanks.INPUT_REGISTERS:
                # TODO: Implement input registers read
                raise NotImplementedError("Input registers not implemented")

            elif batch[0].memorybank == utils.MemoryBanks.DISCRETE_INPUTS:
                # TODO: Implement discrete inputs read
                raise NotImplementedError("Discrete inputs not implemented")

            elif batch[0].memorybank == utils.MemoryBanks.COILS:
                # TODO: Implement coils read
                raise NotImplementedError("Coils not implemented")
            else:
                raise Exception("Non supported memory bank")

            # Process the values
            if batch_results is not None:
                values += processors.process_batch(
                    batch, batch_results, self.byte_order, self.word_order
                )

        return values

    def tags_ready(self) -> bool:
        return len(self.tags) > 0


if __name__ == "__main__":
    # Create a ModbusGateway object, using the host and port parameters, and the tags_list parameter, which is a list of dictionaries with the variable names and memory addresses
    gateway = ModbusGateway(
        host="docencia.i4techlab.upc.edu",
        port=20000,
        tags_list=[
            {
                "name": "var1",
                "address": 0,
                "memory_bank": utils.MemoryBanks.HOLDING_REGISTERS,
                "datatype": "float32",
            },
            {
                "name": "var2",
                "address": 1,
                "memory_bank": utils.MemoryBanks.HOLDING_REGISTERS,
                "datatype": "float32",
            },
        ],
    )

    # Read the values from the modbus server
    values = gateway.read_tags()
    print(values)
    logger.info(values)
