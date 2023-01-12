# AyiinXd
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/AyiinXd >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/AyiinXd/blob/main/LICENSE/>.
#
# FROM AyiinXd <https://github.com/AyiinXd/AyiinXd>
# t.me/AyiinChat & t.me/AyiinSupport

# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================


import os


def where_hosted():
    if os.getenv("DYNO"):
        return "Heroku"
    if os.getenv("RAILWAY_STATIC_URL"):
        return "Railway"
    if os.getenv("KUBERNETES_PORT"):
        return "Qovery"
    if os.getenv("WINDOW") and os.getenv("WINDOW") != "0":
        return "Windows"
    if os.getenv("RUNNER_USER") or os.getenv("HOSTNAME"):
        return "Github actions"
    if os.getenv("ANDROID_ROOT"):
        return "Termux"
    return "VPS"


if where_hosted() == "VPS":
    def _ask_input():
        # Ask for Input even on Vps and other platforms.
        def new_input(*args, **kwargs):
            raise EOFError("args=" + str(args) + ", kwargs=" + str(kwargs))

        __builtins__["input"] = new_input

    _ask_input()
