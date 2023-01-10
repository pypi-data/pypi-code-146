import phonenumbers  # type: ignore


class InvalidPhoneNumber(Exception):
    pass


def is_valid_number(phone_number: str) -> bool:
    if not phone_number:
        return False

    striped_number = str(phone_number).strip()

    if not striped_number.isnumeric():
        return False

    if striped_number.startswith("+"):
        return False

    try:
        # All phone numbers must be in international format with the + sign
        phonenumbers.parse("+{}".format(striped_number), None)
        # TODO: We can truly check for number validity but we are skipping it - https://github.com/daviddrysdale/python-phonenumbers
        return True
    except phonenumbers.NumberParseException:
        return False
