import argparse
import os
from typing import Any

import pyautogui


def get_args() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('function', help='The function name of pyautogui')
    parser.add_argument('argument', nargs='?', help='The literal argument of the function')
    return parser.parse_args()


def main() -> int:
    args: argparse.Namespace = get_args()
    res: Any = getattr(pyautogui, args.function)(eval(args.argument))
    if res is not None:
        print(res)
    return os.EX_OK
