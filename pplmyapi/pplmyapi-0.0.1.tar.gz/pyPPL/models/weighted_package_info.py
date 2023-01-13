from collections import OrderedDict
from ..conf import (Currency, )
from ..validators import (max_length, )
from .base import (SerializableObject, SerializerField, )

class WeightedPackageInfo(SerializableObject):

    xml_mapping = OrderedDict([
        ('weight', SerializerField('v1:Weight')),
    ])

    json_mapping = OrderedDict([
        ('weight', SerializerField('weight')),
    ])

    weight: float = None

    def __init__(
        self,
        weight: float,
        ) -> None:

        # cod price and it's currency
        if weight is None:
            raise ValueError('Weight must be provided')
        self.weight = weight
        