"""Functions to convert strings, passed as CLI arguments, to
appropriate quantities for these argument types."""

import numpy as np
import os
from pint.errors import UndefinedUnitError

from .. import Q_
from .._exiters import quit_print


def _parse_data_range(*args):
    nargs = len(args)
    if nargs < 3 or nargs > 4:
        quit_print(
            f'Expected data range in format "<start> <stop> <num> [<units>]" ' f"but got: {args}"
        )

    if nargs == 3:
        start, stop, num = args
        units = ""
    else:
        start, stop, num, units = args

    try:
        start = float(start)
    except ValueError:
        quit_print(
            f"Could not convert data range start value '{start}' to a floating point number."
        )

    try:
        stop = float(stop)
    except ValueError:
        quit_print(f"Could not convert data range stop value '{stop}' to a floating point number.")

    try:
        num = int(num)
    except ValueError:
        quit_print(f"Could not convert data range num value '{num}' to an integer.")

    if num <= 0:
        quit_print(f"Number of points in data range must be a positive integer.")

    try:
        return Q_(np.linspace(start, stop, num), units)
    except UndefinedUnitError as ex:
        quit_print(str(ex))


def float_file_range_t(string: str):
    # First try opening argument as a file...
    if os.path.isfile(string):
        # TODO (sjr) Could add support for loading from a cavcalc
        #            serialised output file here. Would need to
        #            return the Single/Multi-Output object itself
        #            probably, then grab the relevant parameter from
        #            this in Arguments.process
        try:
            if string.casefold().endswith(".npy"):
                data = np.load(string)
            else:  # load from text/csv file
                data = np.loadtxt(string)
        except:
            quit_print(f"Unable to parse file {string}")

        return Q_(data)

    # ... then try parsing as a range...
    args = string.split()
    if len(args) > 1:
        return _parse_data_range(*args)

    # ... if that fails then just attempt to convert
    # the argument to a floating point number
    try:
        return Q_(string)
    except UndefinedUnitError as ex:
        quit_print(str(ex))


def mesh_t(string: str):
    if string.casefold() == "true":
        return True

    if string.casefold() == "false":
        return tuple()

    mesh_gen = (param_combo.split(",") for param_combo in string.split(";"))
    meshes = []
    params = []
    for param_combo in mesh_gen:
        if not param_combo or all(not s for s in param_combo):
            continue

        pnames = tuple(pname.strip() for pname in param_combo)
        for pname in pnames:
            if (num_occ := pnames.count(pname)) > 1:
                quit_print(
                    f"Parameter '{pname}' was given {num_occ} times in the mesh "
                    f"combination '{param_combo}'."
                )
            if pname in params:
                quit_print(
                    f"Parameter '{pname}' was already specified in a previous mesh "
                    "combination! Repeated parameter meshes are not currently supported."
                )
            params.append(pname)

        meshes.append(pnames)

    return tuple(meshes)


def limits_t(string: str):
    if string.casefold() == "data":
        return string

    try:
        lo_s, hi_s = string.split()
    except ValueError:
        quit_print('Expected limits specified as "<low> <high>".')

    try:
        lo = None if lo_s == "None" else float(lo_s)
    except ValueError:
        quit_print(f"Lower limit: {lo_s} must be convertible to a number, or None.")

    try:
        hi = None if hi_s == "None" else float(hi_s)
    except ValueError:
        quit_print(f"Upper limit: {hi_s} must be convertible to a number, or None.")

    return lo, hi
