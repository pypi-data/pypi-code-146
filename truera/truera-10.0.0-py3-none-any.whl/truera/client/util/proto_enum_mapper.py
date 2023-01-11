from enum import Enum
from typing import Dict

from google.protobuf.internal.enum_type_wrapper import EnumTypeWrapper

from truera.protobuf.rbac import rbac_pb2 as rbac_pb


class ProtoEnumMapper(object):

    @staticmethod
    def get_enum(enum_type: EnumTypeWrapper, key: str) -> int:
        try:
            return enum_type.Value(key)
        except ValueError as ve:
            raise ValueError(
                'Invalid {enum_type} supplied : {key}'.format(
                    enum_type=enum_type.DESCRIPTOR.name, key=key
                )
            )
