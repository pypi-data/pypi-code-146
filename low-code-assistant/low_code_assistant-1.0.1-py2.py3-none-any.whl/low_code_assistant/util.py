import os
import re
from keyword import iskeyword
from typing import Any, Callable, Dict, List

import reacton
import reacton.ipyvuetify as v
import solara.util as sutil

from .settings import settings


def get_nb_locals():
    def get_frame():
        try:
            assert False
        except Exception as e:
            return e.__traceback__.tb_frame if e.__traceback__ is not None else None

    def find_nb_locals(current):
        while current is not None:
            if current.f_locals.get("__doc__") == "Automatically created module for IPython interactive environment":
                return current.f_locals

            current = current.f_back

    return find_nb_locals(get_frame())


nb_locals = get_nb_locals()


def get_vars(filter: Callable[[Any], bool]):
    return [k for k, v in nb_locals.items() if not re.search(r"^_.*$", k) and k != "Page" and filter(v)]


def generate_var_name(prefix):
    count = 0
    while True:
        count += 1
        name = f"{prefix}_{count}"
        if [x for x in get_vars(lambda v: True) if x == name]:
            continue
        return name


logo = sutil.load_file_as_data_url(os.path.join(os.path.dirname(__file__), "DominoLogoWhite.svg"), "image/svg+xml")

logo_grey = sutil.load_file_as_data_url(os.path.join(os.path.dirname(__file__), "DominoLogoGrey.svg"), "image/svg+xml")


@reacton.component
def DominoHeader(title, show_logo=True):
    main = v.CardTitle(
        class_="text-h5",
        style_="background-color: #2d71c7; color: white",
        children=[
            title,
            *(
                [
                    v.Spacer(),
                    v.Img(
                        src=logo,
                        style_="height: 32px; max-width: 32px; border-radius: 16px",
                    ),
                ]
                if show_logo
                else []
            ),
        ],
    )
    return main


def eq_by_ref(a, b):
    return a is b


def copy_upload(file_obj, name):
    import errno
    import shutil
    from datetime import datetime

    now = datetime.now()
    dt_string = now.strftime("%Y%m%d%H%M%S")
    data_dir = os.path.join(settings.domino_working_dir, "low_code_assistant_data")
    try:
        os.makedirs(data_dir)
    except OSError as e:
        if not e.errno == errno.EEXIST:
            raise
    dest_name = os.path.join(data_dir, dt_string + "_" + name)
    destination = open(dest_name, "wb")
    shutil.copyfileobj(file_obj, destination)

    return dest_name


def python_safe_name(name, used=None):
    if used is None:
        used = []
    first, rest = name[0], name[1:]
    name = re.sub("[^a-zA-Z_]", "_", first) + re.sub("[^a-zA-Z_0-9]", "_", rest)
    if name in used:
        nr = 1
        while name + ("_%d" % nr) in used:
            nr += 1
        name = name + ("_%d" % nr)
    return name


def in_dev_mode():
    return settings.low_code_assistant_dev


def remove_keys(d: Dict, keys: List[str]):
    return {k: v for k, v in d.items() if k not in keys}


def is_valid_variable_name(name):
    return name.isidentifier() and not iskeyword(name)
