# -*- coding: utf-8 -*-
import sys
import argparse
from pawnlib.builder.generator import generate_banner
from pawnlib.__version__ import __version__ as _version
from pawnlib.config.globalconfig import pawnlib_config as pawn
from pawnlib.utils.log import AppLogger
from pawnlib.utils.http import disable_ssl_warnings
from pawnlib.typing import check, converter
from pawnlib.output import *
from pawnlib.output.color_print import *

from toolchains.utils import http
from pawnlib.typing import date_utils, str2bool


__version__ = "0.0.1"


def get_parser():
    parser = argparse.ArgumentParser(description='Websocket')
    parser = get_arguments(parser)
    return parser


def get_arguments(parser):
    parser.add_argument('url', help='url')
    parser.add_argument('-c', '--command', type=str, help=f'command', default=None, choices=["start", "stop", "restart", None])
    parser.add_argument('-v', '--verbose', action='count', help=f'verbose mode. view level', default=0)
    parser.add_argument('-b', '--blockheight', type=int, help=f'position of blockheight to start. ', default=0)
    parser.add_argument('-d', '--diff', type=int, help=f'diff timestamp ', default=2)
    parser.add_argument('-t', '--target', type=str, nargs='+', help=f'Monitoring target (block|tx)', default=["block", "tx"], choices=["block", "tx"])
    parser.add_argument('--stack-limit', type=int, help=f'Stack limit count for notify', default=3)
    parser.add_argument('--wait', type=str2bool, help=f'waiting for response', default=1)
    return parser


def main():
    banner = generate_banner(
        app_name="websocket",
        author="jinwoo",
        description="get the aws metadata",
        font="graffiti",
        version=_version
    )
    print(banner)
    # pawn_http.disable_ssl_warnings()
    parser = get_parser()
    args, unknown = parser.parse_known_args()

    pawn.console.log(args)

    args.try_pass = False
    pawn.set(
        args=args,
        try_pass=False,
        last_execute_point=0,
    )

    if args.verbose > 2:
        pawn.set(PAWN_DEBUG=True)
    # http.call_websocket(args.url, is_waiting=args.wait, blockheight=args.blockheight, url="/api/v3/icon_dex/block")

    http.GoloopWebsocket(
        # connect_url="http://20.20.1.242:9000",
        connect_url=args.url,
        blockheight=args.blockheight,
        monitoring_target=["tx"]

    ).run()



if __name__ == "__main__":
    main()
