import re

__all__ = ['sanitize_phone']


def sanitize_phone(phone, starts_with_seven=True):
    """
    >>> sanitize_phone("8 985 248 90-52")
    '79852489052'
    >>> sanitize_phone("+7 985 248 90-52")
    '79852489052'
    >>> sanitize_phone("+7 (985) 248 90-52")
    '79852489052'
    >>> sanitize_phone('996556177270', starts_with_seven=False)
    '996556177270'
    """
    phone = re.sub("[^0-9]", "", phone)
    if starts_with_seven:
        phone = '7' + phone[1:]
    return phone
