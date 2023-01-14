"""
Python SDK
"""

__version__ = "0.2.0"
__author__ = "Extrinsec LLC"
__credits__ = "Extrinsec LLC"

import json
import os
import pkgutil
import platform
import tempfile
from ctypes import cdll

if "extrinsec-appguard" in os.getenv("AWS_LAMBDA_EXEC_WRAPPER", ""):
    raise ValueError("appGuard SDK cannot be used together with the appGuard AWS Lambda extension")

def supported():
    architectures = ["x86_64", "arm64", "aarch64" ]
    provider_envs = ["AWS_EXECUTION_ENV",           # AWS Lambda
                    "K_SERVICE",                    # Google Cloud Functions
                    "FUNCTIONS_WORKER_RUNTIME",     # Azure
                    '__OW_ACTION_NAME'             # DigitalOcean/OpenWhisk
                    ]
    return platform.system().lower() == 'linux' and platform.machine().lower() in architectures and any(map(lambda env: os.environ.get(env), provider_envs))

if supported():
    # set env vars
    os.environ["ES_RUNTIME_LANGUAGE"] = "PYTHON"
    os.environ["ES_RUNTIME_LANGUAGE_VERSION"] = platform.python_version()
    os.environ["ES_APP_DIR"] = os.getcwd()
    os.environ["ES_SDK_VERSION"] = __version__

    arch = platform.machine()
    libc = 'musl' if os.popen('. /etc/os-release && echo $ID').read().strip() == 'alpine' else 'gnu'
    suffix = f"{arch}.{libc}"
    dir_path = os.path.dirname(os.path.realpath(__file__))
    app_guard_path = os.path.join(dir_path, "lib", f"libcore.{suffix}.so")

    if not os.path.isfile(app_guard_path):
        app_guard_path = os.path.join(tempfile.gettempdir(), f"libcore.{suffix}.so")
        with open(app_guard_path, "wb") as app_guard_lib_file:
            app_guard_lib_file.write(pkgutil.get_data(__name__, f"lib/libcore.{suffix}.so"))

    app_guard_lib = cdll.LoadLibrary(app_guard_path)
    print("[INFO] [appGuard] Python SDK version: " + os.environ["ES_SDK_VERSION"])

else:
    err_msg_unsupported_runtime_env = "[ERROR] [appGuard] only Linux x64/arm64 systems on AWS Lambdas, Google Cloud Functions, or Azure Functions are supported."
    print(err_msg_unsupported_runtime_env)
    raise ValueError(err_msg_unsupported_runtime_env)
