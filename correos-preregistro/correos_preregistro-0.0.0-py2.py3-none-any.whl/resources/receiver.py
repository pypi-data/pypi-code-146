from dataclasses import dataclass


@dataclass
class Receiver:
    name: str
    surname: str
    address: str
    city: str
    state: str
    zip: str
    phone: str
    email: str
    lang: str
