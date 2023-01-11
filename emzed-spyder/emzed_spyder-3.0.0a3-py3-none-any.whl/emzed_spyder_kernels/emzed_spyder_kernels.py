#! /usr/bin/env python
# Copyright 2020 Uwe Schmitt <uwe.schmitt@id.ethz.ch>

import os
import sys


import spyder_kernels.console.kernel as kernel
import spyder_kernels.utils.nsview as nsview


def set_cwd(self, dirname):
    if sys.platform == "win32":
        dirname = dirname.replace("\\\\", "\\")
    os.chdir(dirname)


kernel.SpyderKernel.set_cwd = set_cwd


def get_size(item, _orig=nsview.get_size):
    import emzed
    import emzed.ms_data as mzm

    if isinstance(item, emzed.Table):
        return "{} row x {} columns".format(len(item), len(item.col_names))
    if isinstance(item, (emzed.PeakMap, mzm.ImmutablePeakMap)):
        return "{} spectra".format(len(item))
    return _orig(item)


nsview.get_size = get_size


def is_supported(
    value, check_all=False, filters=None, iterate=False, _orig=nsview.is_supported
):
    import emzed
    import emzed.ms_data as mzm

    if isinstance(value, (emzed.Table, mzm.ImmutablePeakMap)):
        return False  # value.is_open()
    return _orig(value, check_all, filters, iterate)


nsview.is_supported = is_supported


orig_globalsfilter = nsview.globalsfilter


def globalsfilter(*a, **kw):
    mapping = orig_globalsfilter(*a, **kw)
    import emzed
    import emzed.ms_data as mzm

    return {
        k: v
        for (k, v) in mapping.items()
        if not isinstance(v, (emzed.Table, mzm.ImmutablePeakMap)) or v.is_open()
    }


nsview.globalsfilter = globalsfilter


def get_type_string(item, _orig=nsview.get_type_string):
    import emzed
    import emzed.ms_data as mzm

    if isinstance(item, emzed.Table):
        return "Table"
    if isinstance(item, emzed.PeakMap):
        return "PeakMap"
    if isinstance(item, mzm.ImmutablePeakMap):
        return "ImmutablePeakMap"
    return _orig(item)


nsview.get_type_string = get_type_string


def value_to_display(value, minmax=False, level=0, _orig=nsview.value_to_display):
    import emzed

    if isinstance(value, emzed.Table):
        return ", ".join(value.col_names)
    return _orig(value, minmax, level)


nsview.value_to_display = value_to_display


if __name__ == "__main__":
    from spyder_kernels.console import start

    start.main()
