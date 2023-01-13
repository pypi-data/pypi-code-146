from collections import OrderedDict
from ..conf import (Flag, )
from ..validators import (max_length, )
from .base import (SerializableObject, SerializerField)

class PackageFlag(SerializableObject):

    xml_mapping = OrderedDict([
        ('code', SerializerField('v1:Code')),
        ('value', SerializerField('v1:Value')),
    ])

    json_mapping = OrderedDict([
    ])

   

    code: str
    value: str

    def __init__(
        self,
        code: str,
        value: bool,
        ) -> None:

        if code not in Flag:
            raise ValueError(f'Invalid code: {code} for flags')
        if not isinstance(value, bool):
            raise ValueError(f'Invalid value: {value} for flags')
        if value == False:
            value = 'false'
        else:
            value = 'true'

        self.code = code.value
        self.value = value

        
