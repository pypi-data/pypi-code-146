# encoding=utf-8
# Copyright (c) 2020-2021 Xie Ding <xdhum@126.com>
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
"""
This module Class for NOR Flash


"""
__author__ = "XieDing"

import logging
import math
from pathlib import Path

from pyftdi.spi import SpiPort
from .ftdispi import MyW25xNORSpiFlashDevice, SpiFlashError, SpiFlashRequestError

module_name = Path(__file__).stem

# from libs.mylog import mlog_color
# mlog = mlog_color(module_name, level='debug')

log_formatter = logging.Formatter(
    '[%(filename)s][%(funcName)s][%(levelname)s]: %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)
mlog = logging.getLogger(module_name)

mlog.setLevel(logging.DEBUG)  # setting log level
mlog.addHandler(stream_handler)


class _W25Q256JVFlashDevice(MyW25xNORSpiFlashDevice):
    """Winbond W25m flash device implementation"""

    support_flash_list = []
    JEDEC_ID_MATCH = False

    DEVICE_FAMILIY = 'W25Q256JV'
    device_info = "256M-Bit"
    NAND_NOR = "NOR"
    DEVICE_NAME = ""

    ManufacturerID = 0xEF  # MF7-MF0
    DeviceID = None  # ID15-ID0
    Memorytype_ID = None
    Capacity_ID = None
    JEDEC_ID = None
    # 2Gbit -- 2<<30 --
    # 1page=256B;
    # BLOCK可以是4K/32K/64K/
    PAGE_SIZE_BYTES = 256  # 256B
    BLOCK_DIV_PAGE = 256  # 按照64KB
    BLOCK_SIZE_BYTES = BLOCK_DIV_PAGE * PAGE_SIZE_BYTES  # 64KB = 65536B
    SECTOR_SIZE_BYTES = 4*1024
    SIZE_BYTES = 256 * 1024 * 1024
    SIZE_BITS = SIZE_BYTES * 8

    total_pages = int(SIZE_BYTES / PAGE_SIZE_BYTES)
    total_blocks = int(total_pages / BLOCK_DIV_PAGE)  # 512

    BYTE_NUM_BYTE_ADDR = 1
    BYTE_NUM_PAGE_ADDR = int(math.log2(total_pages)/8)+1

    SPI_FREQ_WRITE_MAX = 104e6  # MHz
    SPI_FREQ_WRITE_TYP = 50e6  # MHz
    SPI_FREQ_READ_MAX = 104e6  # MHz
    SPI_FREQ_READ_TYP = 50e6  # MHz

    # ----------------- Erase Commands -----------------
    CMD_ERASE_BLOCK = 0xD8  # 64KB
    CMD_ERASE_BLOCK_4BYTE_ADDR = 0xDC  # 64KB with 4B address
    CMD_ERASE_SECTOR4KB = 0x20
    CMD_ERASE_SECTOR4KB_4BYTE_ADDR = 0x21
    CMD_ERASE_BLOCK32KB = 0x52
    CMD_ERASE_BLOCK64KB = 0xD8
    CMD_ERASE_BLOCK64KB_4BYTE_ADDR = 0xDC

    # below is timing info for read/program/erase
    TIMINGS_PageProgram = (0.4e-3, 3e-3)  # 0.4ms, 3ms
    TIMINGS_PageRead = (30e-6, 60e-6)  # 30us, 60us very short time
    TIMINGS_BlockErase = (150e-3, 2000e-3)  # maybe very long time
    TIMINGS_ChipErase = (80, 400)  # 80s, 400s very long time
    TIMINGS_WriteStatusRegister = (10e-3, 15e-3)

    VALID_ADDRESS_MODE = ["3BYTE", "4BYTE"]  # 128Mb以下的，三字节寻址足够
    CURRENT_ADDRESS_MODE = "3BYTE"

    SECURITY_REG1_ADDR = 0xA0
    SECURITY_REG2_ADDR = 0xB0
    SECURITY_REG3_ADDR = 0xC0
    SR_ADDRS = [SECURITY_REG1_ADDR, SECURITY_REG2_ADDR, SECURITY_REG3_ADDR]

    STATUS_REG1_DES = ("SRP", "TB", "BP3", "BP2", "BP1", "BP0", "WEL", "BUSY")
    STATUS_REG2_DES = ("SUS", "CMP", "LB3", "LB2", "LB1", "--", "QE", "SRL")
    STATUS_REG3_DES = ("--", "DRV1", "DRV0", "--", "--", "WPS", "ADP", "ADS")
    STATUS_REG1_DEFAULT = (0, 0, 0, 0, 0, 0, 0, 0)
    STATUS_REG2_DEFAULT = (0, 0, 0, 0, 0, 0, 0, 0)
    STATUS_REG3_DEFAULT = (0, 0, 0, 0, 0, 0, 0, 0)
    # ---------------------------------------------------------------------------------------------------
    # If one NOR serial flash STATUS REG is different from below, it must be override in implementation
    # Protection Register(SR - 1) Volatile Writable, OTP lockable
    # ------------------------------------------------------------------------
    # STATUS REG1  |  S7  |  S6  |  S5  |  S4  |  S3  |  S2  |  S1  |  S0  |
    #              | SRP  |  TB  | BP3  | BP2  | BP1  | BP0  | WEL  | BUSY |

    # ------------------------------------------------------------------------
    # SR_SRP0 = 0b1000_0000  # S7

    SR_BIT_SRP = 0b1000_0000  # S7 -- STATUS REGISTER PROTECT
    SR_BIT_TBP = 0b0100_0000  # S6 top-bottom protect bit
    SR_BIT_BP3 = 0b0010_0000  # S5 bit protect #3
    SR_BIT_BP2 = 0b0001_0000  # S4 bit protect #2
    SR_BIT_BP1 = 0b0000_1000  # S3 bit protect #1
    SR_BIT_BP0 = 0b0000_0100  # S2 bit protect #0
    SR_BIT_WEL = 0b0000_0010  # S1 Write enable Latch bit
    SR_BIT_WIP = 0b0000_0001  # S0 Busy/Work-in-progress bit
    SR_BIT_BUSY = SR_BIT_WIP  # S0 Busy/Work-in-progress bit
    SR_PROTECT_NONE = 0  # BP[0..2] = 0
    # default values for the Block Protection bits are 1 after power up to protect the entire array
    SR_PROTECT_ALL = 0b0111_1100  # 没什么用，芯片掉电会自动全部写保护，不用手动写保护芯片
    # SR_UNLOCK_PROTECT = 0b1000_0011

    # Configuration Register (SR-2) (Volatile Writable)
    #        BIT   |   7  |  6  |  5  |  4  |  3  |  2  |  1 |  0  |
    # -------------------------------------------------------------------
    # STATUS REG2  |  S15 | S14 | S13 | S12 | S11 | S10 | S9 |  S8 |
    #              |  SUS | CMP | LB3 | LB2 | LB1 | --- | QE | SRL |
    # -------------------------------------------------------------------
    # SR_SUS = 0b1000_0000

    SR_BIT_SUS = 0b1000_0000  # SUSPEND STATUS
    SR_BIT_CMP = 0b0100_0000  # COMPLEMENT PROTECT, Volatile/Non-Volatile Writable, Default=0
    SR_BIT_LB3 = 0b0010_0000  # SECURITY REGISTER LOCK BITS, Non-Volatile OTP Writable
    SR_BIT_LB2 = 0b0001_0000  # SECURITY REGISTER LOCK BITS, Non-Volatile OTP Writable
    SR_BIT_LB1 = 0b0000_1000  # SECURITY REGISTER LOCK BITS, Non-Volatile OTP Writable
    SR_BIT_QE = 0b0000_0010  # QUAD ENABLE
    SR_BIT_SRL = 0b0000_0001  # STATUS REGISTER LOCK

    # Status Register (SR-3)
    #        BIT   |    7  |   6  |   5  |  4  |  3  |  2  |  1  |  0  |
    # ------------------------------------------------------------------
    # STATUS REG3  |  S15  |  S14 |  S13 | S12 | S11 | S10 |  S9 |  S8 |
    #              |  ---  | DRV1 | DEV0 | --- | --- | WPS | ADP | ADS |
    # ------------------------------------------------------------------
    # SR_WIP = 0b0000_0001  # S0 Busy/Work-in-progress bit
    SR_BIT_DRV1 = 0b0100_0000  # Output Driver Strength
    SR_BIT_DRV0 = 0b0010_0000  # S5
    SR_BIT_WP_E = 0b0000_0100
    SR_BIT_WPS = 0b0000_0100  # Write Protection Selection,
    SR_BIT_ADP = 0b0000_0010  # Non-Volatile Writable, default = 0
    # Current Address Mode (ADS) – Status Only; default-> 0 -> 3-Byte Address Mode, 1 -> 4-Byte
    SR_BIT_ADS = 0b0000_0001

    CMD_UID_READ = 0x4B
    UID_LEN = 0x8  # 8Byte - 64 bits
    UID_DUMMY_BYTES = 5  # 4 dummy bytes
    BBM_BYTE_NUM = 2  # 2 bytes BBM in spare area

    # def __init__(self, spiport: SpiPort = None, flash_name=None):
    #     super().__init__(spiport, flash_name)
    #     if flash_name is not None:
    #         self.DEVICE_NAME = flash_name
    #     if spiport is not None:
    #         self._spiport = spiport

    def __str__(self):
        return f'Winbond {self.DEVICE_FAMILIY} :{self.device_info} '

    def is_busy(self) -> bool:
        """Reports whether the flash may receive commands or is actually
           being performing internal work.

           :return: True if the device is busy and cannot accept new I/O
                    commands, False otherwise.
           """
        self.stauts_read_sr1()
        return self.STATUS_BUSY

    def stauts_read_sr1(self) -> int:
        """
        CMD = 0x05
        :return:
        """
        # _val = self._read_single_status_reg_tuple(self.CMD_READ_STATUS_REG1)
        _val = self._read_single_status_reg(self.CMD_READ_STATUS_REG1)
        # self.SR_SRP, self.SR_TBP, self.SR_BP3, self.SR_BP2, self.SR_BP1, self.SR_BP0, self.SR_WEL, self.SR_BUSY = _val
        sr_tb = self.SR_BIT_TBP | self.SR_BIT_BP3 | self.SR_BIT_BP2 | self.SR_BIT_BP1 | self.SR_BIT_BP0
        self.STATUS_WHOLE_ARRAY_UNPROTECT = ~bool(_val & sr_tb)
        self.STATUS_BUSY = bool(_val & self.SR_BIT_BUSY)
        return _val

    def stauts_read_sr2(self) -> int:
        # _val = self._read_single_status_reg_tuple(self.CMD_READ_STATUS_REG2)
        # self.SR_SUS, self.SR_CMP, self.SR_LB3, self.SR_LB2, self.SR_LB1, res2, self.SR_QE, self.SR_SRL = _val
        _val = self._read_single_status_reg(self.CMD_READ_STATUS_REG2)
        return _val

    def stauts_read_sr3(self) -> int:
        # _val = self._read_single_status_reg_tuple(self.CMD_READ_STATUS_REG3)
        # res7, self.SR_DRV1, self.SR_DRV0, res4, res3, self.SR_WPS, self.SR_ADP, self.SR_ADS = _val
        _val = self._read_single_status_reg(self.CMD_READ_STATUS_REG3)
        _tup = self.status_regval_int2tuple(_val)
        if bool(_val & self.SR_BIT_ADP):
            self.CURRENT_ADDRESS_MODE = "4BYTE"
        else:
            self.CURRENT_ADDRESS_MODE = "3BYTE"

        return _val

    def check_current_address_mode(self) -> None:
        self.stauts_read_sr3()

    def set_4byte_mode(self) -> None:
        if "4BYTE" in self.VALID_ADDRESS_MODE:
            self.check_current_address_mode()

            if self.CURRENT_ADDRESS_MODE == "3BYTE":
                reg3_val = self.stauts_read_sr3()
                regval = reg3_val | self.SR_BIT_ADP
                self.status_reg_write_enable()
                datain = bytes((self.CMD_WRITE_STATUS_REG3, regval,))
                self._spiport.exchange(datain)
                self._wait_for_completion(self.TIMINGS_WriteStatusRegister)
            elif self.CURRENT_ADDRESS_MODE == "4BYTE":
                pass
            else:
                raise ValueError(f'address mode:{self.CURRENT_ADDRESS_MODE} ?????')

            self.stauts_read_sr3()
            if self.CURRENT_ADDRESS_MODE != "4BYTE":
                raise ValueError("set 4BYTE mode fail, can't set ADP=1 in status reg3")
        else:
            mlog.info(f"valid mode:{self.VALID_ADDRESS_MODE} -- do't support 4Byte address mode")
        mlog.debug(f"CURRENT_ADDRESS_MODE:{self.CURRENT_ADDRESS_MODE}")

    def unlock(self) -> None:
        """
        NOR Flash is different from NAND Flash
        write Status Resister -1 with cmd=0x01
        be careful for this operation
        """

        self._write_enable()
        reg1_val = self.stauts_read_sr1()
        # sr_val = reg1_val & self.SR_UNLOCK_PROTECT
        sr_val = reg1_val & (~self.SR_PROTECT_ALL & 0xff)

        # sr_val = self.SR_PROTECT_NONE | self.SR_UNLOCK_PROTECT
        self.status_reg_write_enable()
        datain = bytes((self.CMD_READ_STATUS_REG1, sr_val))
        self._spiport.exchange(datain)

        duration = self.TIMINGS_WriteStatusRegister
        if any(duration):
            self._wait_for_completion(duration)
        self.status_read()
        if not self.STATUS_WHOLE_ARRAY_UNPROTECT:
            raise SpiFlashRequestError("Cannot unprotect flash device")

    def unique_id_read(self) -> int:
        """W25Q256x serial need 5 dummy bytes after cmd

           :return: the unique ID
        """
        # todo: add unique id read
        data_in = bytes([self.CMD_UID_READ] + [int(xx) for xx in "0"*self.UID_DUMMY_BYTES])
        unique_id = self._spiport.exchange(data_in, self.UID_LEN)
        return unique_id


class W25Q256JVxQFlashDevice(_W25Q256JVFlashDevice):
    """Winbond W25Q256 flash device implementation"""
    support_flash_list = [
        "W25Q256JVIQ",
        "W25Q256JVJQ",
    ]
    JEDEC_ID = 'EF4019'
    ManufacturerID = 0xEF  # MF7-MF0
    DeviceID = 0x4019  # ID15-ID0
    Memorytype_ID = '40'
    Capacity_ID = '19'

    STATUS_REG1_DEFAULT = (0, 0, 0, 0, 0, 0, 0, 0)
    STATUS_REG2_DEFAULT = (0, 0, 0, 0, 0, 0, 0, 0)
    STATUS_REG3_DEFAULT = (0, 1, 1, 0, 0, 0, 0, 0)

    # def __init__(self, spiport: SpiPort = None, flash_name=None):
    #     super().__init__(spiport, flash_name)
    #     if flash_name is not None:
    #         self.DEVICE_NAME = flash_name
    #     if spiport is not None:
    #         self._spiport = spiport


class W25Q256JVxNFlashDevice(_W25Q256JVFlashDevice):
    """Winbond W25Q256 flash device implementation"""
    support_flash_list = [
        "W25Q256JVIN",
    ]
    JEDEC_ID = 'EF4019'
    ManufacturerID = 0xEF  # MF7-MF0
    DeviceID = 0x4019  # ID15-ID0
    Memorytype_ID = '40'
    Capacity_ID = '19'

    STATUS_REG1_DEFAULT = (0, 0, 0, 0, 0, 0, 0, 0)
    STATUS_REG2_DEFAULT = (0, 0, 0, 0, 0, 0, 0, 0)
    STATUS_REG3_DEFAULT = (0, 0, 1, 0, 0, 0, 0, 0)


class W25Q256JVxMFlashDevice(_W25Q256JVFlashDevice):
    """Winbond W25Q256 flash device implementation"""

    support_flash_list = [
        "W25Q256JVIM",
        "W25Q256JVJM",
    ]
    JEDEC_ID = 'EF7019'
    ManufacturerID = 0xEF  # MF7-MF0
    DeviceID = 0x7019  # ID15-ID0
    Memorytype_ID = '70'
    Capacity_ID = '19'
