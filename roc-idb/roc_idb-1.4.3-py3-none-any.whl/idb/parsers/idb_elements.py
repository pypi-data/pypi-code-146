#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import numpy
from poppy.core.generic.metaclasses import SingletonManager
from roc.idb.converters import IDBToBit as BitConverter
from roc.idb.converters import IDBToCDF as Converter
from roc.idb.converters import IDBToNumpy as NumpyConverter

__all__ = [
    'Packet',
    'Parameter',
    'ParameterDefinition',
    'Enumeration',
    'drop_numpy_type',
]


def drop_numpy_type(class_instance):
    def numpy_to_builtin_type(value):
        if isinstance(value, numpy.generic):
            return value.item()
        else:
            return value

    for key in class_instance.__dict__:
        setattr(
            class_instance,
            key,
            numpy_to_builtin_type(getattr(class_instance, key)),
        )


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(NumpyEncoder, self).default(obj)


class Packet(metaclass=SingletonManager):
    """
    Representation of a packet.
    """

    def __init__(
        self, name, srdbid, node=None, kind='normal', type=None, bit_size=0
    ):
        self.name = name
        # remove leading 0
        self.srdbid = str(int(srdbid))
        self.kind = kind
        self.node = node
        self._type = type
        self.byte_size = bit_size // 8
        self.bit_size = bit_size
        self.sid = None
        self.sid_eng = None
        self.service_type = None
        self.service_subtype = None

    def __repr__(self):
        if self.type == 'TM':
            prefix = 'YIW'
        else:
            prefix = 'ZIW'
        return prefix + '{0}'.format(self.srdbid.zfill(5))

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    def add_to_size(self, bit_length):
        self.bit_size += bit_length
        self.byte_size = self.bit_size // 8

    def update_size(self, bit_length):
        self.bit_size = bit_length
        self.byte_size = self.bit_size // 8

    def set_group_properties(self, group_size, block_size=None, spare_size=0):
        grp_bit_size = 0
        params_list_len = len(self.parameters)
        if block_size is None:
            for param in self.parameters[params_list_len - group_size :]:
                grp_bit_size += param.definition.data_type.bit_length
        else:
            grp_bit_size = block_size
        for param in self.parameters[params_list_len - group_size :]:
            param.group_size = group_size
            param.block_size = (grp_bit_size + spare_size) // 8

    def to_dict(self):
        packet_dict = {
            'parameters': {
                repr(parameter): parameter.to_dict()
                for parameter in self.parameters
            }
        }
        packet_dict.update(
            {
                key: getattr(self, key)
                for key in self.__dict__
                if key != 'node'
                and key != 'parameters'
                and '_eng' not in key
                and key != 'bit_size'
                and key != 'description'
            }
        )
        return {self.name: packet_dict}

    def dump(self):
        return [
            'Packet.%s = %s' % (key, getattr(self, key))
            for key in sorted(list(self.__dict__))
            if key != 'node'
        ]

    def to_json(self):
        return json.dumps(
            self.to_dict(), sort_keys=True, indent=4, cls=NumpyEncoder
        )


class Parameter(object):
    """
    Simple class container for the parameter definitions and types.
    """

    def __init__(self, definition, packet_type, unit=None):
        self.definition = definition
        self.type = packet_type
        self.group_size = 0
        self.group_counter = 0
        self.block_size = 0
        # if True this parameter contains the packet sid
        self.is_sid = False
        # alternative id used for some parameters (why ???)
        self.alias = None
        self.unit = unit

    def __lt__(self, other):
        self_value = int(self.name[3:].replace('G', '2').replace('D', '1'))
        self_other = int(other.name[3:].replace('G', '2').replace('D', '1'))
        return self_value < self_other

    @property
    def kind(self):
        if self.srdb_id[3] == 'G':
            return 'global'
        elif self.srdb_id[3] == 'D':
            return 'detailed'
        else:
            return 'normal'

    @property
    def srdb_id(self):
        return self.definition.srdb_id

    @property
    def name(self):
        return self.definition.srdb_id

    @classmethod
    def nameFromSRDBID(cls, short_srdb_id, packet_type, kind):
        """
        Return the name of the parameter in the SRDB rules.
        """
        if kind == 'normal':
            letter = ''
            size = 5
        elif kind == 'global':
            letter = 'G'
            size = 4
        elif kind == 'detailed':
            letter = 'D'
            size = 4

        if packet_type == 'TM':
            prefix = 'NIW'
        else:
            prefix = 'PIW'
        return prefix + letter + '{0}'.format(short_srdb_id.zfill(size))

    def __repr__(self):
        return self.name

    def dump(self):
        return [
            'Parameter.%s = %s' % (key, getattr(self, key))
            for key in sorted(list(self.__dict__))
        ]

    def to_dict(self):
        parameter_dict = {
            'definition - %s'
            % repr(self.definition): self.definition.to_dict()
        }
        parameter_dict.update(
            {
                key: getattr(self, key)
                for key in self.__dict__
                if key != 'definition'
            }
        )
        return parameter_dict

    def is_enumeration(self):
        """
        Return True if a parameter is an enumeration.
        """
        return isinstance(self.definition.data_type, Enumeration)


class ParameterDefinition(metaclass=SingletonManager):
    """
    For storing parameter information from their definition in the IDB.
    """

    def __init__(self, srdb_id, **kwargs):
        self.srdb_id = srdb_id

        for key in kwargs:
            setattr(self, key, kwargs[key])

    @property
    def name(self):
        return self.srdb_id

    def __repr__(self):
        return self.name

    def dump(self):
        return [
            'ParameterDefinition.%s = %s' % (key, getattr(self, key))
            for key in sorted(list(self.__dict__))
            if key != 'node'
        ]

    def to_dict(self):
        definition_dict = {
            key: getattr(self, key)
            for key in self.__dict__
            if key != 'node' and key != 'data_type' and key != 'description'
        }
        definition_dict.update({'data_type': repr(self.data_type)})
        return definition_dict


class Enumeration(metaclass=SingletonManager):
    """
    Class for storing information on enumerations from their definition.
    """

    def __init__(self, srdb_id, palisade_id=None):
        self.srdb_id = srdb_id
        self.palisade_id = palisade_id
        self._palisade_type = None
        self._values = dict()
        self._sub_enum_list = []

    def __repr__(self):
        if self._palisade_type is None:
            return f'Enum.None ({self.name})'
        else:
            return f'Enum.{self._palisade_type} ({self.name})'

    @property
    def name(self):
        return self.srdb_id

    @property
    def values(self):
        val = self._values
        for enum in self._sub_enum_list:
            val.update(enum.values)
        return val

    @values.setter
    def values(self, val):
        if isinstance(val, dict):
            self._values = val
        elif isinstance(val, list):
            self._sub_enum_list = val
        else:
            raise TypeError('Unsupported type for enumeration values')

    @property
    def data_type(self):
        return self._data_type

    @data_type.setter
    def data_type(self, value):
        self._palisade_type = value
        self._data_type = Converter()(value)
        self._bit_length = BitConverter()(value)
        self._numpy_type = NumpyConverter()(value)

    @property
    def numpy_type(self):
        return self._numpy_type

    @property
    def bit_length(self):
        return self._bit_length

    def dims(self):
        return 0

    def sizes(self):
        return None

    def record_variance(self):
        return 'T'

    def dimension_variances(self):
        return None


class Time(object):
    """
    Representation of time.
    """

    def __init__(self, coding, coarse, fine):
        self.coding = coding
        self.coarse = coarse
        self.fine = fine

    def __repr__(self):
        return 'Time.coding:%s/coarse:%s/fine:%s' % (
            self.coding,
            self.coarse,
            self.fine,
        )

    @property
    def data_type(self):
        return Converter()(max(self.coarse, self.fine))

    @property
    def numpy_type(self):
        return 'time'

    @property
    def bit_length(self):
        return 48

    def dims(self):
        return 1

    def sizes(self):
        return 3

    def record_variance(self):
        return 'T'

    def dimension_variances(self):
        return 'T'


class SimpleType(object):
    def __init__(self, data_type):
        self.data_type = data_type

    def __repr__(self):
        return self._palisade_type

    @property
    def data_type(self):
        return self._data_type

    @data_type.setter
    def data_type(self, value):
        self._palisade_type = value
        self._data_type = Converter()(value)
        self._bit_length = BitConverter()(value)
        self._numpy_type = NumpyConverter()(value)

    @property
    def numpy_type(self):
        return self._numpy_type

    @property
    def bit_length(self):
        return self._bit_length

    def dims(self):
        return 0

    def sizes(self):
        return None

    def record_variance(self):
        return 'T'

    def dimension_variances(self):
        return None
