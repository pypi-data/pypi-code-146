SHEET_MAP = {
    'Madrid - Ing': 'Madrid - Ingeniería',
}


def get_real_office_name(office_name):
    if office_name in SHEET_MAP:
        office_name = SHEET_MAP[office_name]

    return office_name
