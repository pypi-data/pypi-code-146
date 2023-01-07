import json
from collections.abc import KeysView
from textwrap import wrap


def stringify(d: object, max_len=200):
    if isinstance(d, KeysView):
        d = list(d)

    s = json.dumps(d)
    if len(s) > max_len:
        if isinstance(d, list):
            s = s[:max_len] + " ...]"
        elif isinstance(d, dict):
            s = s[:max_len] + " ...}"
        else:
            s = s[:max_len] + " ..."
    return s


def wprint(text):
    lstats = []
    for idx, wrapped_text in enumerate(wrap(text)):
        lstats.append(len(wrapped_text))
        if idx == 0:
            print(wrapped_text)
        else:
            print(f"  {wrapped_text}")

    return lstats
