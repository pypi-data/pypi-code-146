#!/usr/bin/env python
# the module "subprocess" requires Python 2.4

import sys
import time
import traceback
import weakref

if True:  # avoids resortin by Isort
    # inject python 2 artefact:
    __builtins__["NoneType"] = type(None)
    import pyper
    from pyper import RError  # noqa: F401
    from pyper import R, _mystr, sendAll


# patch module global function:


def _readLine(p, **b):
    rv = _mystr(p.stdout.readline())
    if rv[0] not in ">[":
        sys.stdout.write(rv)
        sys.stdout.flush()
    return rv


pyper.readLine = _readLine


def on_die(prog, newline):
    try:
        if prog:
            print("send q() command")
            sendAll(prog, 'q("no")' + newline)
            time.sleep(0.5)
            prog.terminate()
            prog.poll()
            print("R interpreter shut down")
    except Exception:
        traceback.print_exc()


class PatchedR(R):
    def __init__(
        self,
        RCMD="R",
        max_len=1000,
        use_numpy=True,
        use_pandas=True,
        use_dict=None,
        host="localhost",
        user=None,
        ssh="ssh",
        return_err=True,
    ):
        super().__init__(
            RCMD, max_len, use_numpy, use_pandas, use_dict, host, user, ssh, return_err
        )
        self.install_del_callaback()

    def install_del_callaback(self):
        weakref.finalize(self, on_die, self.prog, self.newline)
