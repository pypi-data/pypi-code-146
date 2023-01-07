import sys
from collections import deque
from pathlib import Path

from . import MACROS
from .backend import run


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print("""Visual Sponge
    Visualization tool for SPONGE

usage: visual-sponge [MODEL [TRAJ [TRAJ2 [TRAJ3... ]]]] [-p PORT] [--debug] [-h] 

optionals:
    -h, --help:         show this help and exit
    MODEL:              the model (topology) file to load
    TRAJ:               the trajectory file to load
    -d, --debug:        the flag that enables the debug mode
    -p, --port:         the port to open. Default: 10696
""")
        sys.exit(0)
    files = deque()
    toskip = True
    for i, arg in enumerate(sys.argv):
        if toskip:
            toskip = False
            continue
        if arg in ("-p", "--port"):
            MACROS.PORT = int(sys.argv[i + 1])
            toskip = True
        elif arg in ("--debug", "-d"):
            MACROS.DEBUG_MODE = True
        else:
            files.appendleft(str(Path(arg)))

    run(files)

if __name__ == "__main__":
    main()
