from pathlib import Path
import os
import subprocess as sub
import shutil
from .crypted import salt
from .kry import home, tool, IS_WINDOWS
import pyperclip as clip


def parent(loc: str) -> str:
    """Get Parent folder of the `loc`"""
    return Path(loc).parent


def file_name(loc: str) -> str:
    """Get file name of the `loc`"""
    return loc.split("\\")[-1]


def file_name1(loc: str) -> str:
    """Full length name of `loc`"""
    return loc.split(".")[0]


def file_exists(loc: str, create=False, val="") -> str:
    nm = file_name(loc)
    for x in os.listdir(parent(loc)):
        if x == nm:
            return True
    if create:
        write(loc, val)
    return False


def read(loc: str) -> str:
    f = open(loc, encoding="utf-8", mode="r+")
    v = f.read()
    f.close()
    return v


def write(loc: str, val: str):
    try:
        f = open(loc, encoding="utf-8", mode="w+")
        f.write(val)
        f.close()
    except FileNotFoundError:
        print("write location not found", loc)


def read_bin(loc: str) -> bytes:
    f = open(loc, mode="rb+")
    v = f.read()
    f.close()
    return v


def write_bin(loc: str, val: bytes):
    try:
        f = open(loc, mode="wb+")
        f.write(val)
        f.close()
    except FileNotFoundError:
        print("write location not found", loc)


def makedir(dir: str):
    try:
        os.makedirs(dir)
    except:
        pass


def delete_file(pth: str):
    try:
        os.remove(pth)
    except:
        print(pth, "not found")


def cmd(comm: str, direct=True, display=True, file=False):
    if file:
        try:
            TEMP_FOLDER_NAME = ".ofsfobnelippi_temp"
            fl_path = os.path.join(home(), TEMP_FOLDER_NAME, f"{salt()}.cmd")

            def write_script_file():
                try:
                    fl = open(fl_path, encoding="utf-8", mode="w+")
                    fl.write(("" if IS_WINDOWS else "#!/bin/bash\n")+comm)
                    fl.close()
                except:
                    os.makedirs(os.path.join(home(), TEMP_FOLDER_NAME))
                    write_script_file()
            write_script_file()
            if IS_WINDOWS:
                os.system(fl_path)
            else:
                os.system(f"sh {fl_path}")
        except:
            pass
        if os.path.isfile(fl_path):
            delete_file(fl_path)
    elif direct:
        p = sub.Popen(comm, stderr=sub.STDOUT, stdout=sub.PIPE, shell=True)
        dp = []
        while True:
            line = p.stdout.readline()[:-1]
            if not line:
                break
            dp.append(line.decode("utf-8"))
            if display:
                print(dp[-1])
        p.wait()
        return [p.returncode, "\n".join(dp)]
    else:
        os.system(comm)


def delete_folder(pth: str):
    try:
        shutil.rmtree(pth)
    except:
        print(pth, "not found")


def delete(pth: str):
    """Function to delete both files and folder"""
    if os.path.isdir(pth):
        shutil.rmtree(pth)
    elif os.path.isfile(pth):
        os.remove(pth)
    else:
        print(pth, "not found")


def copy_folder(frm: str, to: str, make=True):
    if make:
        makedir(to)
    shutil.copytree(frm, to, dirs_exist_ok=True)


def copy_file(frm: str, to: str, make=True):
    if make:
        if not os.path.isfile(to):
            makedir(parent(to))
            write_bin(to, b"")
    shutil.copy2(frm, to)


def copy(frm: str, to: str, make=True):
    """Function to copy both files and folder"""
    if os.path.isdir(frm):
        copy_folder(frm, to, make)
    elif os.path.isfile(frm):
        copy_file(frm, to, make)
    else:
        print(frm, "not found")


def clip_copy(val: str):
    clip.copy(val)


def clip_paste():
    return clip.paste()


def extract(fl: str, dest: str, direct=True):
    if IS_WINDOWS:
        cmd(f'"{tool}/7zip/7za.exe" x "{fl}" -o"{dest}" -y',
            display=False, direct=direct)
    else:
        cmd(f'7z x "{fl}" -o"{dest}" -y',
            display=False, direct=direct)
