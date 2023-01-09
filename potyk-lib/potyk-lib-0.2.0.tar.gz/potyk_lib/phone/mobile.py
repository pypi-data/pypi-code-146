import phonenumbers

__all__ = ['is_mobile']


def is_mobile(phone: str) -> bool:
    """
    >>> is_mobile("79852489052")
    True
    >>> is_mobile('74955536678')
    False
    """
    return phonenumbers.number_type(phonenumbers.parse(phone, region="RU")) == \
           phonenumbers.PhoneNumberType.MOBILE
