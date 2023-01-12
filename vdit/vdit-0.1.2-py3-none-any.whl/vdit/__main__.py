from pyzbar.pyzbar import decode
from pyautogui import screenshot
from tkinter import Tk
from pathlib import Path

import subprocess
import argparse
import pyqrcode
import pyperclip

def get():
    img = screenshot()
    res= decode(img)
    if not res:
        print('no qr decode')
    else:
        for qr in res:
            txt = qr.data.decode()
            pyperclip.copy(txt)
            print(txt)

def set(txt:str):
    qr = pyqrcode.create(txt)
    dst = Path('set.png')
    qr.png(dst,scale=10)
    subprocess.run(f'start /wait {dst.name}',shell=True)
    dst.unlink()


def main():
    p = argparse.ArgumentParser()
    sub_p = p.add_subparsers(dest='cmd',required=True)
    set_p = sub_p.add_parser('set')
    get_p = sub_p.add_parser('get')
    set_p.add_argument('text',type=str)
    args = p.parse_args()

    if args.cmd == 'get':
        get()
    elif args.cmd == 'set':
        set(args.text)
    else:
        print(f'unhandled [{args.cmd}]')

if __name__ == '__main__':
    main()
