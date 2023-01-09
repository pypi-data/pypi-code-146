import re
import json
from .kry import get_type, start_thread
from .trans import anuvadak
def remove_in_between(val: str, start: str, end: str, md=0) -> str:
    """
    `md = 0` fom `Python`
    `md = 1` for `JavaScript`
    """
    md = ["#", "\/\/"][md]
    regex = re.compile(
        r"\n?(\s*?{0} ({1})\n).+?(\n\s*?{0} ({2}))".format(md, start, end),
        re.DOTALL,
    )
    return regex.sub("", val)


def remove_tags(val: str, nm: str, md=0) -> str:
    """
    `md = 0` fom `Python`
    `md = 1` for `JavaScript`
    """
    md = ["#", "\/\/"][md]
    regex = re.compile(r"\n?\s*?{1} ({0})(?=\n)".format(nm, md))
    return regex.sub("", val)


def remove_line_with_tag(val: str, nm: str, md=0) -> str:
    """
    `md = 0` fom `Python`
    `md = 1` for `JavaScript`
    """
    md = ["#", "\/\/"][md]
    regex = re.compile(r"\n?.*?{1} ({0})(?=\n)".format(nm, md))
    return regex.sub("", val)


def load_json(vl: str):
    return json.loads(vl)


def dump_json(vl, indnt=4, sort=False) -> str:
    return json.dumps(vl, indent=indnt, ensure_ascii=False, sort_keys=sort)


def dict_rev(d: dict) -> dict:
    """Reverse Dictionary ``keys`` and ``values``"""
    r = {}
    for x in d:
        r[d[x]] = x
    return r


def val_from_address(lc: str, vl: list):
    """This gets the value from a json adress `vl`"""
    n = vl
    lc = lc[1:].split("/")
    for x in lc:
        t = x
        if get_type(n) == "list":
            t = int(t)
        n = n[t]
    return n


def set_val_from_address(lc: str, vl: dict, val=None, make=False):
    """This sets the value at json adress"""
    n = vl
    lc = lc[1:].split("/")
    ln = len(lc)
    for i in range(ln):
        x = lc[i]
        t = x
        if get_type(n) == "list":
            t = int(t)
        if i == ln - 1:
            n[t] = val
        else:
            if t not in n and make:
                n[t] = {}
            n = n[t]


def json_to_adresses(v: dict):
    if v == None:
        return []
    r = []

    def prcs(x, n, pr=""):
        tp = get_type(n[x])
        v1 = f"{pr}/{x}"
        if tp == "list":
            lst(n[x], v1)
        elif tp == "dict":
            jsn(n[x], v1)
        else:
            r.append(f"{pr}/{x}")

    def jsn(n, pr=""):
        for x in n:
            prcs(x, n, pr)

    def lst(n, pr=""):
        for x in range(len(n)):
            prcs(x, n, pr)
    if get_type(v) == "dict":
        v = jsn(v)
    elif get_type(v) == "list":
        v = lst(v)
    else:
        raise ValueError
    return r


def process_json(
    v: dict,
    org: dict,
    src: str,
    to: str,
    no=None,
    yes=None,
    func=anuvadak,
    only_org=False,
):
    """`v` -> json, `org` -> original json to refer back"""
    """Function to translate `JSON` objects"""
    no = json_to_adresses(no)
    yes = json_to_adresses(yes)
    thrds = []

    def krym(t):
        return func(t, src, to)

    def check_yes_no(pr1):
        ok = False
        if yes != []:
            for u in yes:
                if u.count(pr1) > 0 or pr1.count(u) > 0:
                    ok = True
                    break
            ok = not ok
        if no != []:
            if pr1 in no:
                ok = True
        return ok

    def jsn(n, pr=""):
        n1 = {}
        for x in n:
            tp = get_type(n[x])
            v1 = ""
            pr1 = pr + "/" + x
            if check_yes_no(pr1) or only_org:
                tp = "no"
            if tp == "str":
                n1[x] = ""
                if n[x] == "":
                    continue

                def exec(sd):
                    n1[sd] = krym(n[sd])
                thrds.append(start_thread(lambda: exec(x)))
                continue
            elif tp == "dict":
                v1 = jsn(n[x], pr1)
            elif tp == "list":
                v1 = lst(n[x], pr1)
            else:
                try:
                    v1 = val_from_address(pr1, org)
                except:
                    print("value not found at", pr1)
                    v1 = ""
            n1[x] = v1
        return n1

    def lst(n, pr=""):
        n1 = []
        for x in range(len(n)):
            tp = get_type(n[x])
            v1 = ""
            pr1 = pr + f"/{x}"
            if check_yes_no(pr1):
                tp = "no"
            if tp == "str":
                n1.append("")
                if n[x] == "":
                    continue

                def exec(sd):
                    n1[sd] = krym(n[sd])
                thrds.append(start_thread(lambda: exec(x)))
                continue
            elif tp == "bool":
                n1[x] = n[x]
            elif tp == "dict":
                v1 = jsn(n[x], pr1)
            elif tp == "list":
                v1 = lst(n[x], pr1)
            else:
                try:
                    v1 = val_from_address(pr1, org)
                except:
                    print("value not found at", pr1)
                    v1 = ""
            n1.append(v1)
        return n1
    if get_type(v) == "dict":
        v = jsn(v)
    elif get_type(v) == "list":
        v = lst(v)
    else:
        raise ValueError
    for x in thrds:
        x.join()
    return v
