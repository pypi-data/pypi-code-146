from enum import Enum

from wedeliver_core.helpers.service_config import ServiceConfig


class Service:
    CAPTAIN = ServiceConfig('CAPTAIN_SERVICE')
    FINANCE = ServiceConfig('FINANCE_SERVICE')
    SDD = ServiceConfig('SDD_SERVICE')
    SUPPLIER = ServiceConfig('SUPPLIER_SERVICE')
    PN = ServiceConfig('PN_SERVICE')
    FINTECH = ServiceConfig('FINTECH_SERVICE')
    STC = ServiceConfig('STC_SERVICE')
    AUTH = ServiceConfig('AUTH_SERVICE')
    MAIL = ServiceConfig('MAIL_SERVICE')
    SMS = ServiceConfig('SMS_SERVICE')
    APILAYER = ServiceConfig('APILAYER_SERVICE')
    INVOICE = ServiceConfig('INVOICE_SERVICE')
    ADDRESS = ServiceConfig('ADDRESS_SERVICE')
    PUBLIC = ServiceConfig('PUBLIC_SERVICE')
    INTERNAL_NOTIFICATION = ServiceConfig('INTERNAL_NOTIFICATION_SERVICE')


class QueryTypes(Enum):
    SIMPLE_TABLE = 1
    FUNCTION = 2
    SEARCH = 3


class InstallmentType(Enum):
    LEASE = 'Lease'
    PERSONAL_LOAN = 'Personal Loan'


def list_enum_values(enum_type):
    "return list of dict the enum values and names for the given enum type"
    return [dict(id=e.value, Value=e.name.capitalize()) for e in enum_type]


def get_enum_value(enum_value, enum_type):
    "return  dict the enum values and names for the given enum type"
    for e in enum_type:
        if e.value == enum_value:
            return dict(id=e.value, Value=e.name.replace("_", " ").capitalize())


def format_values_dict(**values):
    "return  dict the enum values and names for the given enum type"
    return dict(**values)


class OrderByEnum(Enum):
    asc = "asc"
    desc = "desc"


def format_engine_size(engine_size_enum_type):
    "return the engine size in the format of 1.0 L"
    return [
        dict(id=e.value, Value=e.name[1:].replace("_", ".").capitalize() + " L")
        for e in engine_size_enum_type
    ]


def format_enum_with_dash(engine_size_enum_type):
    "return the enum containing dash to be without dash"
    return [
        dict(id=e.value, Value=e.name.replace("_", " ").capitalize())
        for e in engine_size_enum_type
    ]
