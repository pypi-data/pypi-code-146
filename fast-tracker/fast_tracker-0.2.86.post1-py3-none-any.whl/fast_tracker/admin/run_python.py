# -*- coding: utf-8 -*-

from __future__ import print_function

from fast_tracker.admin import command


@command(
    "run-python",
    "...",
    """使用提供的参数执行Python解释器,启动时会强行初始化代理. 环境变量FastTrackerConfigPath可以提供代理配置文件的路径,日志文件的详情由FAST_LOG提供""",
)
def run_python(args):
    import os
    import sys
    import time

    startup_debug = os.environ.get("FAST_STARTUP_DEBUG", "off").lower() in (
        "on",
        "true",
        "1",
    )

    fast_debug_level = int(os.environ.get("FastTracker_Debug_Level", "0"))


    def log_message(text, *args, level=1):
        if startup_debug and fast_debug_level >= level:
            text = text % args
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print("FAST: %s (%d) - %s" % (timestamp, os.getpid(), text))

    log_message("FAST Boot Script (%s)", __file__)

    log_message("working_directory = %r", os.getcwd())
    log_message("current_command = %r", sys.argv)

    log_message("sys.prefix = %r", os.path.normpath(sys.prefix))

    try:
        log_message("sys.real_prefix = %r", sys.real_prefix)
    except AttributeError:
        pass

    log_message("sys.version_info = %r", sys.version_info)
    log_message("sys.executable = %r", sys.executable)
    log_message("sys.flags = %r", sys.flags)
    log_message("sys.path = %r", sys.path)

    for name in sorted(os.environ.keys()):
        if name.startswith("FAST_") or name.startswith("PYTHON"):
            log_message("%s = %r", name, os.environ.get(name))

    from fast_tracker import __file__ as root_directory

    root_directory = os.path.dirname(root_directory)
    boot_directory = os.path.join(root_directory, "bootstrap")

    log_message("root_directory = %r", root_directory)
    log_message("boot_directory = %r", boot_directory)

    python_path = boot_directory

    if "PYTHONPATH" in os.environ:
        path = os.environ["PYTHONPATH"].split(os.path.pathsep)
        if not boot_directory in path:
            python_path = "%s%s%s" % (
                boot_directory,
                os.path.pathsep,
                os.environ["PYTHONPATH"],
            )

    os.environ["PYTHONPATH"] = python_path

    os.environ["FAST_ADMIN_COMMAND"] = repr(sys.argv)

    os.environ["FAST_PYTHON_PREFIX"] = os.path.realpath(os.path.normpath(sys.prefix))
    os.environ["FAST_PYTHON_VERSION"] = ".".join(map(str, sys.version_info[:2]))

    bin_directory = os.path.dirname(sys.argv[0])

    if bin_directory:
        python_exe = os.path.basename(sys.executable)
        python_exe_path = os.path.join(bin_directory, python_exe)
        if not os.path.exists(python_exe_path) or not os.access(
            python_exe_path, os.X_OK
        ):
            python_exe_path = sys.executable
    else:
        python_exe_path = sys.executable

    log_message("python_exe_path = %r", python_exe_path)
    log_message("execl_arguments = %r", [python_exe_path, python_exe_path] + args)

    os.execl(python_exe_path, python_exe_path, *args)
