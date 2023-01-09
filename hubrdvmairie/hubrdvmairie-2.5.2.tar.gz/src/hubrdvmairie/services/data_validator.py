import re
from datetime import datetime


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def is_valid_search_criteria(search_criteria):
    try:
        valide = (
            int(search_criteria["radius_km"]) in [20, 40, 60]
            and bool(datetime.strptime(search_criteria["start_date"], "%Y-%m-%d"))
            and bool(datetime.strptime(search_criteria["end_date"], "%Y-%m-%d"))
            and isfloat(float(search_criteria["longitude"]))
            and isfloat(float(search_criteria["latitude"]))
            and bool(
                re.match(
                    r"^[A-zÀ-ú0-9',-.\s]{1,70}[0-9]{5}$", search_criteria["address"]
                )
            )
        )
    except ValueError:
        valide = False
    return valide
