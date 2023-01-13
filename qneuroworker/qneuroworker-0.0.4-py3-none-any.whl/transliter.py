import transliterate
from transliterate.base import TranslitLanguagePack, registry


class NeuroCoreLanguagePack(TranslitLanguagePack):
    language_code = "neurocore"
    language_name = "KeyBoard"
    mapping = ("ETYOPAHKXCBM",
               'ЕТУОРАНКХСВМ')


registry.register(NeuroCoreLanguagePack)


def translit_car_number(car_number):
    car_number = car_number.upper()
    res = transliterate.translit(car_number, language_code='neurocore')
    return res
