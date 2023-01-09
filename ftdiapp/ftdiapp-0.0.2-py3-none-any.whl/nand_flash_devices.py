# encoding=utf-8
# Copyright (c) 2020-2021 Xie Ding <xdhum@126.com>
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
"""
This Module
Supported NADN/NOR Spi Flash list:
1. Winbond: W25M02, W25Q64


"""
__author__ = "XieDing"

import math

from pyftdi.spi import SpiPort

from .ftdispi import (MyW25xNANDSpiFlashDevice, SpiFlashError, SpiFlashRequestError)


class _W25M02GVFlashDevice(MyW25xNANDSpiFlashDevice):
    """Winbond W25m flash device implementation"""

    support_flash_list = []
    JEDEC_ID_MATCH = False

    DEVICE_FAMILIY = 'W25M02GV'
    device_info = "2x1G-Bit"
    NAND_NOR = "NAND"
    DEVICE_NAME = ""

    JEDEC_ID = 'EFAB21'
    ManufacturerID = 0xEF  # MF7-MF0
    DeviceID = 0xAB21  # ID15-ID0
    Memorytype_ID = 'AB'
    Capacity_ID = '21'
    # 2Gbit -- 2<<30 --
    # 1page=2KB; 1 block = 64 pages = 128KB; 1G-bits = 1024 block
    SPARE_AREA_BYTES = 64
    PAGE_SIZE_BYTES = 2048
    BLOCK_DIV_PAGE = 64
    BLOCK_SIZE_BYTES = BLOCK_DIV_PAGE * PAGE_SIZE_BYTES
    SIZE_BITS = 2 * 1024 * 1024 * 1024
    SIZE_BYTES = int(SIZE_BITS / 8)

    total_pages = int(SIZE_BYTES / PAGE_SIZE_BYTES)
    total_blocks = int(total_pages / BLOCK_DIV_PAGE)

    BYTE_NUM_BYTE_ADDR = 2
    BYTE_NUM_PAGE_ADDR = 3

    SPI_FREQ_WRITE_MAX = 104e6  # MHz
    SPI_FREQ_WRITE_TYP = 50e6  # MHz
    SPI_FREQ_READ_MAX = 104e6  # MHz
    SPI_FREQ_READ_TYP = 50e6  # MHz

    # below is timing info for read/program/erase
    TIMINGS_PageProgram = (250e-6, 700e-6)  # 250uS, 700us
    TIMINGS_PageRead = (30e-6, 60e-6)  # 30us, 60us very short time
    TIMINGS_BlockErase = (2e-3, 10e-3)  # maybe very long time
    # TIMINGS_ChipErase = (1, 1)
    TIMINGS_WriteStatusRegister = (10e-6, 10e-6)

    # -------- Stata register relative parameters --------
    STATUS_REG1_ADDR = 0xA0
    STATUS_REG2_ADDR = 0xB0
    STATUS_REG3_ADDR = 0xC0
    SR_ADDRS = [STATUS_REG1_ADDR, STATUS_REG2_ADDR, STATUS_REG3_ADDR]

    STATUS_REG1_DES = ("SRP0", "BP3", "BP2", "BP1", "BP0", "TB", "WP_E", "SRP1")
    STATUS_REG2_DES = ("OTP_L", "OTP_E", "SR1_L", "ECC_E", "BUF", "--", "--", "--")
    STATUS_REG3_DES = ("--", "LUT_F", "ECC1", "ECC0", "PFAIL", "EFAIL", "WEL", "BUSY")
    STATUS_REG1_DEFAULT = (0, 0, 0, 0, 0, 0, 0, 0)
    STATUS_REG2_DEFAULT = (0, 0, 0, 0, 0, 0, 0, 0)
    STATUS_REG3_DEFAULT = (0, 0, 0, 0, 0, 0, 0, 0)

    # ---------------------------------------------------------------------------------------------------
    # If one NAND serial flash STATUS REG is different from below, it must be override in implementation
    # Protection Register(SR - 1) Volatile Writable, OTP lockable
    # ----------------------------------------------------------------
    # STATUS REG1  |  S7  |  S6 |  S5 |  S4 |  S3 | S2 |  S1  |  S0  |
    #              | SRP0 | BP3 | BP2 | BP1 | BP0 | TB | WP-E | SRP1 |
    # ----------------------------------------------------------------
    SR_BIT_SRP0 = 0b1000_0000  # S7
    SR_BIT_BP3 = 0b0100_0000  # S6 bit protect #3
    SR_BIT_BP2 = 0b0010_0000  # bit protect #2
    SR_BIT_BP1 = 0b0001_0000  # bit protect #1
    SR_BIT_BP0 = 0b0000_1000  # bit protect #0
    SR_BIT_TBP = 0b0000_0100  # top-bottom protect bit
    SR_BIT_WP_E = 0b0000_0010
    SR_BIT_SRP1 = 0b0000_0001

    SR_PROTECT_NONE = 0  # BP[0..2] = 0
    # default values for the Block Protection bits are 1 after power up to protect the entire array
    SR_PROTECT_ALL = 0b0111_1100  # 没什么用，芯片掉电会自动全部写保护，不用手动写保护芯片
    # SR_UNLOCK_PROTECT = 0b1000_0011

    # Configuration Register (SR-2) (Volatile Writable)
    # ------------------------------------------------------------------------
    # STATUS REG2  |  S7   |   S6  |   S5  |   S4  |  S3 | S2  |  S1  |  S0  |
    #              | OTP-L | OTP-E | SR1-L | ECC-E | BUF | --- | ---  |  --- |
    # ------------------------------------------------------------------------
    SR_BIT_OTPL = 0b1000_0000
    SR_BIT_OTPE = 0b0100_0000
    SR_BIT_SR1L = 0b0010_0000
    SR_BIT_ECCE = 0b0001_0000
    SR_BIT_BUF = 0b0000_1000

    SR_ECCE_BIT = 4
    SR_BUF_BIT = 3
    BUF_MODE = None
    # Status Register (SR-3) (Status Only)
    # ----------------------------------------------------------------------------
    # STATUS REG3  |   S7  |    S6 |   S5  |   S4  |   S3   |   S2  |  S1 |  S0  |
    #              |  ---  | LUT-F | ECC-1 | ECC-0 | P-FAIL | E-FAIL| WEL | BUSY |
    # ----------------------------------------------------------------------------
    SR_BIT_LUTF = 0b0100_0000  # S6
    SR_BIT_ECC1 = 0b0010_0000  # S5
    SR_BIT_ECC0 = 0b0001_0000  # S4
    SR_BIT_PFAIL = 0b0000_1000  # S3
    SR_BIT_EFAIL = 0b0000_0100  # S2
    SR_BIT_WEL = 0b0000_0010  # S1 Write enable Latch bit
    SR_BIT_WIP = 0b0000_0001  # S0 Busy/Work-in-progress bit
    SR_BIT_BUSY = SR_BIT_WIP  # S0 Busy/Work-in-progress bit

    CMD_READ_UID = 0x4B
    UID_LEN = 0x8  # 64 bits
    READ_UID_WIDTH = 4  # 4 dummy bytes
    BBM_BYTE_NUM = 2  # 2 bytes BBM in spare area

    def __init__(self, spiport: SpiPort = None, flash_name=None):
        super().__init__(spiport, flash_name)
        if flash_name is not None:
            self.DEVICE_NAME = flash_name
        if spiport is not None:
            self._spiport = spiport

    def __str__(self):
        return f'Winbond {self.DEVICE_FAMILIY} :{self.device_info} '

    def realized_from_spiport(self, spiport: SpiPort):
        self._spiport = spiport

    def set_buffer_mode(self):

        self._write_enable()
        sr2_val = (1 << self.SR_ECCE_BIT) | (1 << self.SR_BUF_BIT)
        datain = bytes((self.CMD_WRSR, self.STATUS_REG2_ADDR, sr2_val))
        self._spiport.exchange(datain)
        duration = self.TIMINGS_WriteStatusRegister
        if any(duration):
            self._wait_for_completion(duration)
        self.stauts_read_sr2()
        if not self.is_buffer_read_mode():
            raise SpiFlashError

    def stauts_read_sr1(self):
        _val = self._read_single_status_reg(self.CMD_READ_STATUS, self.SR_ADDRS[0])

        sr_tb = self.SR_BIT_TBP | self.SR_BIT_BP3 | self.SR_BIT_BP2 | self.SR_BIT_BP1 | self.SR_BIT_BP0
        self.STATUS_WHOLE_ARRAY_UNPROTECT = ~bool(_val & sr_tb)
        return _val

    def stauts_read_sr2(self):
        _val = self._read_single_status_reg(self.CMD_READ_STATUS, self.SR_ADDRS[1])
        # BUF=1 -- Buffer read mode
        self.BUF_MODE = bool(_val & self.SR_BIT_BUF)
        return _val

    def stauts_read_sr3(self):
        _val = self._read_single_status_reg(self.CMD_READ_STATUS, self.SR_ADDRS[2])
        self.STATUS_BUSY = bool(_val & self.SR_BIT_BUSY)

        return _val

    def unlock(self) -> None:
        """
        write Status Resister -1 with cmd=0x01
        be careful for this operation
        """

        self._write_enable()
        sr_addr = self.SR_ADDRS[0]
        reg1_val = self.stauts_read_sr1()

        sr_val = reg1_val & (~self.SR_PROTECT_ALL & 0xff)
        datain = bytes((self.CMD_WRSR, sr_addr, sr_val))
        self._spiport.exchange(datain)
        # duration = self.get_timings('lock')
        duration = self.TIMINGS_WriteStatusRegister
        if any(duration):
            self._wait_for_completion(duration)
        self.status_read()
        if not self.STATUS_WHOLE_ARRAY_UNPROTECT:
            raise SpiFlashRequestError("Cannot unprotect flash device")


class W25M02GVxxIGFlashDevice(_W25M02GVFlashDevice):
    support_flash_list = ["W25M02GVxxIG"]
    STATUS_REG2_DES = ("OTP_L", "OTP_E", "SR1_L", "ECC_E", "BUF", "--", "--", "--")
    # Default BUF=1
    STATUS_REG2_DEFAULT = (0, 0, 0, 0, 1, 0, 0, 0)


class W25M02GVxxITFlashDevice(_W25M02GVFlashDevice):
    support_flash_list = ["W25M02GVxxIT"]

    # Default BUF=0
    STATUS_REG2_DEFAULT = (0, 0, 0, 0, 0, 0, 0, 0)

