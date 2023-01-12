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

"""
Exceptions which can be raised by py-Ayiin Itself.
"""


class pyAyiinError(Exception):
    ...


class PyrogramMissingError(ImportError):
    ...


class TelethonMissingError(ImportError):
    ...


class DependencyMissingError(ImportError):
    ...


class RunningAsFunctionLibError(pyAyiinError):
    ...


class SpamFailed(Exception):
    ...


class DownloadFailed(Exception):
    ...


class DelAllFailed(Exception):
    ...


class FFmpegReturnCodeError(Exception):
    ...
