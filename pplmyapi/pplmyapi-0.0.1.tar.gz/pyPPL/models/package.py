from collections import OrderedDict

from pyPPL.models.package_external_number import PackageExternalNumber
from pyPPL.models.package_set import PackageSet
from pyPPL.models.special_delivery import SpecialDelivery
from pyPPL.models.weighted_package_info import WeightedPackageInfo
from pyPPL.models.package_service import PackageService
from pyPPL.models.recipient import Recipient
from pyPPL.models.payment_info import PaymentInfo
from pyPPL.models.sender import Sender
from pyPPL.models.package_flag import PackageFlag
from pyPPL.models.insurance import Insurance
from pyPPL.models.dormant import Dormant

from ..validators import (max_length, )
from .base import (SerializableObject, SerializerField, SerializerList, )
from ..conf import (Product, CASH_ON_DELIVERY, PARCEL_SHOP_PRODUCTS, Services, Age, DELIVERY_DOMESTIC, DELIVERY_INTERNATIONAL,)
from typing import Union

class Package(SerializableObject):

    xml_mapping = OrderedDict([
        ('package_number', SerializerField('v1:PackNumber')),
        ('package_product_type', SerializerField('v1:PackProductType')),
        ('note', SerializerField('v1:Note')),
        ('depo_code', SerializerField('v1:DepoCode')),
        ('sender', SerializerField('v1:Sender')),
        ('recipient', SerializerField('v1:Recipient')),
        ('special_delivery', SerializerField('v1:SpecialDelivery')),
        ('payment_info', SerializerField('v1:PaymentInfo')),
        ('external_numbers', SerializerList('v1:PackagesExtNums', list_item_name='v1:MyApiPackageExtNum')),
        ('package_services', SerializerList('v1:PackageServices', list_item_name='v1:MyApiPackageInServices')),
        ('flags', SerializerList('v1:PackageFlags', list_item_name='v1:MyApiFlag')),
        ('package_set', SerializerField('v1:PackageSet')),
        ('weighted_package_info', SerializerField('v1:WeightedPackageInfo')),
    ])

    json_mapping = OrderedDict([
        ('package_number', SerializerField('referenceId')),
        ('package_product_type', SerializerField('productType')),
        ('note', SerializerField('note')),
        ('age_check', SerializerField('ageCheck')),
        ('depo_code', SerializerField('depot')),
        ('package_set', SerializerField('shipmentSet')),
        ('sender', SerializerField('sender')),
        ('recipient', SerializerField('recipient')),
        ('dormant', SerializerField('dormant')),
        ('special_delivery', SerializerField('specificDelivery')),
        ('payment_info', SerializerField('cashOnDelivery')),
        ('external_numbers', SerializerList('externalNumbers')),
        ('package_services', SerializerList('services')),
        # ('flags', SerializerList('v1:PackageFlags', list_item_name='v1:MyApiFlag')), # DOESNT IMPLEMENT
        ('weighted_package_info', SerializerField('weighedShipmentInfo')),
    ])

    package_number: str = None
    package_product_type: str = None
    note: str = None
    sender: Sender = None
    recipient: Recipient = None
    depo_code: str = None
    special_delivery: SpecialDelivery = None
    payment_info: PaymentInfo = None
    external_numbers: list[PackageExternalNumber] = []
    package_services: list[PackageService] = []
    flags: list[PackageFlag] = []
    weighted_package_info: WeightedPackageInfo = None
    package_set: PackageSet = None
    age_check: Age = None
    dormant: Dormant = None
    insurance: Insurance = None


    def __init__(
        self,
        package_number: str,
        package_product_type: str,
        note: str,
        recipient: Recipient,
        sender: Sender = None,
        depo_code: str = None,
        special_delivery: SpecialDelivery = None,
        payment_info: PaymentInfo = None, 
        external_numbers: list[PackageExternalNumber] = [],
        package_services: list[PackageService] = [],
        flags: list[PackageFlag] = [],
        weighted_package_info: WeightedPackageInfo = None,
        package_set: PackageSet = None,
        age_check: Age = None,
        dormant: Dormant = None, 
        insurance: Insurance = None, 
        ) -> None:
        
        self.note = max_length(note, 300)
        self.package_number = max_length(package_number, 20)
        
        self.sender = sender
        self.recipient = recipient
        
        if not package_product_type in Product:
            raise ValueError(f'Product {package_product_type} is not supported')
        self.package_product_type = package_product_type.value
        
        self.depo_code = max_length(depo_code, 10)
        
        if special_delivery is not None and special_delivery.parcel_shop_code is not None:
            # parcel shop code is only supported for parcel shop products
            if not package_product_type in PARCEL_SHOP_PRODUCTS:
                raise ValueError(f'Product {package_product_type} does not support parcel shop in special delivery')
        self.special_delivery = special_delivery

        if payment_info is not None and payment_info.is_cod():
            if not package_product_type in CASH_ON_DELIVERY:
                raise ValueError(f'Product {package_product_type} does not support cash on delivery')
        
        self.payment_info = payment_info


        self.external_numbers = external_numbers
        self.package_services = package_services
        self.flags = flags
        self.weighted_package_info = weighted_package_info
        if package_set is None:
            # create a new package set containing this package only
            package_set = PackageSet(package_number)
        self.package_set = package_set

        if age_check is not None:
            self.age_check = age_check

        if insurance is not None:
            # insurance on label is provided only for:
            # - domestic parcels with value > 50 000 CZK
            # - international parcels with value > 100 000 CZK
            if (package_product_type in DELIVERY_DOMESTIC and insurance.value > 50000) or \
                (package_product_type in DELIVERY_INTERNATIONAL and insurance.value > 100000):
                    self.insurance = insurance

        if dormant is not None:
            self.dormant = dormant