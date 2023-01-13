from collections import OrderedDict
from ..conf import (Currency, )
from ..validators import (max_length, )
from .base import (SerializableObject, SerializerField)
from pyPPL.models.package_service import PackageService
from pyPPL.models.recipient import Recipient

class Dormant(SerializableObject):

    json_mapping = OrderedDict([
        ('note', SerializerField('note')),
        ('recipient', SerializerField('recipient')),
        ('package_services', SerializerField('services')),
    ])


    note: str = None
    recipient: Recipient = None
    package_services: list[PackageService] = []

    def __init__(
        self,
        note: str = None,
        recipient: Recipient = None,
        package_services: list[PackageService] = [],
        ) -> None:

        self.note = max_length(note, 300)
        self.package_services = package_services
        self.recipient = recipient