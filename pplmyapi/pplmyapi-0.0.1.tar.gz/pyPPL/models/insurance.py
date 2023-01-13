from collections import OrderedDict
from ..conf import (Currency, )
from ..validators import (max_length, )
from .base import (SerializableObject, SerializerField)

class Insurance(SerializableObject):

    json_mapping = OrderedDict([
        ('insurance_price', SerializerField('insurPrice')),
        ('insurance_currency', SerializerField('insurCurrency')),
    ])


    price: float = None
    currency: str = None

    def __init__(
        self,
        insurance_price: float = None,
        insurance_currency: str = None,
        ) -> None:

        # insurance price and it's currency
        if insurance_price is not None and insurance_currency is None:
            raise ValueError('Insurance currency must be provided if insurance price is provided')
        self.insurance_price = insurance_price
        if insurance_currency is not 'CZK':
            raise ValueError(f'Currency {insurance_currency} is not supported, use only CZK')
        self.insurance_currency = insurance_currency