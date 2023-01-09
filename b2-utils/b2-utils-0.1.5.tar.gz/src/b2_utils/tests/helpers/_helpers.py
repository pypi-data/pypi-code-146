from model_bakery import baker
from validate_docbr import CNPJ, CPF

from b2_utils.models import Address, City, Phone

__all__ = [
    "sample_city",
    "sample_address",
    "sample_phone",
    "sample_cpf",
    "sample_cnpj",
]


def sample_city(**kwargs):
    """Create and return a sample City"""

    return baker.make(City, **kwargs)


def sample_address(**kwargs):
    """Create and return a sample Address"""

    kwargs["city"] = kwargs.get("city", sample_city)
    return baker.make(Address, **kwargs)


def sample_phone(**kwargs):
    """Create and return a sample Phone"""

    return baker.make(Phone, **kwargs)


def sample_cpf():
    """Return a sample CPF"""

    return CPF().generate()


def sample_cnpj():
    """Return a sample CNPJ"""

    return CNPJ().generate()
