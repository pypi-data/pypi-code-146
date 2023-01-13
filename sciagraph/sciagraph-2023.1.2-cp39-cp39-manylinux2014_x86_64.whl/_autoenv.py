"""
Infrastructure for automatically running sciagraph based on an environment
variable, and for automatic initialization on startup.
"""

import os
import sys
import logging
import ctypes


def _check_user_configured_mode_via_env_var():
    """
    Translate a SCIAGRPAH_MODE environment variable into the relevant
    ``python -m sciagraph`` command-line options.

    This will run in the original process started by the user.
    """
    mode = os.environ.pop("SCIAGRAPH_MODE", None)
    if mode is None:
        return
    if mode not in {"process", "api", "celery"}:
        logging.error(
            "The SCIAGRAPH_MODE environment variable only supports the values"
            f" 'process' and 'api', but you set it to {mode!r}, exiting."
        )
        os._exit(1)

    import ctypes

    # TODO: Python 3.10 and later have sys.orig_argv.
    _argv = ctypes.POINTER(ctypes.c_wchar_p)()
    _argc = ctypes.c_int()
    ctypes.pythonapi.Py_GetArgcArgv(ctypes.byref(_argc), ctypes.byref(_argv))
    argv = _argv[: _argc.value]
    args = [f"--mode={mode}", "run"] + argv[1:]
    from .__main__ import main

    try:
        main(args)
    except SystemExit as e:
        if len(e.args) == 1 and isinstance(e.args[0], str):
            sys.stderr.write(e.args[0] + "\n")
            sys.stderr.flush()
            os._exit(1)
        raise


_check_user_configured_mode_via_env_var()


def _initialize(start_job: bool):
    """Initialize Sciagraph inside a new process."""
    # TODO replace with pyo3 module, better handling of e.g. panics!
    exe = ctypes.PyDLL(None)
    initialize = exe.sciagraph_initialize
    initialize.argtypes = [ctypes.c_int]
    initialize.restype = None
    initialize(1 if start_job else 0)


def _check_initialization():
    """
    Check how and if we need to initialize Sciagraph, and do the needful.

    This will run in the final, runtime process created by
    ``python -m sciagraph run``.
    """
    # __SCIAGRAPH_INITIALIZE is set in __main__.py:
    value = os.environ.pop("__SCIAGRAPH_INITIALIZE", None)
    if value is None:
        return

    if value in ("process", "api"):
        _initialize(value == "process")
        return

    if value == "celery":
        # The parent worker process should _not_ run Sciagraph. We want only
        # child processes (the prefork pool) to do so... and we don't want
        # _their_ children to register, either.
        def initialize_only_once(initialized=[]):
            """
            Only initialize once, and not again in worker subprocesses that do
            another fork() 😱.
            """
            if initialized:
                return
            initialized.append(True)
            _initialize(False)

        os.register_at_fork(after_in_child=initialize_only_once)
        return

    logging.error(f"__SCIAGRAPH_INITIALIZE is {value}, this is a bug.")
    os._exit(1)


_check_initialization()
