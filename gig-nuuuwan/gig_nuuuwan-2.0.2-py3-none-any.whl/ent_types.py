class ENTITY_TYPE:
    COUNTRY = 'country'
    PROVINCE = 'province'
    DISTRICT = 'district'
    DSD = 'dsd'
    GND = 'gnd'
    ED = 'ed'
    PD = 'pd'
    LG = 'lg'
    MOH = 'moh'
    UNKNOWN = 'unknown'

    @staticmethod
    def list():
        return [
            ENTITY_TYPE.PROVINCE,
            ENTITY_TYPE.DISTRICT,
            ENTITY_TYPE.DSD,
            ENTITY_TYPE.GND,
            ENTITY_TYPE.ED,
            ENTITY_TYPE.PD,
            ENTITY_TYPE.LG,
            ENTITY_TYPE.MOH,
        ]


NEARBY_ENTITY_TYPES = []


def get_entity_type(entity_id):
    n = len(entity_id)
    if entity_id[:2] == 'LK':
        if n == 2:
            return ENTITY_TYPE.COUNTRY
        if n == 4:
            return ENTITY_TYPE.PROVINCE
        if n == 5:
            return ENTITY_TYPE.DISTRICT
        if n == 7:
            return ENTITY_TYPE.DSD
        if n == 10:
            return ENTITY_TYPE.GND

    if entity_id[:2] == 'EC':
        if n == 5:
            return ENTITY_TYPE.ED
        if n == 6:
            return ENTITY_TYPE.PD

    if entity_id[:2] == 'PS':
        return ENTITY_TYPE.PS

    if entity_id[:2] == 'LG':
        return ENTITY_TYPE.LG

    if entity_id[:3] == 'MOH':
        return ENTITY_TYPE.MOH

    return ENTITY_TYPE.UNKNOWN
