import re


valid_email_addresses = re.compile(r'^[^.]([\w!#$%&\\\'*+\-/=?^_`.{|}~]*[^.])?@([\w-]+\.)+[\w-]+$')
double_dots = re.compile(r'\.\.')


def is_valid_email_address(value):
    return valid_email_addresses.match(value) is not None and double_dots.search(value) is None
