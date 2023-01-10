from dataclasses import dataclass


@dataclass
class Sender:
    name: str
    nif: str
    address: str
    city: str
    state: str
    zip: str
    phone: str
    email: str
    lang: str
