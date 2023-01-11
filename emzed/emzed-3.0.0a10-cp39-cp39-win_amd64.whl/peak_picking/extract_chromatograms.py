#!/usr/bin/env python
# This file is part of emzed (https://emzed.ethz.ch), a software toolbox for analysing
# LCMS data with Python.
#
# Copyright (C) 2020 ETH Zurich, SIS ID.
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.


import time


def extract_chromatograms(peak_table, ms_level=None, post_fixes=None):
    needed_columns = ["id", "mzmin", "mzmax", "rtmin", "rtmax", "peakmap"]
    if post_fixes is None:
        post_fixes = peak_table.supported_postfixes(needed_columns)
        if not post_fixes:
            raise ValueError("given table is no peak table")
    else:
        missing = []
        for post_fix in post_fixes:
            for name in needed_columns:
                if name + post_fix not in peak_table.col_names:
                    missing.append(name + post_fix)
        if missing:
            raise ValueError("column name(s) {} missing".format(", ".join(missing)))

    started = time.time()

    for post_fix in post_fixes:
        chromatograms = []
        for i, row in enumerate(peak_table):
            rtmin = row["rtmin" + post_fix]
            rtmax = row["rtmax" + post_fix]
            mzmin = row["mzmin" + post_fix]
            mzmax = row["mzmax" + post_fix]
            peakmap = row["peakmap" + post_fix]
            if (
                rtmin is None
                or rtmax is None
                or mzmin is None
                or mzmax is None
                or peakmap is None
            ):
                chromatogram = None
            else:
                chromatogram = peakmap.chromatogram(
                    mzmin=mzmin,
                    mzmax=mzmax,
                    rtmin=rtmin,
                    rtmax=rtmax,
                    ms_level=ms_level,
                )
            chromatograms.append(chromatogram)

        peak_table.add_or_replace_column(
            "chromatogram" + post_fix, chromatograms, object, format_=None
        )

    needed = time.time() - started
    minutes = int(needed) / 60
    seconds = needed - minutes * 60
    if minutes:
        print("needed %d minutes and %.1f seconds" % (minutes, seconds))
    else:
        print("needed %.1f seconds" % seconds)

    return peak_table
