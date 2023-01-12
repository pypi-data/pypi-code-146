import re
from wedeliver_core.helpers.get_country_code import get_country_code


def validate_mobile_number(mobile):
    mobile = mobile.replace("+", "").replace(" ", "").lstrip("0")
    if len(mobile) < 12:
        country_code = get_country_code()
        if country_code == "sa":
            dial = "966"
        elif country_code == "ps":
            dial = "970"
        elif country_code == "eg":
            dial = "20"
        else:
            return False
        mobile = "{0}{1}".format(dial, int(mobile))
    if (
        re.match(
            r"^(009665|9665|\+9665|05|5)(5|0|3|6|4|9|1|8|7)([0-9]{7})$", str(mobile)
        )
        or re.match(r"^(009705|9705|\+9705|05|5)([0-9]{8})$", str(mobile))
        or re.match(r"^(201|01|\+201|00201)[0-9]{9}$", str(mobile))
    ):
        return mobile
    else:
        return False
