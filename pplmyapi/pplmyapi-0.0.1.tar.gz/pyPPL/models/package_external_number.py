from collections import OrderedDict
from ..conf import (ExternalNumber, )
from ..validators import (max_length, )
from .base import (SerializableObject, SerializerField)

class PackageExternalNumber(SerializableObject):

    xml_mapping = OrderedDict([
        ('code', SerializerField('v1:Code')),
        ('external_number', SerializerField('v1:ExtNumber')),
    ])

    json_mapping = OrderedDict([
        ('code', SerializerField('code')),
        ('external_number', SerializerField('externalNumber')),
    ])

    code: str
    external_number: str

    def __init__(
        self,
        code: str,
        external_number: str,
        ) -> None:

        if code not in ExternalNumber:
            raise ValueError(f'Invalid code: {code} for external number {external_number}')

        self.code = code.value
        self.external_number = max_length(external_number, 50)

        
