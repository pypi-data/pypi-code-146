#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Exceptions definition for PacketParser plugin.
"""

try:
    from poppy.core.logger import logger
except:
    print('POPPy framework is not installed!')

__all__ = ['RPLError', 'InvalidPacketID',
            'SpiceError','SpiceKernelNotValid', 'NoSpiceFound',
           'TransferFunctionError', 'PacketParsingError']


def init(self, class_obj, message, *args, **kwargs):
    super(class_obj, self).__init__(*args, **kwargs)
    logger.error(message)
    self.message = message

class InvalidPacketID(Exception):
    """
    Exception raised when a packet has an invalid packet
    """
    def __init__(self, message, *args, **kwargs):
        init(self, InvalidPacketID, message, *args, **kwargs)

class RPLError(Exception):
    """
    Exception raised when an error has occurred with RPL
    """
    def __init__(self, message, *args, **kwargs):
        init(self, RPLError, message, *args, **kwargs)

class SpiceError(Exception):
    """
    Exception raised when an error has occurred with SPICE
    """
    def __init__(self, message, *args, **kwargs):
        init(self, SpiceError, message, *args, **kwargs)

class NoSpiceFound(Exception):
    """
    Exception SPICE not loaded
    """
    pass

class SpiceKernelNotValid(Exception):
    """
    Exception for badly formatted Spice kernel
    """
    pass


class PacketParsingError(Exception):
    """
    Exception raised when an error has occurred when parsing packets
    """
    def __init__(self, message, *args, **kwargs):
        init(self, PacketParsingError, message, *args, **kwargs)

class TransferFunctionError(Exception):
    """
    Exception raised when TransferFunction class call has failed
    """
    def __init__(self, message, *args, **kwargs):
        init(self, TransferFunctionError, message, *args, **kwargs)
