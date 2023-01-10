#!/usr/bin/env python3
import argparse
from pawnlib.builder.generator import generate_banner
from pawnlib.__version__ import __version__ as _version
from pawnlib.output.color_print import *
from pawnlib.typing import check
from pawnlib.config import pawnlib_config as pawn
from pawnlib import output
from pawnlib.resource import server
from pawnlib.typing.generator import json_rpc, random_token_address, random_private_key
from toolchains.utils import icx_signer, generate_wallet
from PyInquirer import prompt, Separator
from dataclasses import dataclass
import glob

from pawnlib.utils.operate_handler import run_with_keyboard_interrupt


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
    parser.add_argument('--address', metavar='address',
                        help=f'icx address. default: None', default=None)
    parser.add_argument('--pk', metavar='private_key',
                        help=f'hexa string. default: None', default=None)
    parser.add_argument('--debug', action='store_true',
                        help=f'debug mode. True/False')
    parser.add_argument('-c', '--config', metavar='config',
                        help=f'config name')
    parser.add_argument('-k', '--keystore-name', metavar='key_store',
                        help=f'keystore file name')
    parser.add_argument('-p', '--password', metavar='password',
                        help=f'keystore file password')
    return parser


def simple_prompt(type="type", message="", name="", default=""):
    return prompt(
        {
            "type": type,
            "message": message,
            "name": name,
            "default": default
        }
    )[name]


def prompt_with_keyboard_interrupt(*args, **kwargs):
    answer = prompt(*args, **kwargs)
    # pawn.console.log(f"answer = {answer}")
    if not answer:
        raise KeyboardInterrupt

    if isinstance(args[0], dict):
        arguments = args[0]
    else:
        arguments = args[0][0]

    if isinstance(answer, dict) and len(answer.keys()) == 1 and arguments and arguments.get('name'):
        return answer.get(arguments['name'])

    return answer


def private_key_validator(private_key):
    if icx_signer.is_private_key(private_key) or private_key == "":
        return True
    return "Invalid private key "


@dataclass
class WalletInput:

    params = {
        "Load wallet": [
            {
                "type": "list",
                "name": "keystore_type",
                "message": "How to load the keystore?",
                "choices": ["From JSON File", "Input the Text (Copy & Paste)"]
            },
            # {
            #     "type": "input",
            #     "name": "keystore",
            #     # "message": "What\'s your keystore file?",
            #     # "message": "Enter your keystore file(or JSON or private_key)",
            #     "message": "Enter your keystore",
            # },

        ],
        "Create wallet": [
            {
                "type": "password",
                "name": "private_key",
                "message": "Enter private key (default: random)",
                "validate": lambda text: (icx_signer.is_private_key(text) or text == "") or 'Invalid PrivateKey',
                # "validate": private_key_validator
            },
            {
                "type": "password",
                "name": "password",
                "message": "Enter password",
                "validate": lambda text: len(text) >= 1 or 'Must be at least 1 word(s).',
            }
        ]
    }

    def get(self, key):
        return self.params.get(key)

    def keys(self):
        return list(self.params.keys())


def main_program():
    banner = generate_banner(
        app_name="WALLET",
        author="jinwoo",
        description="Wallet tools",
        font="graffiti",
        version=_version
    )
    print(banner)
    parser = get_parser()
    args, unknown = parser.parse_known_args()
    pawn.console.log(f"args = {args}")

    if args.command == "wallet":
        pawn.console.log("Interactive Mode")
        wallet_input = WalletInput()
        questions = [
            {
                'type': 'list',
                'name': 'sub_command',
                'message': 'What do you want to do?',
                'choices': wallet_input.keys(),
            }
        ]
        sub_command = prompt_with_keyboard_interrupt(questions)
        _questions = []

        for _input in wallet_input.get(sub_command):
            _questions.append(_input)

        data = prompt_with_keyboard_interrupt(_questions)

        if sub_command == "Load wallet":
            keystore_json = {}
            _required_password = False
            # keystore = data['keystore']
            password = None

            if data == "From JSON File":
                regex_file = "*.json"
                json_file_list = glob.glob(regex_file)
                if len(json_file_list) <= 0:
                    raise ValueError(f"[red] Cannot found JSON file - '{regex_file}'")

                keystore = prompt_with_keyboard_interrupt({
                    "type": "list",
                    "name": "keystore",
                    "message": "Select the keystore type",
                    "choices": json_file_list
                })
                _required_password = True
            else:
                keystore = prompt_with_keyboard_interrupt({
                    "type": "input",
                    "name": "keystore",
                    "message": "Input the keystore json or private key",
                    "validate": lambda text: len(text) >= 1 or 'Must be at least 1 word(s).',
                })
            if keystore:
                keystore = str(keystore).strip()
                if output.is_file(keystore):
                    pawn.console.log(f"Found Keystore file - {keystore}")
                    try:
                        keystore_json = output.open_json(keystore)
                    except ValueError:
                        pawn.console.log(f"[red]Invalid JSON file - {keystore}")
                    _required_password = True
                elif icx_signer.is_private_key(keystore):
                    pawn.console.log(f"Found Private key")
                    keystore_json = keystore
                    _required_password = False
                else:
                    try:
                        keystore_json = json.loads(keystore)
                        if isinstance(keystore_json, dict):
                            pawn.console.log("[green][OK] Loaded keystore file - JSON object")
                        else:
                            raise ValueError("Invalid JSON or Keystore text")
                        _required_password = True
                    except Exception as e:
                        raise ValueError(f"[red][Error] cannot load - {e}")

            if _required_password:
                password = prompt_with_keyboard_interrupt(
                    dict(type="password", message="Enter your password", name='password')
                )

            if keystore_json:
                res = icx_signer.load_wallet_key(keystore_json, password)
                if res:
                    pawn.console.log(f"Loaded wallet")
                    dump(res)
                else:
                    pawn.console.log(f"[red][ERROR] Not Loaded wallet")

        elif sub_command == "Create wallet":
            if not data['private_key']:
                pawn.console.log(f"Generate the random private key")
                private_key = random_private_key()
            elif icx_signer.is_private_key(data['private_key']):
                private_key = data['private_key']
            else:
                pawn.console.log("[red] Invalid private key")
                sys.exit()
            wallet = icx_signer.load_wallet_key(private_key, password=data['password'])
            pawn.console.log(f"address={wallet.get('address')}, private_key={private_key}")

            default_filename = f"{wallet.get('address')}_{date_utils.todaydate('ms_text')}.json"
            keystore_filename = prompt_with_keyboard_interrupt(
                dict(type="input", message="Enter filename of keystore?", default=default_filename, name="keystore_filename")
            )

            output.check_file_overwrite(filename=keystore_filename)

            try:
                generate_wallet(file_path=default_filename, password=data['password'], overwrite=False, private_key=private_key)
            except Exception as e:
                pawn.console.log(f"[red][ERROR] Generate wallet - {e}")


def main():
    run_with_keyboard_interrupt(main_program)


if __name__ == '__main__':
    main()

