import typing
from typing import List, NewType

from dataclasses import dataclass, field
from typing import List, TypedDict
from enum import Enum

# --------------------- TYPES ---------------------


class MemoryBanks(Enum):
    HOLDING_REGISTERS = "holding_registers"
    INPUT_REGISTERS = "input_registers"
    DISCRETE_INPUTS = "discrete_inputs"
    COILS = "coils"

    __lt__ = lambda self, other: self.value < other.value
    __eq__ = lambda self, other: self.value == other.value
    __gt__ = lambda self, other: self.value > other.value


class DataTypes(Enum):
    BOOL = "bool"
    INT16 = "int16"
    UINT16 = "uint16"
    INT32 = "int32"
    UINT32 = "uint32"
    FLOAT32 = "float32"
    INT64 = "int64"
    UINT64 = "uint64"
    FLOAT64 = "float64"


def datatype_lenght(datatype: DataTypes) -> int:
    if datatype == DataTypes.BOOL:
        return 1
    elif datatype == DataTypes.INT16:
        return 1
    elif datatype == DataTypes.UINT16:
        return 1
    elif datatype == DataTypes.INT32:
        return 2
    elif datatype == DataTypes.UINT32:
        return 2
    elif datatype == DataTypes.FLOAT32:
        return 2
    elif datatype == DataTypes.INT64:
        return 4
    elif datatype == DataTypes.UINT64:
        return 4
    elif datatype == DataTypes.FLOAT64:
        return 4
    else:
        raise ValueError("Datatype not supported")


@dataclass
class ModbusRegister:
    name: str
    address: int
    memorybank: MemoryBanks
    datatype: DataTypes

    # Create a lenght property to be able to know the lenght of the register by its datatype
    @property
    def length(self) -> int:
        return datatype_lenght(self.datatype)


ModbusRegisters = NewType("ModbusRegisters", List[ModbusRegister])

ModbusRegistersBatched = NewType(
    "ModbusRegistersBatched", List[List[ModbusRegister]]
)


@dataclass
class ModbusResult:
    tag: ModbusRegister
    value: any = None


ModbusResults = NewType("ModbusResults", List[ModbusResult])


# --------------------- FUNCTIONS ---------------------

# Interface to tag classes


@dataclass
class ObjectWithAddressAndBank:
    address: int
    memorybank: str
    length: int


# From a list of ObjectWithAddressAndBank classes, return the total lenght in memory addresses cosidering the length of each object

# TODO: Allow the use calculate batches which are not consecutive


def get_batch_memory_length(list: List[ObjectWithAddressAndBank]) -> int:
    return sum([tag.length for tag in list])


# From a list of {'name': 'variable_name', 'address': number} classes, return a list which contains lists of dictionaries which contain the dictionaries
# from the original list which have consecutive address numbers, with a maximum size of size.

# TODO: Allow the creation of batches which are not consecutive by an allowed non taged memory space


def make_batch_consecutive_bank_and_size(
    list: List[ObjectWithAddressAndBank],
    size: int,
) -> List[List]:
    # Check if size is greater than 2 to be able to make batches
    if size < 2:
        raise ValueError(
            "Is not possible to make batches with a size less than 2"
        )

    # Sort the list by address and memorybank
    list.sort(key=lambda x: x.address)
    list.sort(key=lambda x: x.memorybank)

    parts: List[List] = []

    if len(list) == 1:
        parts.append([list[0]])
        return parts

    # For loop that will iterate over list, creating batches of consecutive address and same memorybank value

    parts.append([list[0]])
    for i in range(1, len(list)):
        # Check that the address is not consecutive or the memorybank is not the same or if the batch is full, if so, create a new batch
        if (
            list[i].address != list[i - 1].address + list[i - 1].length
            or list[i].memorybank != list[i - 1].memorybank
            or len(parts[-1]) >= size
        ):
            parts.append([list[i]])

        # Otherwise, add the element to the last batch
        else:
            parts[-1].append(list[i])

    return parts
