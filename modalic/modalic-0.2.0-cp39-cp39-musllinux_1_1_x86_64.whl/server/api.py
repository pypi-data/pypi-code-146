#  Copyright (c) modalic 2022. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
"""API for calling Aggregation Server"""
import os
import sys


class ServerBinaryNotFound(Exception):
    r"""Error thrown by when aggregation server binary is not found."""


def find_bin_path() -> str:
    r"""Find the path to binary files.

    :returns: Path to binary which is the server application.
    """
    curr_path = os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))

    bin_path = [
        # normal, after installation `lib` is copied into Python package tree.
        os.path.join(curr_path, "bin"),
        # editable installation, no copying is performed.
        os.path.join(curr_path, os.path.pardir, "bin"),
        # search for mosaic aggregator binary from a system prefix, if available.
        # This should be the last option.
        os.path.join(sys.prefix, "bin"),
    ]

    if sys.platform == "win32":
        pass
    if sys.platform.startswith(("linux", "freebsd", "emscripten")):
        bin_path = [os.path.join(p, "aggregator") for p in bin_path]
    if sys.platform == "darwin":
        bin_path = [os.path.join(p, "aggregator") for p in bin_path]
    if sys.platform == "cygwin":
        bin_path = [os.path.join(p, "aggregator") for p in bin_path]

    aggregator = [
        file for file in bin_path if os.path.exists(file) and os.path.isfile(file)
    ]

    if not aggregator:
        link = "https://github.com/modalic/mosaic"
        excpt = (
            "Cannot find binary for executing the server in the candidate path. "
            + "List of candidates:\n- "
            + ("\n- ".join(bin_path))
            + "\nModalic Python package path: "
            + curr_path
            + "\nsys.prefix: "
            + sys.prefix
            + "\nSee: "
            + link
            + " for installing aggregation server Mosaic of Modalic."
        )
        raise ServerBinaryNotFound(excpt)
    return aggregator[0]
