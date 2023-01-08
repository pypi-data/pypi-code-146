# Copyright 2022 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Tests the execution environment
"""

import os
import shutil
import sys

import pytest

from portmod.execute import sandbox_execute
from portmod.perms import Permissions


@pytest.mark.parametrize("global_read", [True, False])
def test_symlinks(global_read):
    """Tests that symlinks are handled correctly"""
    try:
        curdir = os.getcwd()
        os.makedirs(os.path.join(curdir, "bar", "baz"), exist_ok=True)
        os.symlink(os.path.join(curdir, "bar", "baz"), "foo")
        if sys.platform == "win32":
            command = ["cmd", "/c", f'copy nul {os.path.join(curdir, "foo", "baf")}']
        else:
            command = ["touch", f"{curdir}/foo/baf"]
        sandbox_execute(
            command,
            Permissions(
                rw_paths=[os.path.join(curdir, "foo")], global_read=global_read
            ),
        )
    finally:
        shutil.rmtree("bar")
        os.remove("foo")
