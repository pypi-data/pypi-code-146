#
# Copyright (c) 2022 Jim Bauer <4985656-jim_bauer@users.noreply.gitlab.com>
# This software is licensed according to the included LICENSE file
# SPDX-License-Identifier: GPL-3.0-or-later
#

# read version from installed package
from importlib.metadata import version
__version__ = version("feedfilter")

from feedfilter.feed_filter import main # noqa: F401
