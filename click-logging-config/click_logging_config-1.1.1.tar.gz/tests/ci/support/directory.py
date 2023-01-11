#
#  Copyright (c) 2021 Russell Smiley
#
#  This file is part of click_logging_config.
#
#  You should have received a copy of the MIT License along with build_harness.
#  If not, see <https://opensource.org/licenses/MIT>.
#

import contextlib
import os
import pathlib
import tempfile


@contextlib.contextmanager
def change_directory():
    current_dir = pathlib.Path(os.curdir)
    with tempfile.TemporaryDirectory() as this_dir:
        dir_path = pathlib.Path(this_dir)
        os.chdir(dir_path)

        yield dir_path

    os.chdir(current_dir)
