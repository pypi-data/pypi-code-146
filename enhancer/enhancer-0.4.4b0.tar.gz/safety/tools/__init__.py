"""

This Is For Security Purpose Only
As Many Noobs Using Cheap Tricks To Hack userbot.
We here to save them

~ @TeamUltroid

"""

# Lol You Are So desperate.
# You came all here just to see this
# 😂😂😂😂

import os, enum, sys, signal, atexit
from .._python.builtin import List
from .._python.refresher import _get_session, _clear_session
_discared = ["API_ID","API_HASH","SESSION", "VC_SESSION", "REDIS_PASSWORD", "REDISPASSWORD", "HEROKU_API", "BOT_TOKEN", "MONGO_URI","DATABASE_URL"]

__env = {}
_get_sys = {}
_argv = []

def bring_back_dot_env():
    if __env:
        with open(".env", "w") as f:
            f.write(__env["_"])

def sys_exit(useless = 0):
    bring_back_dot_env()
    print("Exiting System")
    os._exit(0)

# Class Var Clean up
def cleanup_cache(what_u_doing_here=None):
    from pyUltroid.configs import Var
    from pyUltroid import ultroid_bot, asst, vcClient
    try:
#       for sig in (signal.SIGHUP, signal.SIGTERM, signal.SIGINT, signal.SIGUSR1, signal.SIGHUP, signal.SIGILL, signal.SIGBUS, signal.SIGSEGV):
#            asst.loop.add_signal_handler(sig, lambda _sig=sig: sys_exit())
#        atexit.register(sys_exit)
        for i in [ultroid_bot, asst, vcClient]:
            if i:
                setattr(i, "refresh_auth", _get_session)
                setattr(i, "clear_auth", _clear_session)
                i.clear_auth(i)
        os_stuff()
#        if os.path.exists(".env"):
#            rem = open(".env", "r").read()
#            __env.update({"_":rem})
#            os.remove(".env")
        _argv.append(sys.argv)
        if len(sys.argv) > 1:
            sys.argv = [sys.argv[0], sys.argv[-1]]
        for z in _discared:
            if z in Var.__dict__.keys():
                _get_sys.update({z: Var.__dict__[z]})
                setattr(Var, z, "")
    except SystemExit:
        sys_exit()

# Env clean up
def os_stuff():
    all = os.environ
    for z in all.keys():
        for zz in _discared:
            if zz in z:
                all.update({z: ""})

# Getting them back for re-start & soft update
def call_back():
    if _argv:
        sys.argv = _argv[0]
    from pyUltroid.configs import Var
#    if __env:
#        open(".env", "w").write(__env["_"])
    for z in _get_sys:
        if _get_sys[z]:
            setattr(Var, z, str(_get_sys[z]))
            os.environ[z] = str(_get_sys[z])
    

class KEEP_SAFE:
    @property
    def All(self):
        return List([
    "_ignore_eval",
    "SESSION",
    "BOT_TOKEN",
    "VC_SESSION",
    "DeleteAccountRequest",
    "HEROKU_API",
    "base64",
    "bash",
    "call_back",
    "get_me\(",
    'get_entity("me")',
    "get_entity('me')", 
    "exec",
    "REDIS_PASSWORD",
    "load_addons",
    "load_other_plugins",
    "os.system",
    "subprocess",
    "await locals()",
    "aexec",
    ".session.save()",
    ".auth_key.key",
    "INSTA_PASSWORD",
    "INSTA_SET",
    "SUDOS", 
    "FULLSUDO",
    "KEEP_SAFE",
    ".flushall",
    "_get_sys",
    ".env",
    "DEVLIST",
    "Secure()"])

class Secure:
    @property
    def Values():
        return List([key for key in _get_sys.values() if key])

enum._make_class_unpicklable(KEEP_SAFE)

__all__ = ["KEEP_SAFE", "cleanup_cache", "call_back"]
