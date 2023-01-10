import os


def where_hosted():
    if os.getenv("DYNO"):
        return "Heroku"
    if os.getenv("RAILWAY_STATIC_URL"):
        return "Railway"
    if os.getenv("KUBERNETES_PORT"):
        return "Qovery"
    if os.getenv("WINDOW") and os.getenv("WINDOW") != "0":
        return "Windows"
    if os.getenv("RUNNER_USER") or os.getenv("HOSTNAME"):
        return "Github actions"
    if os.getenv("ANDROID_ROOT"):
        return "Termux"
    return "VPS"


if where_hosted() == "VPS":
    def _ask_input():
        # Ask for Input even on Vps and other platforms.
        def new_input(*args, **kwargs):
            raise EOFError("args=" + str(args) + ", kwargs=" + str(kwargs))

        __builtins__["input"] = new_input

    _ask_input()
