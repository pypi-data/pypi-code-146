# py - Ayiin
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/pyAyiin >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/pyAyiin/blob/main/LICENSE/>.
#
# FROM py-Ayiin <https://github.com/AyiinXd/pyAyiin>
# t.me/AyiinChat & t.me/AyiinSupport


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

class Changers(object):
    async def int_to_alpha(self, user_id: int) -> str:
        alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
        text = ""
        user_id = str(user_id)
        for i in user_id:
            text += alphabet[int(i)]
        return text


    async def alpha_to_int(self, user_id_alphabet: str) -> int:
        alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
        user_id = ""
        for i in user_id_alphabet:
            index = alphabet.index(i)
            user_id += str(index)
        user_id = int(user_id)
        return user_id


    def time_to_seconds(self, time):
        stringt = str(time)
        return sum(
            int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":")))
        )


    def seconds_to_min(self, seconds):
        if seconds is not None:
            seconds = int(seconds)
            d, h, m, s = (
                seconds // (3600 * 24),
                seconds // 3600 % 24,
                seconds % 3600 // 60,
                seconds % 3600 % 60,
            )
            if d > 0:
                return "{:02d}:{:02d}:{:02d}:{:02d}".format(d, h, m, s)
            elif h > 0:
                return "{:02d}:{:02d}:{:02d}".format(h, m, s)
            elif m > 0:
                return "{:02d}:{:02d}".format(m, s)
            elif s > 0:
                return "00:{:02d}".format(s)
        return "-"
