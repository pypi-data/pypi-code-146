##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
##

import os, datetime, requests

# Windows doesn't support colors
COLOR_START = "" if os.name == "nt" else "\033[94m"
COLOR_END = "" if os.name == "nt" else "\033[0m"


def optumi_log(message):
    try:
        requests.request(
            "POST",
            "https://ocl.optumi.net:8443/message",
            json={
                "message": "[" + datetime.datetime.now().isoformat() + "] " + message
            },
        )
    except Exception as e:
        print(e)


def optumi_format_and_log(c=None, message=""):
    if c is None:
        formatted = COLOR_START + "[Optumi]" + COLOR_END + " " + message
    else:
        formatted = (
            COLOR_START
            + "[Optumi]"
            + COLOR_END
            + " "
            + c.__class__.__name__
            + ": "
            + message
        )

    optumi_log(formatted)

    return formatted
