# encoding=utf-8
# Copyright (c) 2020-2021 Xie Ding <xdhum@126.com>
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
"""
This module is used for SPI with based on pyftdi
 include 3 parts
1. realize FTDI-SPIPort -- for spi debug based on command mode
2. realize FTDI-SPIGPIO -- control GPIO with xDBUS
3. SpiFlash Operation -- NAND/NOR

Supported NADN/NOR Spi Flash list:
1. Winbond: W25M02, W25Q64

Available interfaces:
  ftdi://ftdi:2232:2:4/1   (Dual RS232-HS)
  ftdi://ftdi:2232:2:4/2   (Dual RS232-HS)

"""
__author__ = "XieDing"

import logging
import math
import os
import sys
import time

from pathlib import Path
from typing import Iterable, Optional, Tuple, Union, List

from pyftdi.eeprom import FtdiEeprom
from pyftdi.misc import hexdump
from pyftdi.ftdi import Ftdi
from pyftdi.spi import SpiController, SpiPort
from pyftdi.usbtools import UsbTools

module_name = Path(__file__).stem


log_formatter = logging.Formatter(
    '[%(filename)s][%(funcName)s][%(levelname)s]: %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)
mlog = logging.getLogger(module_name)

mlog.setLevel(logging.DEBUG)  # setting log level
mlog.addHandler(stream_handler)


def finding_ftdi_urls()->list:
    UsbTools.flush_cache()
    devices = Ftdi.list_devices()

    dev_tup_strs = UsbTools.build_dev_strings('ftdi', Ftdi.VENDOR_IDS,
                                              Ftdi.PRODUCT_IDS, devices)
    _urls = [tem[0] for tem in dev_tup_strs]
    return _urls


def finding_ftdi_desc_urls() -> dict:
    ftdi_dict = {}
    UsbTools.flush_cache()
    devices = Ftdi.list_devices()

    for _device in devices:
        usb_desc = _device[0].description
        usb_sn = _device[0].sn
        usb_vid = _device[0].vid
        usb_pid = _device[0].pid
    dev_tup_strs = UsbTools.build_dev_strings('ftdi', Ftdi.VENDOR_IDS,
                                              Ftdi.PRODUCT_IDS, devices)
    for tupx in dev_tup_strs:
        _url = tupx[0]
        _desc = tupx[1].replace("(", "").replace(")", "")
        if _desc not in ftdi_dict:
            ftdi_dict[_desc] = []
        if _url not in ftdi_dict[_desc]:
            ftdi_dict[_desc].append(_url)

    _urls = [tem[0] for tem in dev_tup_strs]
    [mlog.debug(xx) for xx in _urls]
    return ftdi_dict


def get_ftdieeprom_from_url(ftdi_url: str) -> FtdiEeprom:
    # Instantiate an EEPROM manager
    eeprom = FtdiEeprom()
    # Select the FTDI device to access (the interface is mandatory but any
    eeprom.open(ftdi_url)
    return eeprom


def ftdi_read_eeprom_data(ftdi_url: str):
    # Instantiate an EEPROM manager
    eeprom = FtdiEeprom()
    eeprom.open(ftdi_url)
    eeprom.dump_config()
    romdata = hexdump(eeprom.data)
    return romdata


def get_ftdi_spicontroller(ftdi_url: str) -> SpiController:
    spictrl = SpiController()
    spictrl.configure(ftdi_url)
    return spictrl


def get_ftdi_spiport_from_spictrl(spictrl, spi_freq, cs=0, mode=0) -> SpiPort:
    spi_port = spictrl.get_port(cs=cs, freq=spi_freq, mode=mode)
    return spi_port


def get_ftdi_spiport_from_url(ftdi_url, spi_freq, cs=0, mode=0) -> SpiPort:
    spictrl = SpiController()
    spictrl.configure(ftdi_url)
    if spi_freq >= 30e6:
        mlog.warning(
            f"Note: FTDI SPI can only support slower than 30MHZ, it's better to set to 10/20MHz"
        )
    spi_port = spictrl.get_port(cs=cs, freq=spi_freq, mode=mode)
    return spi_port


def realize_ftdi_gpio(spictrl):
    spigpio = spictrl.get_gpio()
    return spigpio


class _MyFtdiSpiCtrl:
    """Interface of a generic FTDI spi device"""

    def __init__(self):
        self.spictrl = None
        self.spiport = None
        self.spigpio = None
        self.spiflash = None
        self.spi_freq = 0

    def is_configed(self):
        if self.spictrl is not None and self.spictrl.configured:
            return True
        else:
            return False

    def terminate(self):
        if self.is_configed():
            self.spictrl.terminate()

    def realize_from_spicontroller(self,
                                   spictrl: SpiController,
                                   spi_freq: int,
                                   cs=0,
                                   mode=0) -> None:
        raise NotImplementedError

    def realize_from_url(self, ftdi_url, spi_freq, cs=0, mode=0) -> None:
        raise NotImplementedError


class MyFtdiSpiPort(_MyFtdiSpiCtrl):
    """
    realized as SPI port, always be Master
    """

    def realize_from_spicontroller(self,
                                   spictrl: SpiController,
                                   spi_freq: int,
                                   cs=0,
                                   mode=0) -> None:
        self.spictrl = spictrl
        self.spiport = self.spictrl.get_port(cs=cs, freq=spi_freq, mode=mode)
        if spi_freq > 30e6:
            mlog.warning(
                f"Note: FTDI SPI can only support slower than 30MHZ, it's better to set to 10/20MHz"
            )

    def realize_from_url(self, ftdi_url, spi_freq, cs=0, mode=0) -> None:
        self.spictrl = SpiController()
        self.spictrl.configure(ftdi_url)
        self.spiport = self.spictrl.get_port(cs=cs, freq=spi_freq, mode=mode)

    def get_port(self):
        return self.spiport

    def set_spi_frequency(self, spi_freq):
        self.spiport.set_frequency(spi_freq)

    def spi_data_trans(self, write_buf):

        if isinstance(write_buf, bytes):
            data_in = write_buf
        elif isinstance(write_buf, bytearray):
            data_in = write_buf
        elif isinstance(write_buf, str):
            write_buf = write_buf.replace("0x", "").replace("_", "")
            data_in = bytes.fromhex(write_buf)
        elif isinstance(write_buf, int):
            data_in = bytes((write_buf,))
        else:
            raise NotImplementedError

        read_buf = self.spiport.exchange(data_in, duplex=True)
        hex_str = read_buf.hex()
        lens = len(read_buf)
        read_int_list = [hex_str[i * 2:2 * i + 2] for i in range(lens)]
        return read_int_list


class MyFtdiSpiGPIO(_MyFtdiSpiCtrl):
    """
    realize GPIO with FTDISPI, currently only support CBUS
    """

    def realize_from_spicontroller(self,
                                   spictrl: SpiController,
                                   spi_freq,
                                   cs=0,
                                   mode=0) -> None:
        self.spictrl = spictrl
        self.spigpio = spictrl.get_gpio()
        self.gpio_cbus_set_all_input()

    def realize_from_url(self, ftdi_url: str, spi_freq, cs=0, mode=0) -> None:
        self.spictrl = SpiController()
        self.spictrl.configure(ftdi_url)
        self.spigpio = self.spictrl.get_gpio()
        self.gpio_cbus_set_all_input()

    def disable_cbus(self):
        self.spigpio.set_direction(0x0000, 0x0000)

    def gpio_cbus_set_all_input(self):
        self.spigpio.set_direction(0xff00, 0x0000)

    def gpio_cbus_set_all_output(self):
        self.spigpio.set_direction(0xff00, 0xff00)

    def gpio_cbus_setdir(self, pins: int, direction: int):
        """
        A logical 0 bit represents an input pin
        Args:
            pins: 1-> config
            direction: 0->input, 1->output

        Returns: None

        """
        self.spigpio.set_direction(pins & 0xff00, direction & 0xff00)

    def gpio_cbus_getdir(self) -> tuple:
        """修改返回值"""
        pindir_int = self.spigpio.direction & 0xff00
        pindir = f"{pindir_int:016b}"
        return pindir_int, pindir

    def gpio_cbus_setval(self, pinvals: int):
        """
        Args:
            pinvals: 0-> low, 1->high

        Returns: None

        """
        pinvals &= 0xff00
        self.spigpio.write(pinvals)

    def gpio_cbus_getval(self) -> tuple:
        """修改返回值为元组"""
        pinvals_int = self.spigpio.read()
        pinvals = f"{pinvals_int:016b}"
        return pinvals_int, pinvals


class SpiFlashError(Exception):
    """Base class for all Spi Flash errors"""
    _fmt = 'SpiFlash Base Error'  #: format string

    def __init__(self, msg=None, **kw):
        """Initialize the Exception with the given message.
        """
        self.msg = msg
        for key, value in kw.items():
            setattr(self, key, value)

    def __str__(self):
        """Return the message in this Exception."""
        if self.msg:
            return self.msg
        try:
            return self._fmt % self.__dict__
        except (NameError, ValueError, KeyError):
            e = sys.exc_info()[1]  # current exception
            return f'Unprintable exception {repr(e)}: {str(e)}'


class SpiFlashNotSupported(SpiFlashError):
    """Exception thrown when a non-existing feature is invoked"""


class SerialFlashJedecMismatch(SpiFlashNotSupported):
    """Exception thrown when JEDEC ID readout from flash not match the given device"""


class SpiFlashTimeout(SpiFlashError):
    """Exception thrown when a flash command cannot be completed in a timelymanner"""


class SpiFlashValueError(SpiFlashError):
    """Exception thrown when a parameter is out of range"""
    _fmt = 'SpiFlash out of range'  #: format string


class SpiFlashContentVerifyError(SpiFlashError):
    """Exception thrown when a parameter is out of range"""
    _fmt = "Content Verify Fail"


class SpiFlashRequestError(SpiFlashError):
    """Cannot complete a flash device request"""


# def get_flash_class(ftdi_spiport: SpiPort, flash_name: str):
def get_flash_class(flash_name: str) -> Union['MyW25xNANDSpiFlashDevice', 'MyW25xNORSpiFlashDevice']:
    flash_classes = []
    _flash_modules = ["ftdiapp.nand_flash_devices", "ftdiapp.nor_flash_devices"]

    for _module in _flash_modules:
        contents = sys.modules[_module].__dict__
        # 找到类名以FlashDevice结束的类
        for name in contents:
            if name.endswith('FlashDevice') and not name.startswith('_'):
                flash_classes.append(contents[name])
        for flash_class in flash_classes:
            xx = flash_class.support_flash_list
            if flash_name in xx:
                mlog.info(f"{flash_name} -- {flash_class}")
                return flash_class(flash_name)

    raise SpiFlashError('No serial flash detected')


def get_flash_classname_from_flash_name(flash_name: str) -> str:
    """
    本模块定制化的功能
    :param flash_name:
    :return:
    """
    # _module = __name__
    _flash_modules = ["ftdiapp.nand_flash_devices", "ftdiapp.nor_flash_devices"]

    # contents = sys.modules[__name__].__dict__
    for _module in _flash_modules:
        contents = sys.modules[_module].__dict__
        # 找到类名以FlashDevice结束的类
        for name in contents:
            if name.endswith('FlashDevice') and not name.startswith('_'):
                flash_class = contents[name]
                class_name = name
                xx = flash_class.support_flash_list
                if flash_name in flash_class.support_flash_list:
                    mlog.info(f"{flash_name} -- class_name{class_name} -> {flash_class}")
                    return class_name

    raise SpiFlashError('No serial flash detected')


def read_binfile2bytes(binfile) -> Union[bytes, bytearray]:
    file_size = os.path.getsize(binfile)
    with open(binfile, 'rb') as fr:
        bytes_data = fr.read(file_size)
    return bytes_data


class _MySpiFlashIF:
    """Interface of a generic SPI flash device
    定义一些串口Flash的通用接口操作,本类不包含具体的实现:
    """

    # FEAT_NONE = 0x000  # No special feature
    # FEAT_LOCK = 0x001  # Basic, revertable locking
    # FEAT_INVLOCK = 0x002  # Inverted (bottom/top) locking
    # FEAT_SECTLOCK = 0x004  # Arbitrary sector locking
    # FEAT_OTPLOCK = 0x008  # OTP locking available
    # FEAT_UNIQUEID = 0x010  # Unique ID
    # FEAT_SECTERASE = 0x100  # Can erase whole sectors
    # FEAT_HSECTERASE = 0x200  # Can erase half sectors
    # FEAT_SUBSECTERASE = 0x400  # Can erase sub sectors
    # FEAT_CHIPERASE = 0x800  # Can erase full chip
    FEAT_NONE = None  # No special feature
    FEAT_LOCK = None  # Basic, revertable locking
    FEAT_INVLOCK = None  # Inverted (bottom/top) locking
    FEAT_SECTLOCK = None  # Arbitrary sector locking
    FEAT_OTPLOCK = None  # OTP locking available
    FEAT_UNIQUEID = None  # Unique ID
    FEAT_SECTORERASE = None  # Can erase whole sectors
    FEAT_BLOCKERASE = None  # Can erase sub sectors
    FEAT_CHIPERASE = None  # Can erase full chip

    def set_spi_frequency(self, freq: Optional[float] = None) -> None:
        """Set the SPI bus frequency to communicate with the device. Set
           default SPI frequency if none is provided."""
        raise NotImplementedError()

    def _check_page_address_boundary(self,
                                     page_addr: int,
                                     page_nums: int = 0) -> None:
        """Verifies that a defined page area are valid on the flash device.
           It does not take into account any locking scheme, only the area
           boundary.

           :param page_addr: the position of the first page/block
           :param page_nums: the count of page/block

           :return True: if not exceed boundary
        """
        raise NotImplementedError()

    def _ftdi_spiport_exchange_data(self, data_in: [int],
                                    read_bytes: int) -> bytes:
        raise NotImplementedError

    # ------------------------- ID operation ---------------------------------
    def jedec_id_read(self) -> bytes:
        raise NotImplementedError

    def unique_id_read(self) -> int:
        """Return the unique ID of the flash, if it exists.

           :return: the unique ID
        """
        raise NotImplementedError()

    @classmethod
    def match_jedec(cls, jedec: Union[bytes, bytearray,
                                      Iterable[int]]) -> bool:
        """Tells whether this class support this JEDEC identifier.

           :param jedec: device type as a sequence of bytes
           :return: True if the current class supports the detected device.
        """
        raise NotImplementedError()

    # ------------------------- Status Register operation ---------------------------------
    def status_read(self) -> None:
        raise NotImplementedError

    def unlock(self) -> None:
        """Make the whole device read/write.

           Some flash devices are write-locked at power up.
        """
        raise NotImplementedError()

    def is_busy(self) -> bool:
        """Reports whether the flash may receive commands or is actually
           being performing internal work.

           :return: True if the device is busy and cannot accept new I/O
                    commands, False otherwise.
           """
        raise NotImplementedError()

    # ------------------------- read operation ---------------------------------
    def _read_lo_speed(self, data_addr: int = 0, lens: int = 1) -> bytes:
        """
        Read=03H, NAND/NOR flash 读取的时候有差异，最好放在具体的芯片层级再具体实现
        Args:
            data_addr:
            lens:

        Returns:

        """
        raise NotImplementedError

    def _read_hi_speed(self, data_addr: int = 0, lens: int = 1) -> bytes:
        """
        Fast Read=0BH
        Args:
            data_addr:
            lens:

        Returns:

        """
        raise NotImplementedError

    def read_pages(self,
                   addr: int,
                   page_nums=1,
                   spare_area=False) -> List[bytes or bytearray]:
        """Read page data from the specified address.
            the count of bytes to read depends on page size due to each flash
           :param addr: the position of the first byte to read
           :param page_nums: pages of data to read
           :param spare_area: NOR flash do not have this feature
           :return: an array of bytes
        """
        raise NotImplementedError()

    # ------------------------- write/program operation ---------------------------------
    def _write_enable(self) -> None:
        """enable write operation, common cmd for all serial flash NAND/NOR"""
        raise NotImplementedError

    def _write_disable(self) -> None:
        """disable write operation, common cmd for all serial flash NAND/NOR"""
        raise NotImplementedError

    def program_single_page(self,
                            page_addr: int,
                            data: Union[bytes, bytearray, Iterable[int]],
                            data_addr: int = 0,
                            verify: bool = False):
        """
        write single page data

        Args:
            page_addr:
            data: should be less than page size, if exceeded will be ignored
            data_addr: data to be written may not be from 00 of a page
            verify: if True, read out page data to verify if data were correctly programed

        Returns:

        """
        raise NotImplementedError

    def program_pages(self,
                      page_addr: int,
                      data: Union[bytes, bytearray, Iterable[int]],
                      data_addr: int = 0,
                      verify: bool = False):
        """
        continueous program data based on page
        Args:
            page_addr:
            data:
            data_addr:
            verify:

        Returns:

        """
        raise NotImplementedError

    # ------------------------- erase operation ---------------------------------
    def erase_single_block(self, page_addr: int, verify: bool = False) -> None:
        """Erase a block of bytes.

           Address and length depends upon device-specific constraints and
           should be aligned on device blocks.

           As a special feature, specifying address as 0 and length to -1
           triggers a full chip erase.

           :param page_addr: the position of the first byte to erase
           :param verify: optionally check that the selected blocks have been
                          erased, reading them back.
        """
        raise NotImplementedError()

    def erase_chip(self, verify: bool = False) -> None:
        """Erase whole chip.
           :param verify: optionally check that the selected blocks have been
                          erased, reading them back.
        """
        raise NotImplementedError()

    def _verify_page_content(
            self, page_addr: int, refdata: Union[bytes, bytearray,
                                                 Iterable[int]]) -> None:
        raise NotImplementedError

    def _wait_for_completion(self, times: Tuple[float, float]) -> None:
        """
        wait program/erase operation done
        Args:
            times: tuple of typical and maximum times for program/erase operation

        Returns: None

        """
        raise NotImplementedError


class MyGenericSpiFlashDevice(_MySpiFlashIF):
    """Generic flash device implementation.
    这里做通用串口Flash的实现
    注意：FTDISPI的数据缓冲区，貌似是不到64K，所以按照page来读取数据，问题不大。
    在这里实现大部分的功能
    """

    # 这里会被重写，列出来所支持的FLASH 型号。
    support_flash_list = []
    DEVICE_FAMILIY = ""
    device_info = ""
    NAND_NOR = ""
    DEVICE_NAME = ""
    # define common command for all serial flash
    CMD_JEDEC_ID = 0x9F
    CMD_READ_LO_SPEED = 0x03  # Read @ low speed
    CMD_READ_HI_SPEED = 0x0B  # Read @ high speed -- may not be used

    CMD_WRITE_ENABLE = 0x06  # Write enable
    CMD_WRITE_DISABLE = 0x04  # Write disable

    # below is device info, should be overriden in concrete implementation
    JEDEC_ID_MATCH = False
    JEDEC_ID = ''  # common
    ManufacturerID = 666  # MF7-MF0
    DeviceID = 666666  # ID15-ID0
    Memorytype_ID = ''
    Capacity_ID = ''
    # device page--block--total
    SPARE_AREA_BYTES = 0
    PAGE_SIZE_BYTES = 1  # initial value, very very large
    SECTOR_SIZE_BYTES = 0
    BLOCK_DIV_PAGE = 0
    BLOCK_SIZE_BYTES = BLOCK_DIV_PAGE * PAGE_SIZE_BYTES
    SECTOR_4KB_BYTES = 0
    SIZE_BITS = 0
    SIZE_BYTES = 0
    total_pages = 0
    total_blocks = 0

    BYTE_NUM_BYTE_ADDR = 0
    BYTE_NUM_PAGE_ADDR = 0

    # NAND Flash can support up to 104MHz for all instructions
    # NOR flash spi freq may be different for read, due to vcc voltage
    SPI_FREQ_READ_MAX = 0  # Hz
    SPI_FREQ_READ_TYP = 0  # Hz
    SPI_FREQ_WRITE_MAX = 0  # Hz
    SPI_FREQ_WRITE_TYP = 0  # Hz
    # below is timing info for read/program/erase -- tuple(typ,max) unit:S
    # Nor flash is much slower than NAND flash
    # these values must be override with serial flash device implementation

    TIMINGS_PageProgram = (1e-3, 10e-3)  #
    TIMINGS_PageRead = (1E-3, 100e-3)  # very short time
    TIMINGS_BlockErase = (1e-3, 100e-3)  # maybe very long time
    TIMINGS_ChipErase = (1, 1)
    TIMINGS_WriteStatusRegister = (1, 1)

    # define status

    STATUS_BUSY = None
    STATUS_WRITE_ENABLE = None
    STATUS_WHOLE_ARRAY_UNPROTECT = None

    def __init__(self):
        """
        init with ftdi-spiport to operator with serial flash
        """
        self._spiport = None

    def realized_from_spiport(self, spiport: SpiPort):
        self._spiport = spiport

    def set_spi_frequency(self, freq: Optional[int] = None) -> None:
        """
        common method for all serial flash
        Args:
            freq: FTDI spi port frequency with Unit:Hz

        Returns: None
        """
        default_freq = self.SPI_FREQ_READ_TYP  # select slowest frequency for read/write operation

        _freq = min(default_freq, freq) if freq else default_freq
        if _freq > 20e6:
            _freq = 20e6
            mlog.warning(
                f"FTDI can support SPI freq_max=30MHz, here set to lower than 20MHz"
            )
        self._spiport.set_frequency(_freq)

    def _check_page_address_boundary(self,
                                     page_addr: int,
                                     page_nums: int = 1) -> None:
        """Verifies that a defined page area are valid on the flash device.
           It does not take into account any locking scheme, only the area
           boundary.

           :param page_addr: the position of the first page/block
           :param page_nums: the count of page/block
           :return True: if not exceed boundary
        """
        if page_addr + (page_nums - 1) * self.PAGE_SIZE_BYTES > self.SIZE_BYTES:
            raise SpiFlashValueError('Out of range')

    def _ftdi_spiport_exchange_data(self, data_in, out_bytes=0) -> bytes:
        """
        Read data with dummy cycles
            cmd + dummy byte cycles + data read
        """
        # jedec_id = self._spiport.exchange(jedec_cmd, 3).hex().upper()
        data_read = self._spiport.exchange(bytes(data_in), out_bytes)
        return data_read

    # ------------------------- Status Register operation ---------------------------------
    def status_read(self) -> tuple:
        sr1 = self.stauts_read_sr1()
        sr2 = self.stauts_read_sr2()
        sr3 = self.stauts_read_sr3()
        return sr1, sr2, sr3

    def stauts_read_sr1(self) -> int:
        raise NotImplementedError

    def stauts_read_sr2(self) -> int:
        raise NotImplementedError

    def stauts_read_sr3(self) -> int:
        raise NotImplementedError

    # should be Implemented on NAND/NOR flash level
    def unlock(self) -> None:
        """Make the whole device read/write.

           Some flash devices are write-locked at power up.
        """
        raise NotImplementedError()

    # should be Implemented on NAND/NOR flash level or dedicate device level
    def is_busy(self) -> bool:
        """Reports whether the flash may receive commands or is actually
           being performing internal work.

           :return: True if the device is busy and cannot accept new I/O
                    commands, False otherwise.
           """
        raise NotImplementedError

    # ------------------------- ID operation ---------------------------------
    def jedec_id_read(self) -> bytes:
        """
        Read nand flash device JEDEC identifier (3 bytes)
        ------------------------------------------------------
        | Commands | OpCode | Byte2 | Byte3  | Byte4 | Byte5 |
        | JEDEC ID |   9Fh  | Dummy | ManuID |   Device ID   |
        ------------------------------------------------------
        Read nor flash device JEDEC identifier (3 bytes)
        ----------------------------------------------
        | Commands | OpCode |  Byte2 | Byte3 | Byte4 |
        | JEDEC ID |   9Fh  | ManuID |   Device ID   |
        ----------------------------------------------
        """
        # how to judge dummy cycle???
        # data_in = [self.CMD_JEDEC_ID]
        # data_in.extend([0] * dummy_bytes)
        # jedec_cmd = bytes(data_in)
        # # jedec_id = self._spiport.exchange(jedec_cmd, 3).hex().upper()
        # jedec_id = self._spiport.exchange(jedec_cmd, 3)
        # return jedec_id
        # NOR flash don't need dummy byte
        data_in = (self.CMD_JEDEC_ID,)
        return self._ftdi_spiport_exchange_data(data_in, 3)

    def unique_id_read(self) -> int:
        """Return the unique ID of the flash, if it exists.

           :return: the unique ID
        """
        raise NotImplementedError()

    def match_jedec(self, jedec: Union[bytes, bytearray,
                                       Iterable[int]]) -> bool:
        """Tells whether this class support this JEDEC identifier"""
        # manufacturer, device, capacity = jedec[:3]
        jedec_id_read = jedec[:3].hex().upper()
        if jedec_id_read != self.JEDEC_ID:
            self.JEDEC_ID_MATCH = False
            mlog.error(
                f"JEDEC_ID don't match! {self.DEVICE_NAME} ID {self.JEDEC_ID} -> read: {jedec_id_read}"
            )
        else:
            self.JEDEC_ID_MATCH = True
            mlog.info(
                f"{self.DEVICE_NAME} JEDEC_ID match! ID: {self.JEDEC_ID} -> read: {jedec_id_read}"
            )
        return self.JEDEC_ID_MATCH

    # ------------------------- read operation ---------------------------------
    def _read_lo_speed(self, data_addr: int = 0, lens: int = 1) -> bytes:
        """
        Read=03H, NAND/NOR flash 读取的时候有差异，最好放在具体的芯片层级再具体实现
        Args:
            data_addr:
            lens:

        Returns:

        """
        raise NotImplementedError

    def _read_hi_speed(self, data_addr: int = 0, lens: int = 1) -> bytes:
        """
        Fast Read=0BH
        Args:
            data_addr:
            lens:

        Returns:

        """
        raise NotImplementedError

    def format_page_data(self, page_idx, page_data: Union[bytes, bytearray]) -> list:
        N1 = 16
        data_len = len(page_data)
        if data_len > self.PAGE_SIZE_BYTES:
            raise ValueError("Data larger than 1 page.")
        num1 = int(data_len / N1)
        num2 = data_len % N1
        w1 = self.BYTE_NUM_PAGE_ADDR * 2
        w2 = self.BYTE_NUM_BYTE_ADDR * 2
        Address = "Address".rjust(w1 + w2, ' ')
        data_list = [
            f"Page Data:{page_idx}",
            f" {Address} | 00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f",
            f"---------------------------------------------------------------"
        ]
        page_str = f"{page_idx:0{w1}x}"
        for idx in range(num1):
            list1 = [
                f"{tem:02x}" for tem in page_data[idx * N1:(idx + 1) * N1]
            ]
            str1 = f"{page_str} {idx * 16:0{w2}x} | {' '.join(list1)}"
            data_list.append(str1)
        if num2 > 0:
            list2 = [f"{tem:02x} " for tem in page_data[N1 * num1:]]
            str2 = " ".join(list2)
            data_list.append(f"{page_str} {num1 * 16:0{w2}x} | {str2}")
        data_list.append(
            f"---------------------------------------------------------------")
        [mlog.debug(xx) for xx in data_list]
        return data_list

    def read_pages(self,
                   addr: int,
                   page_nums=1,
                   spare_area=False) -> List[bytes or bytearray]:
        """
        read data for given page address
        """
        raise NotImplementedError

    # ------------------------- write/program operation ---------------------------------
    def _write_enable(self) -> None:
        wirte_enable_cmd = bytes((self.CMD_WRITE_ENABLE,))
        self._spiport.exchange(wirte_enable_cmd)

    def _write_disable(self) -> None:
        write_disable_cmd = bytes((self.CMD_WRITE_DISABLE,))
        self._spiport.exchange(write_disable_cmd)

    def program_single_page(self,
                            page_addr: int,
                            data: Union[bytes, bytearray, Iterable[int]],
                            data_addr: int = 0,
                            verify: bool = False) -> None:
        """
        write single page data

        Args:
            page_addr:
            data: should be less than page size, if exceeded will be ignored
            data_addr: data to be written may not be from 00 of a page
            verify: if True, read out page data to verify if data were correctly programed

        Returns:

        """
        raise NotImplementedError

    def program_pages(self,
                      page_addr: int,
                      data: Union[bytes, bytearray, Iterable[int]],
                      data_addr: int = 0,
                      verify: bool = False) -> None:
        """
        continuous program data based on page
        Args:
            page_addr:
            data:
            data_addr:
            verify:

        Returns:

        """
        raise NotImplementedError

    # ------------------------- erase operation ---------------------------------
    def erase_single_block(self, page_addr: int, verify: bool = False) -> None:
        """Erase a block of bytes.
            should be implemented due to each device
        """
        raise NotImplementedError()

    # should be Implemented on NAND/NOR flash level
    def erase_chip(self, verify=False) -> None:
        """in pyseialflash it is implemented as Erase sectors/blocks/chip of a "generic" flash device.
            here, I redefine this method:
            For NOR  flash: chip_erase -- 0xC7 -- dedicate command
            for NAND flash: block erase for all the blocks(maybe not used, for nand flash capacity is too large)
        """
        raise NotImplementedError

    def _verify_page_content(
            self, page_addr: int, refdata: Union[bytes, bytearray,
                                                 Iterable[int]]) -> None:
        data = self.read_pages(page_addr)[0]
        mlog.debug(f"ref  data:{refdata.hex()}")
        lens_ref = len(refdata)
        if lens_ref < self.PAGE_SIZE_BYTES:
            data = data[0:lens_ref]
        mlog.debug(f"read data:{data.hex()}")
        if data != refdata:
            raise SpiFlashContentVerifyError

    def _wait_for_completion(self, times: Tuple[float, float]) -> None:
        typical_time, max_time = times
        timeout = time.time()
        timeout += typical_time + max_time
        cycle = 0
        while self.is_busy():
            # need to wait at least once
            if cycle and time.time() > timeout:
                raise SpiFlashTimeout(f'Command timeout ({cycle} cycles)')
            time.sleep(typical_time)
            cycle += 1

    def _data_to_page_data_list(self, datain: Union[bytes, bytearray, Iterable[int]]) -> List[bytes or bytearray]:
        """
        数据分页
        :param datain:
        :return:
        """
        page_size = self.PAGE_SIZE_BYTES
        data_lens = len(datain)
        page_nums = int(data_lens / page_size)
        part_page_bytes = data_lens % page_size
        page_data_list = []
        for page_idx in range(page_nums):
            page_data = datain[page_idx * page_size:(page_idx + 1) * page_size]
            page_data_list.append(page_data)
        if part_page_bytes > 0:
            page_data = datain[page_nums * page_size:]
            page_data_list.append(page_data)
        return page_data_list


class MyW25xNANDSpiFlashDevice(MyGenericSpiFlashDevice):
    """Generic NAND flash device implementation
        based on for 'W25x' series.
        Note: only add implementation for NAND(not NOR)
    """

    READ_MODES = ("Continuous Read", "Buffer Read")
    SR_ADDRS = [0, 0, 0]  # should be override in dedicate nand flash implementation

    STATUS_REG1_ADDR = None
    STATUS_REG2_ADDR = None
    STATUS_REG3_ADDR = None
    STATUS_REG1_DES = ("--", "--", "--", "--", "--", "--", "--", "--")
    STATUS_REG2_DES = ("--", "--", "--", "--", "--", "--", "--", "--")
    STATUS_REG3_DES = ("--", "--", "--", "--", "--", "--", "--", "--")
    STATUS_REG1_DEFAULT = (0, 0, 0, 0, 0, 0, 0, 0)
    STATUS_REG2_DEFAULT = (0, 0, 0, 0, 0, 0, 0, 0)
    STATUS_REG3_DEFAULT = (0, 0, 0, 0, 0, 0, 0, 0)

    BUF_MODE = None
    # Common command for all nand serial flash
    CMD_WRSR = 0x01  # Write status register

    CMD_PAGE_DATA_READ = 0x13
    CMD_READ_STATUS = 0x05  # Read status register
    # for page program
    CMD_PAGE_PROGRAM_DATA_LOAD = 0x02
    CMD_PROGRAM_EXECUTE = 0x10

    CMD_ERASE_BLOCK = 0xD8
    BBM_BYTE_NUM = None
    # timings for read/program/erase
    TIMINGS_PageProgram = (1e-3, 10e-3)  #
    TIMINGS_PageRead = (1E-3, 100e-3)  # very short time
    TIMINGS_BlockErase = (1e-3, 100e-3)  # maybe very long time
    TIMINGS_WriteStatusRegister = (1, 1)

    def __init__(self, spiport: SpiPort = None, flash_name=None):
        super().__init__()
        if flash_name is not None:
            self.DEVICE_NAME = flash_name
        if spiport is not None:
            self._spiport = spiport
            # todo: automatically detect buffer mode or continueous read mode???
            # self.set_buffer_mode()

    def __len__(self):
        return self.SIZE_BYTES

    def realized_from_spiport(self, spiport: SpiPort):
        self._spiport = spiport

    def is_busy(self) -> bool:
        """Reports whether the flash may receive commands or is actually
           being performing internal work.

           :return: True if the device is busy and cannot accept new I/O
                    commands, False otherwise.
           """
        # return self._check_busy_bit(self._read_status())
        self.stauts_read_sr3()
        return self.STATUS_BUSY

    def is_buffer_read_mode(self) -> bool:
        """
        this is only for NAND flash,
        with buffer mode, we can read out spare area data: BBM, ECC, ...
        Returns: bool: Ture indicate buffer mode

        """
        self.stauts_read_sr2()
        return self.BUF_MODE

    def set_buffer_mode(self):
        raise NotImplementedError

    def jedec_id_read(self) -> bytes:
        """
        Read nand flash device JEDEC identifier (3 bytes)
        ------------------------------------------------------
        | Commands | OpCode | Byte2 | Byte3  | Byte4 | Byte5 |
        | JEDEC ID |   9Fh  | Dummy | ManuID |   Device ID   |
        ------------------------------------------------------
        """
        # how to judge dummy cycle???
        # data_in = [self.CMD_JEDEC_ID]
        # data_in.extend([0] * dummy_bytes)
        # jedec_cmd = bytes(data_in)
        # # jedec_id = self._spiport.exchange(jedec_cmd, 3).hex().upper()
        # jedec_id = self._spiport.exchange(jedec_cmd, 3)
        # return jedec_id
        data_in = (self.CMD_JEDEC_ID, 0)
        return self._ftdi_spiport_exchange_data(data_in, 3)

    def unique_id_read(self) -> int:
        """Return the unique ID of the flash, if it exists.

           :return: the unique ID
        """
        # todo: add unique id read
        mlog.warning("unique_id_read to be updated")
        unique_id = 0
        return unique_id

    def _load_page_data_to_read(self, addr: int):

        pa15_8 = addr >> 8
        pa7_0 = addr & 0xff
        datain = bytes((self.CMD_PAGE_DATA_READ, 0, pa15_8, pa7_0))
        self._spiport.exchange(datain, 0)
        # wait_time = self.TIMINGS["PageRead"][1]

        wait_time = self.TIMINGS_PageRead[1]
        time.sleep(wait_time)

    def _read_lo_speed(self, data_addr: int = 0, lens: int = 1) -> bytes:
        """
        for NAND serial flash, read with cmd=0x03, data format like below:
        |OpCode |  Byte2  |  Byte3 | Byte4 | Byte5 |Byte6  | ... |
        | 0x03  | addr_H  | addr_L | dummy | data0 | data1 | ... |
        Args:
            data_addr:
            lens:

        Returns:

        """
        # todo: to judge buffer mode or continueous read mode?????
        _data_in = bytes((self.CMD_READ_LO_SPEED, (data_addr >> 8) & 0xff,
                          data_addr & 0xff, 0))
        return self._spiport.exchange(_data_in, lens)

    def _read_hi_speed(self, data_addr: int = 0, lens: int = 1) -> bytes:
        read_cmd = bytes((self.CMD_READ_HI_SPEED, (data_addr >> 16) & 0xff,
                          (data_addr >> 8) & 0xff, data_addr & 0xff, 0))
        return self._spiport.exchange(read_cmd, lens)

    def read_pages(self,
                   addr: int,
                   page_nums=1,
                   spare_area=False) -> List[bytes or bytearray]:
        """
        read data of one or more pages from given page address
        Note:
            1. by default, only read one page data
            2. read without Spare Area: BBM, ECC, ...
        """

        read_bytes_num = self.PAGE_SIZE_BYTES
        if spare_area:
            read_bytes_num += self.SPARE_AREA_BYTES

        self._check_page_address_boundary(addr, page_nums)
        pages_data = []

        # 查看当前状态寄存器
        if not self.is_buffer_read_mode():
            # todo: 后面增加功能，修改BUF mode
            raise Exception(NotImplementedError,
                            f"必须以BUF mode进行操作，需要更新设置BUF=1")

        for page_idx in range(page_nums):
            page_addr = addr + page_idx
            # load page data
            self._load_page_data_to_read(page_addr)
            # read page data
            # _page_data = self._read_hi_speed(addr, _page_size)
            _page_data = self._read_lo_speed(0, read_bytes_num)
            pages_data.append(_page_data)
            mlog.debug(f"addr:{page_addr} page_data:{_page_data}")
        return pages_data

    def read_bbm_single_page(self, page_addr: int) -> Tuple[bool, str]:
        """
        read BBM(Bad Block Marker) info of given page address
        1. only page0 of each block
        2. if BBM of page0 is bad, then the whole block is abandoned
        Args:
            page_addr: 16-bit
        Returns:

        """
        # todo: 确定其他型号的NAND Flash是不是也是两个字节的BBM
        bad_page_flag = False
        if self.BBM_BYTE_NUM is None:
            raise ValueError(
                f"please define BBM Bytes Number of {self.DEVICE_NAME}")
        else:
            bbm_bytes = self.BBM_BYTE_NUM
        # check boundary
        if page_addr >= self.total_pages:
            raise SpiFlashValueError

        # 查看当前状态寄存器
        if not self.is_buffer_read_mode():
            self.set_buffer_mode()

        # calculate block address
        pa_block1 = (page_addr >> 6) & 0x3ff
        block_idx = int(page_addr / self.BLOCK_DIV_PAGE)
        page_offset = 0

        block_page0_addr = block_idx * self.BLOCK_DIV_PAGE
        self._load_page_data_to_read(block_page0_addr)
        data_addr_offset = self.PAGE_SIZE_BYTES
        marker_val = self._read_lo_speed(data_addr_offset,
                                         bbm_bytes).hex().upper()
        mlog.debug(f"addr:{page_addr} -- block[{block_idx}] BBM:{marker_val}")

        expected_marker = "FF" * bbm_bytes
        if expected_marker != marker_val:
            bad_page_flag = True
        return bad_page_flag, marker_val

    def read_bbms_all(self) -> List[int]:
        """
        check whole flash BBM
        Returns:

        """
        bad_block_addrs = []
        for block_addr in range(self.total_pages):
            page_addr = block_addr * self.BLOCK_DIV_PAGE
            bbm_val = self.read_bbm_single_page(page_addr)
            if bbm_val != "FFFF":
                bad_block_addrs.append(page_addr)
        return bad_block_addrs

    def write_bbm_block(self):
        raise NotImplementedError

    def unlock(self) -> None:
        """
        NOR Flash is different from NAND Flash
        write Status Resister -1 with cmd=0x01
        be careful for this operation
        """
        raise NotImplementedError

    def _page_program_data_load(self,
                                data: Union[bytes, bytearray, Iterable[int]],
                                addr=0) -> None:

        _data_in = bytes((self.CMD_PAGE_PROGRAM_DATA_LOAD,
                          (addr >> 8) & 0xff, addr & 0xff)) + bytes(data)
        self._spiport.exchange(_data_in, 0)
        self._wait_for_completion(self.TIMINGS_PageRead)

    def _program_execute(self, page_addr: int):
        _data_in = bytes((self.CMD_PROGRAM_EXECUTE, 0, (page_addr >> 8) & 0xff,
                          page_addr & 0xff))
        self._spiport.exchange(_data_in, 0)
        self._wait_for_completion(self.TIMINGS_PageProgram)

    def program_single_page(self,
                            page_addr: int,
                            data: Union[bytes, bytearray, Iterable[int]],
                            data_addr: int = 0,
                            verify: bool = False):
        """
        write single page data

        Args:
            page_addr:
            data: should be less than page size, if exceeded will be ignored
            data_addr: data to be written may not be from 00 of a page
            verify: if True, read out page data to verify if data were correctly programed

        Returns:

        """

        # step0 check BBM
        bad_page_flag, marker_val = self.read_bbm_single_page(page_addr)
        if bad_page_flag:
            mlog.warning(f"Page:{page_addr} is BAD, makerVal={marker_val}")
            return None
        if len(data) > self.PAGE_SIZE_BYTES:
            mlog.warning(
                f"program_single_page: data lens shouldn't larger than Page Size "
            )
            return None
        if data_addr > 0:
            raise Exception(
                NotImplementedError,
                f"don't support part page program! data_addr should be 0")
        # step1 write enable
        self._write_enable()
        # step2 program data load
        # todo:??block里面的page可以随机写入，不用必须从PAGE0开始写入
        # 在本版本中，page program 允许随机页地址编程？？？
        # 貌似micro的NAND 在一个块以内，页必须从一个块的页最低位到这个块的页的最高位连续编程，禁止随机页地址的编程。
        self._page_program_data_load(data, data_addr)
        # step3 program execute
        self._program_execute(page_addr)
        # step4 wait for completion
        self._wait_for_completion(self.TIMINGS_PageProgram)
        if verify:
            self._verify_page_content(page_addr, data)

    def program_pages(self,
                      page_addr: int,
                      data: Union[bytes, bytearray, Iterable[int]],
                      data_addr: int = 0,
                      verify: bool = True):
        """
        实现策略:
        1. 通过给定的页地址换算出所处的块位置
        2. 读取给定换算出来的块的坏块信息(BBM)
        3. 如果当前块是坏块，则顺延一个块进行写操作

        Args:
            page_addr:
            data: should be less than page size, if exceeded will be ignored
            data_addr: data to be written may not be from 00 of a page
            verify: if True, read out page data to verify if data were correctly programed

        Returns:

        """
        if data_addr != 0:
            raise NotImplementedError("Currently only support page program from beginning of each page")
        # todo: 数据分段 data
        page_data_list = self._data_to_page_data_list(data)

        # program single page data
        # check block???
        for page_data in page_data_list:
            self.program_single_page(page_addr, page_data, verify=verify)
            page_addr += 1

        return None

    # overrided in MyGenericNANDSpiFlashDevice

    def stauts_read_sr1(self) -> int:
        raise NotImplementedError

    def stauts_read_sr2(self) -> int:
        raise NotImplementedError

    def stauts_read_sr3(self) -> int:
        raise NotImplementedError

    def _read_single_status_reg(self, cmd: int, sr_addr: int) -> int:
        """
        NAND serial flash has only 1 cmd to read status reg, but with 3 REG address
        # Read Status Register 0Fh / 05h
        # --------------------------------------------
        # | OpCode |  Byte2  | Byte3 | Byte4 | Byte5 |
        # |   05H  | SR Addr |  S7-0 |  S7-0 |  S7-0 |
        # --------------------------------------------
        Returns:
        """
        read_cmd = bytes((cmd, sr_addr))

        reg_bytes = self._spiport.exchange(read_cmd, 1)
        if len(reg_bytes) != 1:
            raise SpiFlashTimeout("Unable to retrieve flash status")
        reg_int = int(reg_bytes.hex(), 16)
        return reg_int

    def _read_single_status_reg_tuple(self, cmd: int, sr_addr: int) -> tuple:
        """
        NAND serial flash has only 1 cmd to read status reg, but with 3 REG address
        # Read Status Register 0Fh / 05h
        # --------------------------------------------
        # | OpCode |  Byte2  | Byte3 | Byte4 | Byte5 |
        # |   05H  | SR Addr |  S7-0 |  S7-0 |  S7-0 |
        # --------------------------------------------
        Returns:
        """
        reg_int = self._read_single_status_reg(cmd, sr_addr)
        _tup = tuple(list(f"{reg_int:08b}"))
        return _tup

    def erase_single_block(self, page_addr: int, verify: bool = False) -> None:
        """
        erase the whole block which include the given page address,
        Args:
            page_addr: any page in the block to be ereased.
            verify:

        Returns:

        """
        # step1 enable write
        block_idx = page_addr / self.BLOCK_DIV_PAGE
        # block_idx = page_addr / self.PAGE_SIZE_BYTES
        if block_idx > self.total_blocks - 1:
            raise SpiFlashValueError
        mlog.debug(
            f"page address={page_addr} --> Block[{block_idx}] in whole chip")
        self._write_enable()
        page_addr_h = (page_addr >> 8) & 0xff
        page_addr_l = page_addr & 0xff
        datain = bytes((self.CMD_ERASE_BLOCK, 0, page_addr_h, page_addr_l))
        self._ftdi_spiport_exchange_data(datain, 0)
        # step3 wait for complete
        self._wait_for_completion(self.TIMINGS_BlockErase)
        # time.sleep(1)

    def erase_chip(self, verify=False) -> None:
        """in pyseialflash it is implemented as Erase sectors/blocks/chip of a "generic" flash device.
            for NAND flash: block erase for all the blocks(maybe not used, for nand flash capacity is too large)
        """
        for block_idx in range(self.total_blocks):
            page_addr = block_idx + self.BLOCK_DIV_PAGE
            self.erase_single_block(page_addr)


# class W25M02GVFlashDevice(MyGenericNANDSpiFlashDevice):
#     """Winbond W25m flash device implementation"""
#
#     support_flash_list = [
#         "W25M02GVxxIT",
#         "W25M02GVxxIG",
#     ]
#     JEDEC_ID_MATCH = False
#
#     DEVICE_FAMILIY = 'W25M02GV'
#     device_info = "2x1G-Bit"
#     NAND_NOR = "NAND"
#     DEVICE_NAME = ""
#
#     JEDEC_ID = 'EFAB21'
#     ManufacturerID = 0xEF  # MF7-MF0
#     DeviceID = 0xAB21  # ID15-ID0
#     Memorytype_ID = 'AB'
#     Capacity_ID = '21'
#     # 2Gbit -- 2<<30 --
#     # 1page=2KB; 1 block = 64 pages = 128KB; 1G-bits = 1024 block
#     SPARE_AREA_BYTES = 64
#     PAGE_SIZE_BYTES = 2048
#     BLOCK_DIV_PAGE = 64
#     BLOCK_SIZE_BYTES = BLOCK_DIV_PAGE * PAGE_SIZE_BYTES
#     SIZE_BITS = 2 * 1024 * 1024 * 1024
#     SIZE_BYTES = int(SIZE_BITS / 8)
#
#     total_pages = int(SIZE_BYTES / PAGE_SIZE_BYTES)
#     total_blocks = int(total_pages / BLOCK_DIV_PAGE)
#
#     SPI_FREQ_WRITE_MAX = 104e6  # MHz
#     SPI_FREQ_WRITE_TYP = 50e6  # MHz
#     SPI_FREQ_READ_MAX = 104e6  # MHz
#     SPI_FREQ_READ_TYP = 50e6  # MHz
#
#     # below is timing info for read/program/erase
#     TIMINGS_PageProgram = (250e-6, 700e-6)  # 250uS, 700us
#     TIMINGS_PageRead = (30e-6, 60e-6)  # 30us, 60us very short time
#     TIMINGS_BlockErase = (2e-3, 10e-3)  # maybe very long time
#     # TIMINGS_ChipErase = (1, 1)
#     TIMINGS_WriteStatusRegister = (10e-6, 10e-6)
#
#     SR1_ADDR = 0xA0
#     SR2_ADDR = 0xB0
#     SR3_ADDR = 0xC0
#     SR_ADDRS = [SR1_ADDR, SR2_ADDR, SR3_ADDR]
#
#     CMD_READ_UID = 0x4B
#     UID_LEN = 0x8  # 64 bits
#     READ_UID_WIDTH = 4  # 4 dummy bytes
#     BBM_BYTE_NUM = 2  # 2 bytes BBM in spare area
#
#     def __init__(self, spiport: SpiPort = None, flash_name=None):
#         super().__init__(spiport, flash_name)
#         if flash_name is not None:
#             self.DEVICE_NAME = flash_name
#         if spiport is not None:
#             self._spiport = spiport
#
#     def __str__(self):
#         return f'Winbond {self.DEVICE_FAMILIY} :{self.device_info} '
#
#     def realized_from_spiport(self, spiport: SpiPort):
#         self._spiport = spiport
#
#     def set_buffer_mode(self):
#
#         self._write_enable()
#         sr2_val = (1 << self.SR_ECCE_BIT) | (1 << self.SR_BUF_BIT)
#         datain = bytes((self.CMD_WRSR, self.SR2_ADDR, sr2_val))
#         self._spiport.exchange(datain)
#         duration = self.TIMINGS_WriteStatusRegister
#         if any(duration):
#             self._wait_for_completion(duration)
#         self.stauts_read_sr2()
#         if not self.is_buffer_read_mode():
#             raise SpiFlashError


class MyW25xNORSpiFlashDevice(MyGenericSpiFlashDevice):
    """Generic W25x Serials NOR flash device implementation
        based on for 'W25Q' series.
        Note: 1. only add implementation for NOR
              2. Currently don't support Security Register operation
              3. NOR flash的写保护有两种模式：
                <a> WPS=0,由状态寄存器位：SEC,TB,BP1,BP2,BP3的组合来实现
                <b> WPS=1,由特定的指令来实现lock/unlock
    """

    # No READ_MODES -- "Continuous Read", "Buffer Read"
    # No status reg address
    # 128M以下的，和256MB以上的也有差异，在具体的系列里面实例化，指定寄存器的细节
    STATUS_REG1_DES = ("--", "--", "--", "--", "--", "--", "--", "--")
    STATUS_REG2_DES = ("--", "--", "--", "--", "--", "--", "--", "--")
    STATUS_REG3_DES = ("--", "--", "--", "--", "--", "--", "--", "--")
    STATUS_REG1_DEFAULT = (0, 0, 0, 0, 0, 0, 0, 0)
    STATUS_REG2_DEFAULT = (0, 0, 0, 0, 0, 0, 0, 0)
    STATUS_REG3_DEFAULT = (0, 0, 0, 0, 0, 0, 0, 0)

    # Common command for all nand serial flash
    # CMD_WRSR = 0x01  # Write status register
    CMD_READ_STATUS_REG1 = 0x05
    CMD_READ_STATUS_REG2 = 0x35
    CMD_READ_STATUS_REG3 = 0x15

    CMD_WRITE_STATUS_EN = 0x50
    CMD_WRITE_STATUS_REG1 = 0x01
    CMD_WRITE_STATUS_REG2 = 0x31
    CMD_WRITE_STATUS_REG3 = 0x11

    VALID_ADDRESS_MODE = []  # 128Mb以下的，三字节寻址足够
    CURRENT_ADDRESS_MODE = "3BYTE"
    # ---------------- for page program -------------------
    # CMD_PAGE_PROGRAM_DATA_LOAD = None
    # CMD_PROGRAM_EXECUTE = None
    CMD_READ_LO_SPEED = 0x03  # Read @ low speed
    CMD_PAGE_DATA_READ = 0x03
    CMD_PAGE_DATA_READ_4BYTE_ADDR = 0x13
    CMD_PAGE_PROGRAM = 0x02
    CMD_PAGE_PROGRAM_4BYTE_ADDR = 0x12

    # ----------------- Erase Commands -----------------

    CMD_ERASE_SECTOR4KB = 0x20
    CMD_ERASE_SECTOR4KB_4BYTE_ADDR = 0x21

    CMD_ERASE_BLOCK32KB = 0x52

    CMD_ERASE_BLOCK64KB = 0xD8
    CMD_ERASE_BLOCK64KB_4BYTE_ADDR = 0xDC

    CMD_ERASE_BLOCK = 0xD8  # 64KB
    CMD_ERASE_BLOCK_4BYTE_ADDR = 0xDC  # 64KB with 4B address

    CMD_ERASE_CHIP = 0xC7  # or 0x60

    CMD_UID_READ = None
    UID_LEN = None  # 8Byte - 64 bits
    UID_DUMMY_BYTES = None  # 4 dummy bytes

    # timings for read/program/erase
    TIMINGS_PageProgram = (0, 0)  #
    TIMINGS_PageRead = (0, 0)  # very short time
    TIMINGS_BlockErase = (0, 0)  # maybe very long time
    TIMINGS_ChipErase = (0, 0)
    TIMINGS_WriteStatusRegister = (0, 0)

    def __init__(self, spiport: SpiPort = None, flash_name=None):
        super().__init__()
        if flash_name is not None:
            self.DEVICE_NAME = flash_name
        if isinstance(spiport, SpiPort):
            self._spiport = spiport
            if self.VALID_ADDRESS_MODE:
                self.set_4byte_mode()

    def __len__(self):
        return self.SIZE_BYTES

    def realized_from_spiport(self, spiport: SpiPort):
        """
        如果当前的Flash支持4Byte地址访问模式，那么默认切换
        :param spiport:
        :return:
        """
        self._spiport = spiport
        if self.VALID_ADDRESS_MODE:
            self.set_4byte_mode()

    def is_busy(self) -> bool:
        """Reports whether the flash may receive commands or is actually
           being performing internal work.

           :return: True if the device is busy and cannot accept new I/O
                    commands, False otherwise.
           """
        raise NotImplementedError

    def jedec_id_read(self) -> bytes:
        """
        Read nor flash device JEDEC ID (3 bytes), without dummy bytes
        ------------------------------------------------------
        | Commands | OpCode | Byte3  | Byte4 | Byte5 |
        | JEDEC ID |   9Fh  | ManuID |   Device ID   |
        ------------------------------------------------------
        """

        # jedec_id = self._spiport.exchange(jedec_cmd, 3).hex().upper()
        data_in = bytes((self.CMD_JEDEC_ID,))
        return self._spiport.exchange(data_in, 3)

    def unique_id_read(self) -> int:
        """不同容量的Flash需要的dummy 字节数不一样，在子类中实现

           :return: the unique ID
        """
        # todo: add unique id read
        raise NotImplementedError

    def _read_lo_speed(self, byte_addr: int = 0, lens: int = 1) -> bytes:
        """
        for NAND serial flash, read with cmd=0x03, data format like below:
        |OpCode |  Byte2  |  Byte3 | Byte4 | Byte5 |Byte6  | ... |
        | 0x03  | addr_H  | addr_L | dummy | data0 | data1 | ... |
        Args:
            byte_addr:
            lens:

        Returns:

        """
        # todo: to judge buffer mode or continuous read mode?????
        # _data_in = bytes((self.CMD_READ_LO_SPEED, (byte_addr >> 8) & 0xff, byte_addr & 0xff, 0))
        if byte_addr + lens > self.SIZE_BYTES:
            raise SpiFlashValueError
        byte_addr = self.__adress_int_to_bytes(byte_addr)
        if self.CURRENT_ADDRESS_MODE == "4BYTE":
            _data_in = bytes((self.CMD_PAGE_DATA_READ_4BYTE_ADDR,)) + byte_addr
        else:
            _data_in = bytes((self.CMD_READ_LO_SPEED,)) + byte_addr

        return self._spiport.exchange(_data_in, lens)

    def _read_hi_speed(self, byte_addr: int = 0, lens: int = 1) -> bytes:
        # read_cmd = bytes((self.CMD_READ_HI_SPEED, (data_addr >> 16) & 0xff,
        #                   (data_addr >> 8) & 0xff, data_addr & 0xff, 0))
        byte_addr = self.__adress_int_to_bytes(byte_addr)
        _data_in = bytes((self.CMD_READ_LO_SPEED,)) + byte_addr
        return self._spiport.exchange(_data_in, lens)

    def read_data_with_byte_addr(self, byte_addr: int, byte_nums: int = 1):
        return self._read_lo_speed(byte_addr, byte_nums)

    def read_pages(self, start_page_idx: int, page_nums=1, spare_area=False) -> List[bytes or bytearray]:
        """
        read data of one or more pages from given page address

        Note:
            1. by default, only read one page data
            2. NOR flash do not have Spare Area: BBM, ECC, ...,

        """

        read_bytes_num = self.PAGE_SIZE_BYTES
        if spare_area:
            read_bytes_num += self.SPARE_AREA_BYTES

        self._check_page_address_boundary(start_page_idx, page_nums)
        pages_data = []

        for _idx in range(page_nums):
            byte_addr = (start_page_idx + _idx) * self.PAGE_SIZE_BYTES
            _page_data = self._read_lo_speed(byte_addr, read_bytes_num)
            pages_data.append(_page_data)
            # mlog.debug(f"addr:{page_addr} page_data:{_page_data}")
        return pages_data

    def unlock(self) -> None:
        """
        NOR Flash is different from NAND Flash
        write Status Resister -1 with cmd=0x01
        be careful with this operation
        """
        raise NotImplementedError

    def check_current_address_mode(self) -> None:
        raise NotImplementedError

    def set_4byte_mode(self) -> None:
        raise NotImplementedError

    def _page_program_byteaddr_data(self, cmd: int, byte_addr: int, data: Union[bytes, bytearray, Iterable[int]]):
        """
        rule1: 字节地址从每一个页的起始地址开始，而且数据长度不超过页的字节数
        rule2： 字节地址非起始地址，则写入的数据长度不能超过剩余的页内字节数
        :param cmd: dedicate page program command:02h/12h
        :param byte_addr:
        :param data:
        :return:
        """
        # page_idx = int(byte_addr / self.PAGE_SIZE_BYTES)
        data_lens = len(data)
        if self.CURRENT_ADDRESS_MODE == "3BYTE":
            addr_byte_num = 3
        elif self.CURRENT_ADDRESS_MODE == "4BYTE":
            addr_byte_num = 3
        else:
            raise NotImplementedError("CURRENT_ADDR currently only support 3/4Bytes")

        if data_lens > self.PAGE_SIZE_BYTES:
            raise ValueError("写入的数据长度超过页大小")
        # judge page start address
        if byte_addr & 0xff > 0:  # page start address
            offset_addr = byte_addr & 0xff
            if data_lens > self.PAGE_SIZE_BYTES - offset_addr:
                addr_wid = addr_byte_num * 2
                raise ValueError(f"byte_addr:{byte_addr:#0{addr_wid + 2}x}页内非起始地址，写入数据长度超过页内剩余空间")

        # xxx = bytes([(byte_addr >> 8 * (addr_byte_num - idx - 1)) & 0xff for idx in range(addr_byte_num)])
        addr_bytes = self.__adress_int_to_bytes(byte_addr)
        if isinstance(data, list):
            data_bytes = bytes(data)
        else:
            data_bytes = data
        _data_in = bytes((cmd,)) + addr_bytes + data_bytes
        self._spiport.exchange(_data_in)
        return None

    def program_single_page(self, page_addr: int, data: Union[bytes, bytearray, Iterable[int]],
                            byte_addr_offset: int = 0, verify: bool = False):
        """
        单个页编程, 与128MB以下的NORflash兼容，支持3字节的地址访问,向前兼容。
        目标：只能看到编程一个页，看不到实现的细节，是3字节地址模式还是4字节地址模式
        Args:
            page_addr: offset page address, should convert to byte address
            data: should be less than page size, if exceeded will be ignored
            byte_addr_offset: data to be written may not be from 00 of a page
            verify: if True, read out page data to verify if data were correctly programed

        Returns:

        """

        if self.CURRENT_ADDRESS_MODE == "3BYTE":
            # todo: 小于128Mb的只能只用3字节寻址模式
            write_cmd = self.CMD_PAGE_PROGRAM
            addr_lens = 24
        elif self.CURRENT_ADDRESS_MODE == "4BYTE":
            # todo: 大于128Mb的强制使用4字节寻址模式， 3字节寻址模式还需要使用扩展地址，太麻烦
            write_cmd = self.CMD_PAGE_PROGRAM_4BYTE_ADDR
            addr_lens = 32
        else:
            raise ValueError('ADDRESS_MODE can only be "3BYTE" or "4BYTE"')

        if len(data) > self.PAGE_SIZE_BYTES:
            mlog.warning(f"[PageProgram]: data lens shouldn't larger than Page Size ")
            return None

        # step1 write enable
        self._write_enable()
        # step2 program data, calculate byte address from page address
        byte_addr = page_addr * self.PAGE_SIZE_BYTES + byte_addr_offset
        self._page_program_byteaddr_data(write_cmd, byte_addr, data)

        # step4 wait for completion
        self._wait_for_completion(self.TIMINGS_PageProgram)
        if verify:
            self._verify_page_content(page_addr, data)

    def program_pages(self, page_addr: int, data: Union[bytes, bytearray, Iterable[int]], data_addr: int = 0,
                      verify: bool = True):
        """
        write single page data

        Args:
            page_addr:
            data: should be less than page size, if exceeded will be ignored
            data_addr: data to be written may not be from 00 of a page
            verify: if True, read out page data to verify if data were correctly programed

        Returns:

        """
        if data_addr != 0:
            raise NotImplementedError("Currently only support page program from beginning of each page")
        page_data_list = self._data_to_page_data_list(data)

        # program single page data
        for page_data in page_data_list:
            self.program_single_page(page_addr, page_data, verify=verify)
            page_addr += 1

        return None

    # overrided in MyGenericNANDSpiFlashDevice

    def stauts_read_sr1(self) -> int:
        raise NotImplementedError

    def stauts_read_sr2(self) -> int:
        raise NotImplementedError

    def stauts_read_sr3(self) -> int:
        raise NotImplementedError

    def _read_single_status_reg(self, cmd: int) -> int:
        """
        NOR serial flash has 3 cmd for read status reg, different from NAND
        # Read Status Register: 0x--
        # ----------------------------------
        # | OpCode | Byte2 | Byte3 | Byte4 |
        # |   05H  |  S7-0 |  S7-0 |  S7-0 |
        # ----------------------------------
        Returns:
        """
        read_cmd = bytes((cmd,))

        reg_bytes = self._spiport.exchange(read_cmd, 1)
        if len(reg_bytes) != 1:
            raise SpiFlashTimeout("Unable to retrieve flash status")
        reg_int = int(reg_bytes.hex(), 16)
        return reg_int

    def _read_single_status_reg_tuple(self, cmd: int) -> Tuple:
        """
        NOR serial flash has 3 cmd for read status reg, different from NAND
        # Read Status Register 0Fh / 05h
        # ----------------------------------
        # | OpCode | Byte2 | Byte3 | Byte4 |
        # |   05H  |  S7-0 |  S7-0 |  S7-0 |
        # ----------------------------------
        Returns:
        """
        reg_int = self._read_single_status_reg(cmd)
        _tup = tuple(list(f"{reg_int:08b}"))
        return _tup

    @staticmethod
    def status_regval_int2tuple(val) -> Tuple:
        _tup = tuple(list(f"{val:08b}"))
        return _tup

    def status_reg_write_enable(self):
        _data_in = bytes((self.CMD_WRITE_STATUS_EN,))
        return self._spiport.exchange(_data_in)

    def erase_single_sector_4kb(self, byte_addr: int, verify: bool = False):
        """
        Args:
            byte_addr: byte address
            verify: True to verify with read FF of given sector

        Returns:

        """

        # step1 enable write
        if byte_addr > self.SIZE_BYTES:
            raise SpiFlashValueError

        self._write_enable()
        datain = bytes((self.CMD_ERASE_SECTOR4KB_4BYTE_ADDR,)) + self.__adress_int_to_bytes(byte_addr)
        self._spiport.exchange(datain)
        # step3 wait for complete
        self._wait_for_completion(self.TIMINGS_BlockErase)
        self._write_disable()

    def erase_single_block(self, block_idx: int, verify: bool = False) -> None:
        """
        erase the whole block which include the given page address,
        Args:
            block_idx: any page in the block to be ereased.
            verify:

        Returns:

        """
        # step1 enable write
        if block_idx > self.total_blocks - 1:
            raise SpiFlashValueError

        byte_addr = block_idx * self.BLOCK_SIZE_BYTES
        if self.CURRENT_ADDRESS_MODE == "3BYTE":

            data_in = bytes((self.CMD_ERASE_BLOCK,)) + self.__adress_int_to_bytes(byte_addr)
        else:
            data_in = bytes((self.CMD_ERASE_BLOCK_4BYTE_ADDR,)) + self.__adress_int_to_bytes(byte_addr)

        self._write_enable()
        self._spiport.exchange(data_in)
        # step3 wait for complete
        self._wait_for_completion(self.TIMINGS_BlockErase)
        # time.sleep(1)
        self._write_disable()

    def erase_chip(self, verify=False) -> None:
        """in pyseialflash it is implemented as Erase sectors/blocks/chip of a "generic" flash device.
            for NOR flash: use chip erase command
        """

        # step1 write enable
        self._write_enable()

        # step2 erase whole chip
        chip_erase_cmd = bytes((self.CMD_ERASE_CHIP,))
        self._spiport.exchange(chip_erase_cmd)

        # step3 wait for completion
        self._wait_for_completion(self.TIMINGS_ChipErase)
        if verify:
            data = [0xff for xx in range(self.PAGE_SIZE_BYTES)]
            for page_addr in range(self.total_pages):
                self._verify_page_content(page_addr, data)
        self._write_disable()

    def __adress_int_to_bytes(self, addr) -> Union[bytes, bytearray]:
        if self.CURRENT_ADDRESS_MODE == "3BYTE":
            addr_byte_num = 3
        elif self.CURRENT_ADDRESS_MODE == "4BYTE":
            addr_byte_num = 4
        else:
            raise ValueError("Unknown address mode")
        xx = bytes([(addr >> 8 * (addr_byte_num - idx - 1)) & 0xff for idx in range(addr_byte_num)])
        addr_bytes = bytes()
        for idx in range(addr_byte_num):
            x = (addr >> 8 * (addr_byte_num - idx - 1)) & 0xff
            addr_bytes += bytes((x,))
        return xx


if __name__ == '__main__':
    finding_ftdi_urls()
    # finding_ftdi_desc_urls()
