#!/usr/bin/env python3
"""
Basic Parameters library

Functions to convert BP

Authors : B. Katra (LPP), R. Piberne (LPP)
"""
# -*- coding: utf-8 -*-

import numpy as np

def init_struct(struct):
    """
    Initialize structures for BP conversion

    :param self: Object instance.
    :param struct: python structure used for BP conversion.
    :type self: object
    :type struct: structure
    :return:
    :rtype:
    :Example: init_struct(struct)

    """

    #For floating point data to be recorded on 16-bit words :
    struct.nbitexp = 6                  # number of bits for the exponent
    struct.nbitsig = 16 - struct.nbitexp       # number of bits for the significand
    struct.rangesig_16 = (1 << struct.nbitsig)-1  # == 2^nbitsig - 1
    struct.rangesig_14 = (1 << 8)-1
    struct.expmax = 32 + 5
    struct.expmin = struct.expmax - (1 << struct.nbitexp) + 1

def convToFloat16(struct, rFloat) :
    """
    BP1 conversion from integer to float16

    :param self: Object instance.
    :param struct: python structure used for BP conversion.
    :param rFloat: Unsigned short (np.uint16_t) to convert
    :type self: object
    :type struct: structure
    :return: The corresponding float
    :rtype: np.float64
    :Example: cdfL2['PB'][...] = convToFloat16(struct, cdfL1['PB'][...])

    """


    #print(rFloat, type(rFloat))
    #print(bin(rFloat))

    #We extract A_exponent and A_significant parts
    A_exp = np.uint8((rFloat>>10) & 0x3f)
    A_sig = (rFloat & 0x3ff)

    #print(A_exp, bin(A_exp))
    #print(A_sig, bin(A_sig))


    #We compute values of significand and exponent
    exp = np.int32(A_exp)+np.int32(struct.expmin)
    sig = np.float64((np.int32(A_sig)) / np.float64((np.int32(struct.rangesig_16))) + 1)/2
    sig_square = sig*2.**exp

    return sig_square


def convToFloat8(rUint) :
    """
    BP1 conversion from integer to float8

    :param self: Object instance.
    :param rUint: Unsigned char (np.uint8_t) to convert
    :type self: object
    :type rUint: np.uint8_t
    :return: The corresponding float
    :rtype: np.float32
    :Example: cdfL2['NVEC_V0'][...] = convToFloat8(cdfL1['NVEC_V0'][...])

    """

    return np.float32(np.int32(rUint)/127.5)-1


def convToFloat4(rUint) :
    """
    BP1 conversion from integer to float4

    :param self: Object instance.
    :param rUint: Unsigned char (np.uint8_t) to convert.
    :type self: object
    :type rUint: np.uint8_t
    :return: The corresponding float
    :rtype: np.float32
    :Example: cdfL2['ELLIP'][...] = convToFloat4(cdfL1['ELLIP'][...])

    """

    #rUint = (rUint >> 3) & 0xF
    #(not need the bit right-shift operator here since the 4-bits of ELLIP have been written in the L0 file in the first 4th bits space
    rUint = rUint & 0xF # 0xF = 00001111

    return np.float32(np.int32(rUint)/15.0)


def convToFloat3(rUint) :
    """
    BP1 conversion from integer to float3

    :param self: Object instance.
    :param rUint: Unsigned char (np.uint8_t) to convert.
    :type self: object
    :type rUint: np.uint8_t
    :return: The corresponding float
    :rtype: np.float32
    :Example: cdfL2['DOP'][...] = convToFloat3(cdfL1['DOP'][...])

    """
    rUint = rUint & 0x7
    return np.float32(np.int32(rUint)/7.0)


def convToFloat14(struct, rFloat) :
    """
    BP1 conversion from integer to float14

    :param self: Object instance.
    :param struct: python structure used for BP conversion.
    :param rFloat: Unsigned short (np.uint16_t) to convert
    :type self: object
    :type struct: structure
    :return: The corresponding float
    :rtype: np.float64
    :Example: cdfL2['VPHI'][...] = convToFloat14(struct, cdfL1['VPHI'][...])

    """

    #We extract A_exponent and A_significant parts
    A_exp = np.uint8((rFloat>>8) & 0x3f)
    A_sig = (rFloat & 0xff)

    #We compute values of significand and exponent
    exp = np.int32(A_exp)+np.int32(struct.expmin)
    sig = np.float64((np.int32(A_sig))/np.float64((np.int32(struct.rangesig_14))) + 1)/2
    sig_square = sig*2.**exp
    return sig_square

def Uint16ToUint8(uint16_array, offset, length):
    """
    Extract bits from an input 16-bits unsigned integer array.
    Output array is returned as an numpy.uint8.

    :param uint16_array: Unsigned short (np.uint16_t) to convert
    :param offset: bit offset
    :param length: number of bits to extract, provided as a hexa
    :return: array of numpy.uint8 with bits extracted
    """

    #We extract bit(s) from input
    return (np.uint8)((uint16_array>>offset) & length)

def convToAutoFloat(struct, rFloat):
    """
    BP2 conversion from integer to float for auto correlation products

    :param self: Object instance.
    :param struct: python structure used for BP conversion.
    :param rUint: Unsigned short (np.uint8_t) to convert
    :type self: object
    :type struct: structure
    :return: The corresponding float
    :rtype: np.float16
    :Example: cdfL2['AUTO'][...] = convToAutoFloat(struct, cdfL1['AUTO'][...])

    """

    #We extract A_exponent and A_significant parts
    A_exp = np.uint8((rFloat>>10) & 0x3f)
    A_sig = (rFloat & 0x3ff)

    #We compute values of significand and exponent
    exp = np.int32(A_exp)+np.int32(struct.expmin)
    sig = np.float64((np.int32(A_sig))/np.float64((np.int32(struct.rangesig_16))) + 1)/2

    sig_square = sig*2.**exp

    return sig_square

def convToCrossFloat(rUint) :
    """
    BP2 conversion from integer to float for cross correlation products

    :param self: Object instance.
    :param rUint: Unsigned char (np.uint8_t) to convert.
    :type self: object
    :type rUint: np.uint8_t
    :return: The corresponding float
    :rtype: np.float64
    :Example: cdfL2['CROSS_RE'][...] = convToCrossFloat(cdfL1['CROSS_RE'][...])

    """
    return np.float32(np.int32(rUint)/127.5)-1


def convToUint8(rUint):
    """
    BP1 conversion from integer to unsigned 8 bit integer for nvec_v2 sign bit

    :param rUint: Unsigned char to convert.
    :type rUint: np.uint8_t
    :return: The corresponding uint8
    :rtype: np.uint8

    """

    return np.uint8(rUint & 0x1)

def main():
    pass


if __name__ == "__main__":
    main()