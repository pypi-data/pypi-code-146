from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.解析錯誤 import 解析錯誤
from kesi import Ku
from 用字 import 建議
from tuitse.constant import THAU_JI, KHIN_SIANN_JI, LIAN_JI


def kiamtsa(hanji, lomaji, hamsik_tsitji_ubo=None, pio=建議):
    ku_han = Ku(hanji)
    ku_lo = Ku(lomaji)
    ji_han = list(ku_han.thianji())
    ji_lo = list(ku_lo.thianji())

    # Kí ta̍k jī tī sû-thâu a̍h sû-bué
    ji_id_tin = []
    for su in ku_lo:
        ji_id_tin.append(THAU_JI)

        ji_tin = list(su)[1:]
        for ji in ji_tin:
            if ji.si_khinsiann:
                ji_id_tin.append(KHIN_SIANN_JI)
            else:
                ji_id_tin.append(LIAN_JI)

    # Kiàn-li̍p DP pió
    dp_tin = [[], ]
    loo_tin = [[], ]

    huinn_tngte = len(ji_han)
    for _punso in range(huinn_tngte + 1):
        dp_tin[0].append((0, 0))
        loo_tin[0].append('toping')
    for lo in ji_lo:
        tsua_dp = [(0, 0), ]
        tsua_loo = ['binting', ]

        for binting, tshu, han in zip(
            dp_tin[-1][1:], dp_tin[-1], ji_han
        ):
            try:
                jibut = 拆文分析器.建立字物件(han.hanlo, lo.hanlo)
            except 解析錯誤 as e:
                print('解析錯誤, ', e)
                kam_u = False
            else:
                hanlo_kangkhuan = (
                    han.hanlo == lo.hanlo
                    or '--{}'.format(han.hanlo) == lo.hanlo
                )
                kam_u = (pio.有這个字無(jibut) or (
                    hanlo_kangkhuan
                    and not kam_alapik_sooji(jibut.型, jibut.音)
                ))
                if hamsik_tsitji_ubo:
                    kam_u = kam_u or hamsik_tsitji_ubo(jibut)
            toping = tsua_dp[-1]
            if kam_u:
                hah_tshu = (tshu[0] + 1, tshu[1])
                if toping >= binting and toping >= hah_tshu:
                    tsua_dp.append(toping)
                    tsua_loo.append('toping')
                elif binting >= hah_tshu:
                    tsua_dp.append(binting)
                    tsua_loo.append('binting')
                else:
                    tsua_dp.append(hah_tshu)
                    tsua_loo.append('tshu')
            else:
                # Bô tsit jī
                behah_tshu = (tshu[0], tshu[1] + 1)
                if binting >= toping and binting >= behah_tshu:
                    tsua_dp.append(binting)
                    tsua_loo.append('binting')
                elif toping >= binting and toping >= behah_tshu:
                    tsua_dp.append(toping)
                    tsua_loo.append('toping')
                else:
                    tsua_dp.append(behah_tshu)
                    tsua_loo.append('behah_tshu')
        dp_tin.append(tsua_dp)
        loo_tin.append(tsua_loo)
    # Se̍h-thâu khuànn siáng ū tuì--tio̍h
    kiat_ko = []
    tit = len(loo_tin) - 1
    huinn = len(loo_tin[0]) - 1
    ting_id = THAU_JI
    while tit > 0 or huinn > 0:
        if loo_tin[tit][huinn] == 'binting':
            tit -= 1
            kiat_ko.append((
                '',
                ji_lo[tit].hanlo,
                ji_id_tin[tit],
                False
            ))
            ting_id = ji_id_tin[tit]
        elif loo_tin[tit][huinn] == 'toping':
            huinn -= 1
            kiat_ko.append((
                ji_han[huinn].hanlo,
                '',
                ting_id,
                False
            ))
        elif loo_tin[tit][huinn] == 'tshu':
            tit -= 1
            huinn -= 1
            kiat_ko.append((
                ji_han[huinn].hanlo,
                ji_lo[tit].hanlo,
                ji_id_tin[tit],
                True
            ))
            ting_id = ji_id_tin[tit]
        elif loo_tin[tit][huinn] == 'behah_tshu':
            tit -= 1
            huinn -= 1
            kiat_ko.append((
                ji_han[huinn].hanlo,
                ji_lo[tit].hanlo,
                ji_id_tin[tit],
                False
            ))
            ting_id = ji_id_tin[tit]
    kiat_ko.reverse()
    siongbue = []
    for ji in kiat_ko:
        if ji[0].startswith('--'):
            han = ji[0][2:]
        else:
            han = ji[0]
        if ji[1].startswith('--'):
            lo = ji[1][2:]
        else:
            lo = ji[1]
        siongbue.append((
            han, lo, ji[2], ji[3]
        ))
    return siongbue


def kam_alapik_sooji(hanji, lomaji):
    try:
        int(hanji)
        int(lomaji)
    except ValueError:
        return False
    return True
