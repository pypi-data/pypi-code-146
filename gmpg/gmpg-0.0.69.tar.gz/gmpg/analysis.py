"""
Tools for metamodern software development.

Includes support for testing, syntax checking and metrics measurement
using pytest, flake8, radon respectively.

Provides code analysis and package/interface introspection.

"""

# TODO issue tracking, code review
# TODO code analysis via pysonar2, psydiff
# TODO facilitate anonymous A/B testing in the canopy

import __future__

import collections
import importlib
import inspect
import json
import os
import pkgutil
import re
import subprocess
import sys
import textwrap
import types
import xml.etree.ElementTree

import radon.complexity
import radon.metrics
import radon.raw
from radon.complexity import cc_rank as rank_cc
from radon.metrics import mi_rank as rank_mi

from . import git

__all__ = ["git", "get_api", "get_metrics", "rank_cc", "rank_mi"]


languages = {"py": "Python", "c": "C", "html": "HTML", "css": "CSS", "js": "Javascript"}


def get_metrics(code):
    """
    Return metrics for given code.

    Uses radon to analyze line counts, complexity and maintainability.

    """
    return {
        "lines": radon.raw.analyze(code),
        "maintainability": radon.metrics.mi_visit(code, True),
        "complexity": {o[0]: o[-1] for o in radon.complexity.cc_visit(code)},
    }


def generate_dependency_graph(project_name, project_dir="."):
    subprocess.run(
        [
            "/srv/poetry/bin/poetry",
            "run",
            "pydeps",
            project_name,
            "--show-deps",
            "--noshow",
            "--max-bacon",
            "2",
            "--pylib",
            "-x",
            "os",
            "re types",
            "_*",
            "enum",
        ],
        cwd=project_dir,
    )


def test(pkgdir="."):
    """Test pkgdir with pytest and return test results."""
    # TODO packages = pkg.discover(pkgdir).pop("packages", [])
    proc = subprocess.Popen(  # TODO use .run()
        [
            "pytest-gevent",
            "--doctest-modules",
            "--ignore",
            "setup.py",
            # XXX "--pep8",
            "--cov",
            ".",  # TODO ",".join(packages),
            "--cov-report",
            "xml:.test_coverage.xml",
            "--junit-xml",
            ".test_results.xml",
            "--doctest-glob",
            "README*",
        ],
        env=os.environ,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    _, err = [x.decode("utf-8") for x in proc.communicate()]
    return
    return _parse_junit(), _parse_coverage(), err


def _parse_junit(path=".test_results.xml"):
    suite_tag = xml.etree.ElementTree.parse(str(path)).find("testsuite")
    _suite = dict(suite_tag.attrib)
    suite = {
        "tests": int(_suite["tests"]),
        "errors": int(_suite["errors"]),
        "failures": int(_suite["failures"]),
        "skipped": int(_suite["skipped"]),
        "time": _suite["time"],
        "cases": collections.defaultdict(collections.OrderedDict),
    }
    for case_tag in suite_tag:
        case = dict(case_tag.attrib)
        case["type"] = "success"
        for child in case_tag:
            if child.tag == "failure":
                case["type"] = "failure"
                case["message"] = child.attrib["message"]
            elif child.tag == "system-out":
                ...
            if child.text:
                case["output"] = child.text
        test_identifier = ":".join((case.pop("classname"), case.pop("name")))
        suite["cases"][test_identifier] = case
        # XXX details = {"line": case["line"], "time": case["time"], "outcome": outcome}
        # XXX suite["cases"][case["file"]][test_identifier] = details
    return suite


def _parse_coverage(path=".test_coverage.xml"):
    coverages = {}
    for package in list(list(xml.etree.ElementTree.parse(str(path)).getroot())[1]):
        for case in list(list(package)[0]):
            lines = []
            for line in list(list(case)[1]):
                lines.append((line.attrib["number"], line.attrib["hits"]))
            coverages[case.attrib["filename"]] = (
                round(float(case.attrib["line-rate"]) * 100, 1),
                lines,
            )
    return coverages


# def count_sloc(self):
#     """
#     count Source Lines Of Code
#
#     """
#     # TODO accrue statistics
#     line_counts = collections.defaultdict(int)
#
#     def handle(file):
#         line_count = 0
#         suffix = file.suffix.lstrip(".")
#         if suffix in languages:
#             with file.open() as fp:
#                 lines = fp.readlines()
#                 for line in lines[:10]:
#                     if line.rstrip() == "# noqa":
#                         break
#                 else:
#                     line_count = len(lines)
#                     line_counts[suffix] += line_count
#         yield
#         if line_count:
#             print(" /d,lg/{}/X/".format(line_count), end="")
#             self.position += 3 + len(str(line_count))
#         yield
#
#     def summarize():
#         # TODO commify
#         print("Source Lines of Code:")
#         # print("--------------------", end="\n\n")  TODO markdown output
#         # (`cli` feature to uniform output to HTML for pipe to web agent)
#         total = 0
#         for suffix, line_count in line_counts.items():
#             print("  {:15}{:>10}".format(languages[suffix], line_count))
#             total += line_count
#         print("  {:>25}".format(total))
#
#     return handle, summarize


def get_api(mod, pkg=None) -> dict:
    """Return a dictionary containing contents of given module."""
    mod = mod.removesuffix(".py")
    if pkg:
        mod = ".".join((pkg, mod))
    try:
        module = importlib.import_module(mod)
    except Exception as err:
        print(err)
        module = None
    members = []
    if module:
        members = _get_namespace_members(module)
    details = {"name": mod, "mod": module, "members": members, "descendants": {}}
    try:
        mod_location = module.__path__
        for _, _mod, __ in pkgutil.iter_modules(mod_location):
            details["descendants"][_mod] = get_api(_mod, pkg=mod)
    except AttributeError:
        pass
    return json.loads(JSONEncoder().encode(details))


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        details = {"doc": inspect.getdoc(obj)}
        if callable(obj):
            try:
                details["sig"] = str(inspect.signature(obj))
            except ValueError:
                print(f"can't get signature for builtin {obj}")
        if isinstance(obj, types.ModuleType):
            metrics = None
            if obj.__name__ not in sys.stdlib_module_names:
                metrics = get_metrics(get_code(obj))
            details.update(
                **{
                    "type": "module",
                    "all": getattr(obj, "__all__", []),
                    "metrics": metrics,
                }
            )
        elif isinstance(obj, type):
            details.update(**{"type": "class"})
        elif isinstance(obj, types.FunctionType):
            details.update(**{"type": "function"})
        elif isinstance(obj, object):
            details.update(**{"type": "object"})
        elif isinstance(obj, __future__._Feature):
            details.update(**{"type": "future feature"})
        else:
            return json.JSONEncoder.default(self, obj)
        return details


# def get_api(mod, pkg=None) -> dict:
#     """Return a dictionary containing contents of given module."""
#     if pkg:
#         mod = ".".join((pkg, mod))
#     try:
#         module = importlib.import_module(mod)
#     except Exception as err:
#         print(err)
#         module = None
#     members = []
#     if module:
#         members = _get_namespace_members(module)
#     details = {"name": mod, "mod": module, "members": members, "descendants": {}}
#     try:
#         mod_location = module.__path__
#         for _, _mod, __ in pkgutil.iter_modules(mod_location):
#             details["descendants"][_mod] = get_api(_mod, pkg=mod)
#     except AttributeError:
#         pass
#     return details


def get_doc(obj):
    """Return a two-tuple of object's first line and rest of docstring."""
    docstring = obj.__doc__
    if not docstring:
        return "", ""
    return inspect.cleandoc(docstring).partition("\n\n")[::2]


def _get_namespace_members(mod):  # NOQA FIXME
    modules = inspect.getmembers(mod, inspect.ismodule)
    # for name, m in inspect.getmembers(m, inspect.ismodule):
    #     if inspect.getmodule(mod) != m:
    #         continue
    #     modules.append((name, m))
    exceptions = []
    for name, exc in inspect.getmembers(mod, _isexception):
        if inspect.getmodule(exc) != mod:
            continue
        exceptions.append((name, exc))
    functions = []
    for name, func in get_members(mod, "function"):
        if inspect.getmodule(func) != mod:
            continue
        functions.append((name, func))
    classes = []
    for name, cls in get_members(mod, "class"):
        # if inspect.getmodule(cls) != mod:
        #     continue
        if (name, cls) in exceptions:
            continue
        classes.append((name, cls))
    global_mems = []
    defaults = (
        "__all__",
        "__builtins__",
        "__cached__",
        "__doc__",
        "__file__",
        "__loader__",
        "__name__",
        "__package__",
        "__spec__",
    )
    for global_mem in inspect.getmembers(mod):
        if (
            global_mem in modules
            or global_mem in exceptions
            or global_mem in functions
            or global_mem in classes
            or global_mem[0] in defaults
        ):
            continue
        global_mems.append(global_mem)
    return modules, global_mems, exceptions, functions, classes


def _isexception(obj):
    return inspect.isclass(obj) and issubclass(obj, Exception)


# XXX def _isfunction_or_datadescriptor(obj):
# XXX     return inspect.isfunction(obj) or inspect.isdatadescriptor(obj)


def get_members(obj, pred, hidden=True):
    """Return a list of object's members."""
    pub = []
    hid = []
    keywords = {
        "function": ("def ", "("),
        "class": ("class ", ":("),
        "datadescriptor": ("def ", "("),
        "function_or_datadescriptor": ("def ", "("),
    }
    document_order = []
    for line in get_code(obj).splitlines():
        keyword, delimiter = keywords[pred]
        if line.lstrip().startswith(keyword):
            match = re.search(r" ([A-Za-z0-9_]+)[{}]".format(delimiter), line)
            document_order.append(match.groups()[0])
    try:
        pred_handler = getattr(inspect, "is" + pred)
    except AttributeError:
        pred_handler = globals().get("is" + pred)
    members = dict(inspect.getmembers(obj, pred_handler))
    for name in document_order:
        try:
            _obj = members[name]
        except KeyError:
            continue
        (hid if name.startswith("_") else pub).append((name, _obj))
    return (pub + hid) if hidden else pub


def get_source(obj):
    """
    Return the string representation of given object's code.

    Comments are stripped and code is dedented for easy parsing.

    """
    lines, lineno = inspect.getsourcelines(obj)
    code = "".join(line for line in lines if not line.lstrip().startswith("#"))
    docstring = getattr(obj, "__doc__", None)
    if docstring is not None:
        code = code.replace('"""{}"""'.format(docstring), "", 1)
    return textwrap.dedent(code), lineno


def get_code(obj):
    """
    Return a string containing the source code of given object.

    The declaration statement and any associated docstring will be removed.

    """
    # TODO use sourcelines to return line start no
    try:
        source = inspect.getsource(obj)
    except (OSError, TypeError):
        source = ""
    if obj.__doc__:
        source = source.partition('"""')[2].partition('"""')[2]
    if not source.strip():
        source = source.partition("\n")[2]
    return textwrap.dedent(source)
