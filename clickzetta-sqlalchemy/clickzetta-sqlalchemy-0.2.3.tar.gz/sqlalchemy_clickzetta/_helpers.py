import functools
import re

import sqlalchemy
import base64
import json
from clickzetta.client import Client
from clickzetta.enums import LoginParams

USER_AGENT_TEMPLATE = "sqlalchemy/{}"


def create_clickzetta_client(
        username=None,
        password=None,
        instance_name=None,
        workspace=None,
        vc_name=None,
        base_url=None,

):
    login_params = LoginParams(username, password, instance_name)
    return Client(
        login_params=login_params,
        workspace=workspace,
        instance_name=instance_name,
        vc_name=vc_name,
        base_url=base_url,
    )


def substitute_re_method(r, flags=0, repl=None):
    if repl is None:
        return lambda f: substitute_re_method(r, flags, f)

    r = re.compile(r, flags)

    @functools.wraps(repl)
    def sub(self, s, *args, **kw):
        def repl_(m):
            return repl(self, m, *args, **kw)

        return r.sub(repl_, s)

    return sub


def substitute_string_re_method(r, *, repl, flags=0):
    r = re.compile(r, flags)
    return lambda self, s: r.sub(repl, s)
