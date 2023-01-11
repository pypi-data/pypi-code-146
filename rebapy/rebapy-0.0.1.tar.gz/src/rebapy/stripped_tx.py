from enum import Enum
from typing import Optional
from abc import ABC, abstractmethod


class InputLenType(Enum):
    ZERO = 0
    ONE_BYTE = 1
    TWO_BYTES = 2
    INVALID = 3

    def as_num_bytes(self):
        if self is InputLenType.INVALID:
            return 0
        return self.value


class StrippedTxConfig(bytes):
    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls, *args, *kwargs)
        if len(self) != 1:
            raise ValueError(
                f"Value MUST be a single byte!  Found {len(self)}")
        return self

    @property
    def is_dyn_gas(self) -> bool:
        DYN_GAS_FLAG = 0x80
        return self[0] & DYN_GAS_FLAG

    @property
    def has_block_num(self) -> bool:
        BLOCK_NUM_FLAG = 0x40
        return self[0] & BLOCK_NUM_FLAG

    @property
    def input_len(self) -> InputLenType:
        INPUT_LEN_MASK = 0x30
        INPUT_LEN_INDEX = 4
        input_len = (self[0] & INPUT_LEN_MASK) >> INPUT_LEN_INDEX
        return InputLenType(input_len)

    @property
    def tx_version(self) -> int:
        return 1 if ((self[0] & 0x08) != 0) else 0

    def as_dict(self):
        return {
            "is_dyn_gas": self.is_dyn_gas,
            "has_block_num": self.has_block_num,
            "input_len": self.input_len.as_num_bytes(),
            "tx_version": self.tx_version
        }


class GasBase(ABC):
    @abstractmethod
    def as_dict(self):
        pass


class DynamicGas(GasBase):
    def __init__(self, max_fee_per_gas: int, max_priority_fee_per_gas: int):
        self.max_fee_per_gas = max_fee_per_gas
        self.max_priority_fee_per_gas = max_priority_fee_per_gas

    def as_dict(self):
        return {
            "max_fee_per_gas": self.max_fee_per_gas,
            "max_priority_fee_per_gas": self.max_priority_fee_per_gas
        }


class StaticGas(GasBase):
    def __init__(self, gas_price: int):
        self.gas_price = gas_price

    def as_dict(self):
        return {
            "gas_price": self.gas_price
        }


class StrippedTransaction:
    def __init__(self,
                 config: StrippedTxConfig,
                 hash: bytes,
                 from_address: bytes,
                 to_address: bytes,
                 value: int,
                 input: bytes,
                 gas: GasBase,
                 gas_limit: int,
                 block_number: Optional[int]):
        self.config = config

        if len(hash) != 32:
            raise ValueError(f"Expected len(hash)==32, found {len(hash)}")
        self.hash = hash

        if len(from_address) != 20:
            raise ValueError(
                f"Expected len(from_address)==20, found {len(from_address)}")
        self.from_address = from_address

        if len(to_address) != 20:
            raise ValueError(
                f"Expected len(to_address)==20, found {len(to_address)}")
        self.to_address = to_address

        self.value = value
        self.input = input
        self.gas = gas
        self.gas_limit = gas_limit
        self.block_number = block_number

    def as_dict(self):
        return {
            "config": self.config.as_dict(),
            "hash": '0x' + self.hash.hex(),
            "from": '0x' + self.from_address.hex(),
            "to": '0x' + self.to_address.hex(),
            "value": self.value,
            "input": '0x' + self.input.hex(),
            "gas_limit": self.gas_limit,
            "block_number": self.block_number,
            **self.gas.as_dict()
        }
