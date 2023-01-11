"""Main module."""

import os
import pathlib
import subprocess as sp
from time import sleep
import re
import json
import sys
import click
import signal

_PID_FILE = "jupyter.pid"
_JUPYTER_LOG = "jupyter.log"
_JMANAGER_LOG = "jmanager.log"


def receiveSignal(signalNumber, frame):
    if not os.path.isfile(_PID_FILE):
        return
    with open(_PID_FILE) as f:
        pid = json.load(f)
    with open(_JMANAGER_LOG) as f:
        f.write(
            f"receiving signal {signalNumber}. removing {_PID_FILE}. it's contents was {json.dumps(pid)}")
    os.remove(_PID_FILE)


class TooManyTrial(Exception):
    pass


class Launcher:
    def __init__(self):
        pass

    def __del__(self):
        os.remove(_PID_FILE)

    def launch(self, internet):
        cmd = ["jupyter", "lab"]
        if internet:
            cmd.append('--ip=*')
        with open(_JUPYTER_LOG, "w") as f:
            po = sp.Popen(cmd,
                          stdout=f,
                          stderr=sp.STDOUT,
                          text=True)
        n_try = 0
        port, token = None, None
        while True:
            if n_try >= 100:
                raise TooManyTrial()
            with open(_JUPYTER_LOG) as f:
                for l in f:
                    r = re.match(
                        r"^\s+http://.+:([0-9]+)/lab\?token=([0-9a-z]+)$", l)
                    if r:
                        port, token = r.expand(r"\1"), r.expand(r"\2")
                        break
            if port is not None:
                break
            else:
                n_try += 1
                sleep(1)
        with open(_PID_FILE, "w") as f:
            dat = dict(
                pid=po.pid,
                port=int(port),
                token=token
            )
            json.dump(dat, f)
        signal.signal(signal.SIGTERM, receiveSignal)
        po.wait()


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        run()


@main.command(help="Terminate jupyter process")
def kill():
    work_dir = find_pid_file(os.getcwd())
    if work_dir is not None:
        with open(os.path.join(work_dir, _PID_FILE)) as f:
            pid = json.load(f)
        sp.Popen(["kill", "-9", str(pid["pid"])])


def open_browser():
    with open(_PID_FILE) as f:
        dat = json.load(f)
    url = f"http://localhost:{dat['port']}/?token={dat['token']}"
    sys.stderr.write(json.dumps(dat) + "\n")
    sys.stderr.write(url + "\n")
    sp.Popen(["open", url])


@main.command(hidden=True)
@click.option("--internet/--nointernet", "-i", default=False, type=bool)
def launch(internet):
    launcher = Launcher()
    launcher.launch(internet)


def find_pid_file(dir_path: str) -> str | None:
    path = os.path.join(dir_path, _PID_FILE)
    if os.path.exists(path):
        return dir_path
    current = pathlib.Path(dir_path)
    if current == pathlib.Path("/"):  # current cwd is root
        return None
    else:
        return find_pid_file(str(current.parent))


@main.command(help="Launch new jupyter or connect to existing one.")
@click.option("--internet/--nointernet", "-i", default=False, type=bool)
def run(internet):
    if internet:
        opts = "--internet"
    else:
        opts = "--nointernet"
    work_dir = find_pid_file(os.getcwd())
    if work_dir is None:
        sys.stderr.write("launching new jupyter process\n")
        sp.Popen(["jmanager", "launch", opts])
    else:
        sys.stderr.write("jupyter process already run\n")
        os.chdir(work_dir)
        open_browser()


@main.command(help="Print lines for .gitignore")
def ignore():
    print(_PID_FILE)
    print(_JUPYTER_LOG)
    print(_JMANAGER_LOG)
