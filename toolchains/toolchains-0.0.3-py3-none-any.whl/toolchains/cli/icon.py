#!/usr/bin/env python3
import argparse
from pawnlib.builder.generator import generate_banner
from pawnlib.__version__ import __version__ as _version
from pawnlib.output.color_print import *
from pawnlib.config import pawnlib_config as pawn
from pawnlib.output import write_json
from pawnlib.resource import server
from pawnlib.typing.generator import json_rpc, random_token_address


icx_methods = ["account", "icx_sendTransaction", "get_transactionResult", "icx_getLastBlock", "icx_getBalance", "icx_getTotalSupply"]


class IconRpcTemplates:
    templates = {
        "main_api": {
            # "icx_getTotalSupply": json_rpc("icx_getTotalSupply"),
            "icx_getTotalSupply": {},
            "icx_getLastBlock": {},
            "icx_getBalance": {"params": {"address": ""}},
            "icx_getTransactionResult": {"params": {"txHash": ""}},
            "icx_getTransactionByHash": {"params": {"txHash": ""}},
            "icx_getBlockByHeight": {"params": {"height": ""}},
            "icx_getBlockByHash": {"params": {"hash": ""}},
            "icx_getScoreApi":  {"params": {"address": ""}},
            "icx_call": {"params": ""},
            "icx_sendTransaction":  {"params": {"from": "", "to": "", "stepLimit": "", "value": ""}},
            "icx_sendTransaction(SCORE)": {"method": "icx_sendTransaction"}
        },
        "IISS": {
            "setStake": dict(
                method="icx_sendTransaction",
                params={
                       "method": "setStake",
                       "params": {
                           "value": ""
                       }
                   }
               ),
        }
    }

    def __init__(self, category={}, method=None):
        self.return_rpc = {}
        self._category = category
        self._method = method
        self._params = {}
        self.get_rpc()

    def get_category(self):
        return list(self.templates.keys())

    def get_methods(self, category=None):
        methods = []
        for _category in self.get_category():
            if _category == category:
                return self.templates.get(_category).keys()
            methods += self.templates.get(_category).keys()
        return methods

    def create_rpc(self, params={}, method=None):

        pass

    def get_rpc(self, category=None, method=None):
        if category:
            self._category = category
        if method:
            self._method = method

        if self._category and self._method:

            if self.templates.get(self._category):
                _arguments = self.templates[self._category].get(method, {})
                if not isinstance(_arguments, dict):
                    raise ValueError(f"[Template Error] Syntax Error -> category={self._category}, method={self._method}")

                if not self._method:
                    raise ValueError(f"[Template Error] Required method ->  category={self._category}, method={self._method}")
                self._method = _arguments.get('method', self._method)
                self._params = _arguments.get('params', {})
                self.return_rpc = json_rpc(method=self._method, params=self._params)

                pawn.console.log(f"-- return_rpc {self.return_rpc}")

                return self.return_rpc
        return {}

    def get_required_params(self):
        return self._params


def get_parser():
    parser = argparse.ArgumentParser(description='ICON')
    parser = get_arguments(parser)
    return parser


def get_arguments(parser):
    parser.add_argument(
        'command',
        help='account, icx_sendTransaction, icx_sendTransaction_v3, get_transactionResult, icx_getBalance, icx_getTotalSupply',
        nargs='?'
    )
    parser.add_argument('--url', metavar='url',
                        help=f'loopchain baseurl. default: None', default=None)
    parser.add_argument('--from', metavar='address', dest='from_addr',
                        help=f'from address. default: None', default=None)
    parser.add_argument('--to', metavar='address', dest="to_addr",
                        help=f'to address. default: None', default=None)
    parser.add_argument('--address', metavar='address',
                        help=f'icx address. default: None', default=None)
    parser.add_argument('--txhash', metavar='txhash', help='txhash')
    parser.add_argument('--icx', metavar='amount', type=float,
                        help=f'icx amount to transfer. unit: icx. ex) 1.0. default:0.001', default=0.001)
    parser.add_argument('--fee', metavar='amount', type=float,
                        help='transfer fee. default: 0.01', default=0.001)
    parser.add_argument('--pk', metavar='private_key',
                        help=f'hexa string. default: None', default=None)
    parser.add_argument('--debug', action='store_true',
                        help=f'debug mode. True/False')
    parser.add_argument('-n', '--number', metavar='number', type=int,
                        help=f'try number. default: None', default=None)

    parser.add_argument('--nid', metavar='nid', type=str, help=f'network id default: None', default=None)

    parser.add_argument('-c', '--config', metavar='config',
                        help=f'config name')

    parser.add_argument('-k', '--keystore-name', metavar='key_store',
                        help=f'keystore file name')

    parser.add_argument('-p', '--password', metavar='password',
                        help=f'keystore file password')

    parser.add_argument('-t', '--timeout', metavar='timeout', type=float, help=f'timeout')
    parser.add_argument('-w', '--worker', metavar='worker', type=int, help=f'worker')
    parser.add_argument('-i', '--increase', metavar='increase_count', type=int, help=f'increase count number')
    parser.add_argument('--increase-count', metavar='increase_count', type=int, help=f'increase count number', default=1)

    parser.add_argument('-r', '--rnd_icx', metavar='rnd_icx', help=f'rnd_icx', default="no")
    return parser


def get_delivery_options(answers):
    options = ['bike', 'car', 'truck']
    if answers['size'] == 'jumbo':
        options.append('helicopter')
    return options


def get_methods(answers):
    icon_tpl = IconRpcTemplates()
    return icon_tpl.get_methods(answers['category'])


def get_required(answers):
    icon_tpl = IconRpcTemplates(category=answers['category'], method=answers['method'])
    pawn.console.log(f"get_required => {icon_tpl.get_required_params()}, {answers['category']}, {answers['method']}")

    return icon_tpl.get_required_params()

from PyInquirer import prompt, Separator


def main():
    banner = generate_banner(
        app_name="ICON",
        author="jinwoo",
        description="get the aws metadata",
        font="graffiti",
        version=_version
    )
    print(banner)

    parser = get_parser()
    args, unknown = parser.parse_known_args()

    pawn.console.log(f"args = {args}")

    icon_tpl = IconRpcTemplates()

    print(icon_tpl.get_category())
    print(icon_tpl.get_methods())

    if args.command == "icon":
        pawn.console.log("Interactive Mode")
        methods = icx_methods + [Separator()]
        questions = [
            {
                'type': 'list',
                'name': 'category',
                'message': 'What do you want to do?',
                'choices': icon_tpl.get_category() + ["wallet"],
                #     [
                #     'Order a pizza',
                #     'Make a reservation',
                #     Separator(),
                #     'Ask for opening hours',
                #     {
                #         'name': 'Contact support',
                #         'disabled': 'Unavailable at this time'
                #     },
                #     'Talk to the receptionist'
                # ]
            },
            {
                'type': 'list',
                'name': 'method',
                'message': 'Which vehicle you want to use for delivery?',
                # 'choices': lambda cate: icon_tpl.get_methods(answers['category']),
                'choices': get_methods,
            },
        ]

        answers = prompt(questions)
        dump(answers)
        payload = icon_tpl.get_rpc(answers['category'], answers['method'])
        required_params = icon_tpl.get_required_params()

        if required_params:
            _questions = []
            for k, v in required_params.items():
                _questions.append({'type': 'input', 'name': k.lower(), 'message': f'What\'s "{k}" parameter?'})
                # from 주소면 wallet 디렉토리를 읽어서 리스트를 보여준다.

            payload['params'] = prompt(_questions)

        pawn.console.log(f"payload={payload}")


if __name__ == '__main__':
    main()
