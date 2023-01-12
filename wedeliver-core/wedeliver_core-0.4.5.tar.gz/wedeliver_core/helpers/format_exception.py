import inspect
from datetime import datetime
from sys import platform
from wedeliver_core import WeDeliverCore
from flask import request


def format_exception(exception, user=None, status_code=None, soft_message=None):
    app = WeDeliverCore.get_app()
    user = user or dict()
    try:
        caller_frame = request.path
    except Exception:
        try:
            caller_frame = inspect.currentframe()
            caller_frame = inspect.getouterframes(caller_frame, 2)[1][3]
        except Exception:
            caller_frame = "Unknown"

    try:
        ip = request.remote_addr
    except Exception:
        ip = "Unknown"
    try:
        args = str(request.args)[:1000]
    except Exception:
        args = "Unknown"
    try:
        form = str(request.form)[:1000]
    except Exception:
        form = "Unknown"
    try:
        user_id = "{0} - {1} - {2}".format(
            user.get("email"),
            user.get("mobile"),
            user.get("user_id"),
        )
    except Exception:
        user_id = "Unknown"
    try:
        role = user.get("role")
    except Exception:
        role = "Unknown"
    try:
        node = platform if type(platform) is str else str(platform.node())
    except Exception:
        node = "Unknown"

    if status_code:
        status_code = "\nStatus Code: {0}".format(status_code)
    if soft_message:
        soft_message = "\nSoft Message: {0}".format(soft_message)

    return """Node: {node}
Time: {_time}
Env: {env}
IP: {ip}
API: {call}
User: {user}
Role: {role}
Args: {args}
Form: {form}{status_code}{soft_message}
Error: {error}""".format(
        env=app.config.get("FLASK_ENV"),
        call=caller_frame,
        user=user_id,
        role=role,
        node=node,
        _time=str(datetime.now()),
        ip=ip,
        args=args,
        form=form,
        error=exception,
        status_code=status_code or "",
        soft_message=soft_message or "",
    )
