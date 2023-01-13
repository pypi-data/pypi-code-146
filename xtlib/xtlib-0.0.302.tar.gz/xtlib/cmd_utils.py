#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# cmd_utils.py: support code spliting xt cmd into args and back again

import shlex
from xtlib.console import console

def user_cmd_split(cmd):
    # split on spaces, unless protected by quotes or []
    parts = []

    part = ""
    protector = None

    for ch in cmd:
        if protector:
            # spaces are protected
            part += ch
            if ch == protector:
                protector = None
        else:
            # spaces are separators
            if ch == " ":
                parts.append(part)
                part = ""
            else:
                part += ch
                if ch in ["'", '"']:
                    protector = ch
                elif ch == "[":
                    protector = "]"

    # add last part, if any
    if part:
        parts.append(part)

    # cleanup parts
    cmd_parts = []

    for i, part in enumerate(parts):
        part = part.strip()
        if part:
            if part.startswith("'") and part.endswith("'"):
                part = part[1:-1]
            elif part.startswith('"') and part.endswith('"'):
                part = part[1:-1]

            cmd_parts.append(part)

    return cmd_parts

def xt_cmd_split(cmd):
    # shlex and LINUX SHELL lose single quotes around strings, but windows does not
    # shlex also zaps single backslashes
    cmd = cmd.replace("\\", "\\\\")    # double backslashes to prevent their removal

    args = shlex.split(cmd)
    console.diag("shlex args={}".format(args))

    # now, undouble backslashes
    for a, arg in enumerate(args):
        if "\\\\" in arg:
            args[a] = arg.replace("\\\\", "\\")

    args = add_back_quotes(args)
    return args

def join_args(args):
    cmd = " ".join(args)
    return cmd

def text_needs_quotes(text):
    needed = False
    has_quotes = text[0] in "'`\""
    if not has_quotes:
        for ch in " <>!=:":
            if ch in text:
                needed = True
                break

    return needed

def add_quotes_around_text(text):

    if text.endswith(","):
        # don't quote the ending comma
        text = '"{}",'.format(text[0:-1])
    else:
        text = '"{}"'.format(text)

    return text

def add_back_quotes(args):

    # add back quotes where needed 
    for a, arg in enumerate(args):
        if "=" in arg:
            name, value = arg.split("=", 1)
            if text_needs_quotes(value):
                value = add_quotes_around_text(value)
                args[a] = "{}={}".format(name, value)

        # ensure it is not already quoted
        elif text_needs_quotes(arg):
            args[a] = add_quotes_around_text(arg)

    return args

