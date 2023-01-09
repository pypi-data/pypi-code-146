import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *


class DataSize(metaclass=jsii.JSIIMeta, jsii_type="cdk-extensions.core.DataSize"):
    @jsii.member(jsii_name="bytes")
    @builtins.classmethod
    def bytes(cls, bytes: jsii.Number) -> "DataSize":
        '''Create a ``DataSize`` representing an amount of bytes.

        :param bytes: The number of bytes this ``DataSize`` will represent.

        :return: A ``DataSize`` representing the specified number of bytes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataSize.bytes)
            check_type(argname="argument bytes", value=bytes, expected_type=type_hints["bytes"])
        return typing.cast("DataSize", jsii.sinvoke(cls, "bytes", [bytes]))

    @jsii.member(jsii_name="gibibytes")
    @builtins.classmethod
    def gibibytes(cls, gibibytes: jsii.Number) -> "DataSize":
        '''Create a ``DataSize`` representing an amount of gibibytes.

        :param gibibytes: The number of gibibytes this ``DataSize`` will represent.

        :return: A ``DataSize`` representing the specified number of gibibytes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataSize.gibibytes)
            check_type(argname="argument gibibytes", value=gibibytes, expected_type=type_hints["gibibytes"])
        return typing.cast("DataSize", jsii.sinvoke(cls, "gibibytes", [gibibytes]))

    @jsii.member(jsii_name="gigabytes")
    @builtins.classmethod
    def gigabytes(cls, gigabytes: jsii.Number) -> "DataSize":
        '''Create a ``DataSize`` representing an amount of gigabytes.

        :param gigabytes: The number of gigabytes this ``DataSize`` will represent.

        :return: A ``DataSize`` representing the specified number of gigabytes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataSize.gigabytes)
            check_type(argname="argument gigabytes", value=gigabytes, expected_type=type_hints["gigabytes"])
        return typing.cast("DataSize", jsii.sinvoke(cls, "gigabytes", [gigabytes]))

    @jsii.member(jsii_name="kibibytes")
    @builtins.classmethod
    def kibibytes(cls, kibibytes: jsii.Number) -> "DataSize":
        '''Create a ``DataSize`` representing an amount of kibibytes.

        :param kibibytes: The number of kibibytes this ``DataSize`` will represent.

        :return: A ``DataSize`` representing the specified number of kibibytes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataSize.kibibytes)
            check_type(argname="argument kibibytes", value=kibibytes, expected_type=type_hints["kibibytes"])
        return typing.cast("DataSize", jsii.sinvoke(cls, "kibibytes", [kibibytes]))

    @jsii.member(jsii_name="kilobytes")
    @builtins.classmethod
    def kilobytes(cls, kilobytes: jsii.Number) -> "DataSize":
        '''Create a ``DataSize`` representing an amount of kilobytes.

        :param kilobytes: The number of kilobytes this ``DataSize`` will represent.

        :return: A ``DataSize`` representing the specified number of kilobytes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataSize.kilobytes)
            check_type(argname="argument kilobytes", value=kilobytes, expected_type=type_hints["kilobytes"])
        return typing.cast("DataSize", jsii.sinvoke(cls, "kilobytes", [kilobytes]))

    @jsii.member(jsii_name="mebibytes")
    @builtins.classmethod
    def mebibytes(cls, mebibytes: jsii.Number) -> "DataSize":
        '''Create a ``DataSize`` representing an amount of mebibytes.

        :param mebibytes: The number of mebibytes this ``DataSize`` will represent.

        :return: A ``DataSize`` representing the specified number of mebibytes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataSize.mebibytes)
            check_type(argname="argument mebibytes", value=mebibytes, expected_type=type_hints["mebibytes"])
        return typing.cast("DataSize", jsii.sinvoke(cls, "mebibytes", [mebibytes]))

    @jsii.member(jsii_name="megabytes")
    @builtins.classmethod
    def megabytes(cls, megabytes: jsii.Number) -> "DataSize":
        '''Create a ``DataSize`` representing an amount of megabytes.

        :param megabytes: The number of megabytes this ``DataSize`` will represent.

        :return: A ``DataSize`` representing the specified number of megabytes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataSize.megabytes)
            check_type(argname="argument megabytes", value=megabytes, expected_type=type_hints["megabytes"])
        return typing.cast("DataSize", jsii.sinvoke(cls, "megabytes", [megabytes]))

    @jsii.member(jsii_name="pebibytes")
    @builtins.classmethod
    def pebibytes(cls, pebibytes: jsii.Number) -> "DataSize":
        '''Create a ``DataSize`` representing an amount of pebibytes.

        :param pebibytes: The number of pebibytes this ``DataSize`` will represent.

        :return: A ``DataSize`` representing the specified number of pebibytes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataSize.pebibytes)
            check_type(argname="argument pebibytes", value=pebibytes, expected_type=type_hints["pebibytes"])
        return typing.cast("DataSize", jsii.sinvoke(cls, "pebibytes", [pebibytes]))

    @jsii.member(jsii_name="petabytes")
    @builtins.classmethod
    def petabytes(cls, petabytes: jsii.Number) -> "DataSize":
        '''Create a ``DataSize`` representing an amount of petabytes.

        :param petabytes: The number of petabytes this ``DataSize`` will represent.

        :return: A ``DataSize`` representing the specified number of petabytes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataSize.petabytes)
            check_type(argname="argument petabytes", value=petabytes, expected_type=type_hints["petabytes"])
        return typing.cast("DataSize", jsii.sinvoke(cls, "petabytes", [petabytes]))

    @jsii.member(jsii_name="tebibytes")
    @builtins.classmethod
    def tebibytes(cls, tebibytes: jsii.Number) -> "DataSize":
        '''Create a ``DataSize`` representing an amount of tebibytes.

        :param tebibytes: The number of tebibytes this ``DataSize`` will represent.

        :return: A ``DataSize`` representing the specified number of tebibytes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataSize.tebibytes)
            check_type(argname="argument tebibytes", value=tebibytes, expected_type=type_hints["tebibytes"])
        return typing.cast("DataSize", jsii.sinvoke(cls, "tebibytes", [tebibytes]))

    @jsii.member(jsii_name="terabytes")
    @builtins.classmethod
    def terabytes(cls, terabytes: jsii.Number) -> "DataSize":
        '''Create a ``DataSize`` representing an amount of terabytes.

        :param terabytes: The number of terabytes this ``DataSize`` will represent.

        :return: A ``DataSize`` representing the specified number of terabytes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataSize.terabytes)
            check_type(argname="argument terabytes", value=terabytes, expected_type=type_hints["terabytes"])
        return typing.cast("DataSize", jsii.sinvoke(cls, "terabytes", [terabytes]))

    @jsii.member(jsii_name="toBytes")
    def to_bytes(self) -> jsii.Number:
        '''Convert the DataSize object to the byte representation.

        :return: The number of bytes for the data size.
        '''
        return typing.cast(jsii.Number, jsii.invoke(self, "toBytes", []))

    @jsii.member(jsii_name="toGibibytes")
    def to_gibibytes(self) -> jsii.Number:
        '''Convert the DataSize object to its gibibyte representation.

        If the data size doesn't fit evently into gibibytes it will be rounded
        up to the closest gibibyte which will be required to hold all the data.

        :return: The number of gibibytes for the data size.
        '''
        return typing.cast(jsii.Number, jsii.invoke(self, "toGibibytes", []))

    @jsii.member(jsii_name="toGigabytes")
    def to_gigabytes(self) -> jsii.Number:
        '''Convert the DataSize object to its gigabyte representation.

        If the data size doesn't fit evently into gigabytes it will be rounded
        up to the closest gigabyte which will be required to hold all the data.

        :return: The number of gigabytes for the data size.
        '''
        return typing.cast(jsii.Number, jsii.invoke(self, "toGigabytes", []))

    @jsii.member(jsii_name="toKibibytes")
    def to_kibibytes(self) -> jsii.Number:
        '''Convert the DataSize object to its kibibyte representation.

        If the data size doesn't fit evently into kibibytes it will be rounded
        up to the closest kibibyte which will be required to hold all the data.

        :return: The number of kibibytes for the data size.
        '''
        return typing.cast(jsii.Number, jsii.invoke(self, "toKibibytes", []))

    @jsii.member(jsii_name="toKilobytes")
    def to_kilobytes(self) -> jsii.Number:
        '''Convert the DataSize object to its kilobyte representation.

        If the data size doesn't fit evently into kilobytes it will be rounded
        up to the closest kilobyte which will be required to hold all the data.

        :return: The number of kilobytes for the data size.
        '''
        return typing.cast(jsii.Number, jsii.invoke(self, "toKilobytes", []))

    @jsii.member(jsii_name="toMebibytes")
    def to_mebibytes(self) -> jsii.Number:
        '''Convert the DataSize object to its mebibyte representation.

        If the data size doesn't fit evently into mebibytes it will be rounded
        up to the closest mebibyte which will be required to hold all the data.

        :return: The number of mebibytes for the data size.
        '''
        return typing.cast(jsii.Number, jsii.invoke(self, "toMebibytes", []))

    @jsii.member(jsii_name="toMegabytes")
    def to_megabytes(self) -> jsii.Number:
        '''Convert the DataSize object to its megabyte representation.

        If the data size doesn't fit evently into megabytes it will be rounded
        up to the closest megabyte which will be required to hold all the data.

        :return: The number of megabytes for the data size.
        '''
        return typing.cast(jsii.Number, jsii.invoke(self, "toMegabytes", []))

    @jsii.member(jsii_name="toPebibytes")
    def to_pebibytes(self) -> jsii.Number:
        '''Convert the DataSize object to its pebibyte representation.

        If the data size doesn't fit evently into pebibytes it will be rounded
        up to the closest pebibyte which will be required to hold all the data.

        :return: The number of pebibytes for the data size.
        '''
        return typing.cast(jsii.Number, jsii.invoke(self, "toPebibytes", []))

    @jsii.member(jsii_name="toPetabytes")
    def to_petabytes(self) -> jsii.Number:
        '''Convert the DataSize object to its petabyte representation.

        If the data size doesn't fit evently into petabytes it will be rounded
        up to the closest petabyte which will be required to hold all the data.

        :return: The number of petabytes for the data size.
        '''
        return typing.cast(jsii.Number, jsii.invoke(self, "toPetabytes", []))

    @jsii.member(jsii_name="toTebibytes")
    def to_tebibytes(self) -> jsii.Number:
        '''Convert the DataSize object to its tebibyte representation.

        If the data size doesn't fit evently into tebibytes it will be rounded
        up to the closest tebibyte which will be required to hold all the data.

        :return: The number of tebibytes for the data size.
        '''
        return typing.cast(jsii.Number, jsii.invoke(self, "toTebibytes", []))

    @jsii.member(jsii_name="toTerabytes")
    def to_terabytes(self) -> jsii.Number:
        '''Convert the DataSize object to its terabyte representation.

        If the data size doesn't fit evently into terabytes it will be rounded
        up to the closest terabyte which will be required to hold all the data.

        :return: The number of terabytes for the data size.
        '''
        return typing.cast(jsii.Number, jsii.invoke(self, "toTerabytes", []))


__all__ = [
    "DataSize",
]

publication.publish()
