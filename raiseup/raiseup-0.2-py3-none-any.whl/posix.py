import errno
import os
import sys
try:
    from shlex import quote
except ImportError:
    from pipes import quote


def quote_shell(args):
    return " ".join(quote(arg) for arg in args)


def quote_applescript(string):
    charmap = {
        "\n": "\\n",
        "\r": "\\r",
        "\t": "\\t",
        "\"": "\\\"",
        "\\": "\\\\",
    }
    return '"%s"' % "".join(charmap.get(char, char) for char in string)


def elevate(file_path,show_console=True, graphical=True):
    if os.getuid() == 0:
        return

    args = [sys.executable, os.path.realpath(file_path)]
    commands = []

    if graphical:
        if sys.platform.startswith("darwin"):
            commands.append([
                "osascript",
                "-e",
                "do shell script %s "
                "with administrator privileges "
                "without altering line endings"
                % quote_applescript(quote_shell(args))])

        if sys.platform.startswith("linux") or sys.platform.startswith("freebsd"):
            commands.append(["pkexec"]+["env"]+["DISPLAY="+os.environ.get("DISPLAY")]+["XAUTHORITY="+os.environ.get("XAUTHORITY")]+args)
            commands.append(["gksudo"] + args)
            commands.append(["kdesudo"] + args)

    commands.append(["sudo"] + args)
    commands.append(["doas"] + args)

    for args in commands:
        try:
            os.execlp(args[0].split()[0], *args)
        except OSError as e:
            print(e)
            if e.errno != errno.ENOENT or args[0] == "sudo":
                raise
