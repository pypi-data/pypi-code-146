# vim: ts=4 sts=4 sw=4 ft=python expandtab :
#
# Author: D.S. Ljugmark <spider@skuggor.se>, Modio AB
# SPDX-License-Identifier: AGPL-3.0-or-later
#
"""The main library entrypoint is pretty empty.

Two selftest routines right now. The rest should all use the sub-modules.
"""

from . import selftest

if __name__ == "__main__":
    selftest()
