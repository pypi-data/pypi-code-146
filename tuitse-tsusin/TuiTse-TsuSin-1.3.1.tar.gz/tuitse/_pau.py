from kesi.butkian.kongiong import 敢是拼音字元
from tuitse import THAU_JI, LIAN_JI, KHIN_SIANN_JI

KHANG_PEH = '\u00A0'


def pau(jitin):
    kiatko = []
    su = []
    ting_hing_si_lomaji = False
    ting_im_si_lomaji = False

    for ji in jitin:

        try:
            hing_si_lomaji = 敢是拼音字元(ji[0][-1])
        except IndexError:
            hing_si_lomaji = False
        try:
            im_si_lomaji = 敢是拼音字元(ji[1][-1])
        except IndexError:
            im_si_lomaji = False

        hanji = ji[0] if ji[0] else KHANG_PEH
        lomaji = ji[1] if ji[1] else KHANG_PEH
        lui = ji[2]
        sin = {}

        if lui == THAU_JI:
            if su:
                kiatko.append(su)
                su = []
            sin = {
                'hanji': hanji,
                'lomaji': lomaji,
                'si_tioh': ji[3]
            }
        elif lui == LIAN_JI or lui == KHIN_SIANN_JI:
            thiap = {
                'hanji': KHANG_PEH,
                'lomaji': KHANG_PEH,
                'si_tioh': True
            }
            if lui == LIAN_JI:
                hu = '-'
            else:
                hu = '--'
            if hing_si_lomaji and ting_hing_si_lomaji:
                thiap['hanji'] = hu
            if im_si_lomaji and ting_im_si_lomaji:
                thiap['lomaji'] = hu
            su.append(thiap)
            sin = {
                'hanji': hanji,
                'lomaji': lomaji,
                'si_tioh': ji[3]
            }
        elif lui == KHIN_SIANN_JI:
            pass
        su.append(sin)
        ting_hing_si_lomaji = hing_si_lomaji
        ting_im_si_lomaji = im_si_lomaji
    if su:
        kiatko.append(su)
    return kiatko
