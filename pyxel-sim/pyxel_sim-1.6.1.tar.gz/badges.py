#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

"""Badge creator script.
by David Lucsanyi
"""
import argparse
import subprocess


def badges():
    """Create badges."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-cov",
        "--coverage",
        type=float,
        default=None,
        help="Test coverage badge with percent",
    )
    parser.add_argument(
        "-ver", "--version", type=str, default=None, help="Version badge"
    )
    parser.add_argument(
        "-lic", "--license", type=str, default=None, help="License badge"
    )
    parser.add_argument(
        "-doc", "--documentation", type=str, default=None, help="Documentation badge"
    )
    parser.add_argument("-ch", "--chat", type=str, default=None, help="Chat badge")
    opts = parser.parse_args()

    if opts.coverage:
        if 0.0 <= opts.coverage < 20.0:
            colour = "red"
        elif 20.0 <= opts.coverage < 40.0:
            colour = "orange"
        elif 40.0 <= opts.coverage < 60.0:
            colour = "yellow"
        elif 60.0 <= opts.coverage < 80.0:
            colour = "yellowgreen"
        elif 80.0 <= opts.coverage < 90.0:
            colour = "green"
        elif 90.0 <= opts.coverage <= 100.0:
            colour = "brightgreen"
        else:
            colour = "lightgrey"
        percent = f"{opts.coverage:.2f}"
        process = (
            "wget -O coverage.svg https://img.shields.io/badge/coverage-"
            + percent
            + "%25-"
            + colour
            + ".svg"
        )
        subprocess.run(process, shell=True)

    if opts.documentation:
        colour = "brightgreen"
        process = (
            "wget -O documentation.svg https://img.shields.io/badge/docs-"
            + opts.documentation
            + "-"
            + colour
            + ".svg"
        )
        subprocess.run(process, shell=True)

    # if opts.license:
    #     colour = 'green'
    #     process = 'wget -O license.svg https://img.shields.io/badge/license-' + \
    #               opts.license + '-' + colour + '.svg'
    #     subprocess.run(process, shell=True)

    # if opts.chat:
    #     colour = 'green'
    #     process = 'wget -O chat.svg https://img.shields.io/badge/chat-' + \
    #               opts.chat + '-' + colour + '.svg'
    #     subprocess.run(process, shell=True)


if __name__ == "__main__":
    badges()
