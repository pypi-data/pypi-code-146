"""Provide ``setup()`` to
`sphinx <https://www.sphinx-doc.org/en/master/extdev/index.html>`_.
"""
from __future__ import annotations

import io
import os
from contextlib import redirect_stdout, suppress
from subprocess import check_output
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from sphinx.application import Sphinx

from ._version import __version__, __version_tuple__  # type: ignore
from .rst import RSTEvalParser

SH = os.getenv("SHELL", "sh")


def eval_sh(input: str) -> str:
    """Eval sh.

    :param input:
    :type input: str
    :rtype: str
    """
    try:
        output = check_output(  # nosec B603
            [SH, "-c", input], universal_newlines=True
        )
    except Exception:
        output = ""
    return output


def eval_bash(input: str) -> str:
    """Eval bash.

    :param input:
    :type input: str
    :rtype: str
    """
    try:
        output = check_output(  # nosec B603 B607
            ["bash", "-c", input], universal_newlines=True
        )
    except Exception:
        output = ""
    return output


def eval_python(input: str) -> str:
    """Eval python.

    :param input:
    :type input: str
    :rtype: str
    """
    string = io.StringIO()
    try:
        with redirect_stdout(string):
            exec(input)  # nosec B102
        string.seek(0)
        output = string.read()
    except Exception:
        output = ""
    return output


EVAL_FUNCS = {"sh": eval_sh, "bash": eval_bash, "python": eval_python}


def setup(app: Sphinx) -> dict[str, Any]:
    """Set up.

    :param app:
    :type app: Sphinx
    :rtype: dict[str, Any]
    """
    app.add_config_value("eval_funcs", EVAL_FUNCS, "env")
    app.add_source_parser(RSTEvalParser, True)
    with suppress(ImportError):
        from .myst import MystEvalParser

        app.add_source_parser(MystEvalParser, True)
    return {"version": __version__}
