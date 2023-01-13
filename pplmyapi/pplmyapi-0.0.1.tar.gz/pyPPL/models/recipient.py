from collections import OrderedDict
from ..conf import (Country, )
from ..validators import (max_length, )
from .base import (SerializableObject, SerializerField, SerializerList,)

class Recipient(SerializableObject):

    xml_mapping = OrderedDict([
        ('city', SerializerField('v1:City')),
        ('contact', SerializerField('v1:Contact')),
        ('country', SerializerField('v1:Country')),
        ('email', SerializerField('v1:Email')),
        ('name', SerializerField('v1:Name')),
        ('name2', SerializerField('v1:Name2')),
        ('phone', SerializerField('v1:Phone')),
        ('street', SerializerField('v1:Street')),
        ('zip_code', SerializerField('v1:ZipCode')),
    ])

    json_mapping = OrderedDict([
        ('city', SerializerField('city')),
        ('contact', SerializerField('contact')),
        ('country', SerializerField('country')),
        ('email', SerializerField('email')),
        ('name', SerializerField('name')),
        ('name2', SerializerField('name2')),
        ('phone', SerializerField('phone')),
        ('street', SerializerField('street')),
        ('zip_code', SerializerField('zipCode')),
    ])

    def __init__(
        self,
        name: str,
        city: str,
        street: str,
        zip_code: str,
        country = Country.CZ,
        phone: str = None,
        email: str = None,
        contact: str = None,
        name2: str = None,
        ) -> None:
        
        self.name = max_length(name, 50)
        self.city = max_length(city, 50)
        self.street = max_length(street, 50)
        self.zip_code = max_length(zip_code, 10)

        if not Country.has_value(country): 
            raise ValueError(f'Country {country} is not supported')
        self.country = country

        self.phone = max_length(phone, 30)
        self.email = max_length(email, 50)
        self.contact = max_length(contact, 300)
        self.name2 = max_length(name2, 50)
    

    