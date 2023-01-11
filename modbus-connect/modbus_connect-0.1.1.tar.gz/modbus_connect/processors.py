from typing import List

import pymodbus.payload
import pymodbus.register_read_message
import pymodbus.bit_read_message
import pymodbus.constants

import modbus_connect.utils as utils
from modbus_connect.utils import MemoryBanks, DataTypes


def process_batch(
    batch: utils.ModbusRegisters,
    batch_results: pymodbus.register_read_message.ReadHoldingRegistersResponse
    or pymodbus.bit_read_message.ReadCoilsResponse,
    byte_order: pymodbus.constants.Endian,
    word_order: pymodbus.constants.Endian,
) -> utils.ModbusResults:
    # Initialize the list of results
    values: utils.ModbusResults = []

    # Check the memory bank of the first register in the batch to determine the processing function between word like or bit like, for each register in the batch, process the register and append the result to the list of results
    if batch[0].memorybank == utils.MemoryBanks.HOLDING_REGISTERS:
        for tag in batch:
            if (
                tag.memorybank == utils.MemoryBanks.HOLDING_REGISTERS
                or tag.memorybank == utils.MemoryBanks.INPUT_REGISTERS
            ):
                values.append(
                    utils.ModbusResult(
                        tag,
                        process_wordlike_register(
                            tag,
                            batch_results.registers[
                                tag.address
                                - batch[0].address : (
                                    tag.address - batch[0].address
                                )
                                + tag.length
                            ],
                            byte_order,
                            word_order,
                        ),
                    )
                )
    elif (
        batch[0].memorybank == utils.MemoryBanks.COILS
        or batch[0].memorybank == utils.MemoryBanks.DISCRETE_INPUTS
    ):
        for register in batch:
            if (
                register.memorybank == utils.MemoryBanks.COILS
                or register.memorybank == utils.MemoryBanks.DISCRETE_INPUTS
            ):
                values.append(
                    process_bitlike_register(
                        register,
                        batch_results.getBit(
                            register.address - batch[0].address
                        ),
                    )
                )

    return values


def process_wordlike_register(
    tag: utils.ModbusRegister,
    registers_list: list[int],
    byte_order: pymodbus.constants.Endian,
    word_order: pymodbus.constants.Endian,
) -> any:
    if tag.datatype == DataTypes.INT16:
        return registers_list[0]

    elif tag.datatype == DataTypes.INT32:
        return pymodbus.payload.BinaryPayloadDecoder.fromRegisters(
            registers_list,
            byte_order,
            wordorder=word_order,
        ).decode_32bit_int()

    elif tag.datatype == DataTypes.FLOAT32:
        return pymodbus.payload.BinaryPayloadDecoder.fromRegisters(
            registers_list,
            byte_order,
            wordorder=word_order,
        ).decode_32bit_float()

    else:
        raise ValueError("Invalid datatype: " + tag.datatype)


def process_bitlike_register(
    tag: utils.ModbusRegister,
    register: any,
):
    value = None

    if tag.datatype == DataTypes.BOOL:
        value = utils.ModbusResult(tag, bool(register))

    else:
        raise ValueError("Invalid datatype: " + tag["datatype"])

    return value
