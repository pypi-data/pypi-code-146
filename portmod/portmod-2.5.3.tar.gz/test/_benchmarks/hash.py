# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import pytest

from portmod.globals import env
from portmodlib._deprecated.vfs import find_file
from portmodlib.portmod import _get_hash


def canimport(name: str) -> bool:
    """Returns true if the given module can be imported"""
    try:
        __import__(name)
        return True
    except ModuleNotFoundError:
        return False


@pytest.mark.skipif(
    not canimport("pytest_benchmark"),
    reason="requires pytest-benchmark",
)
@pytest.mark.parametrize("alg", ["BLAKE2B", "MD5", "SHA512", "BLAKE3"])
@pytest.mark.parametrize(
    "buffer", [16 * 1024, 65536, 5 * 1024 * 1024, 512 * 1024 * 1024]
)
@pytest.mark.parametrize("file", ["TR_Data.bsa", "Quill of Feyfolken.omwaddon"])
def test_get_hash_rust(benchmark, alg, buffer, file):
    """Test the speed of loading Manifest files

    Note: requires an openmw configuration and a prefix named openmw
    """
    env.set_prefix("openmw")
    file = find_file(file)

    def test():
        _get_hash(file, [alg], buffer)

    benchmark(test)


@pytest.mark.skipif(
    not canimport("pytest_benchmark"),
    reason="requires pytest-benchmark",
)
@pytest.mark.parametrize(
    "buffer", [16 * 1024, 65536, 5 * 1024 * 1024, 512 * 1024 * 1024]
)
@pytest.mark.parametrize("file", ["TR_Data.bsa", "Quill of Feyfolken.omwaddon"])
def test_get_hash_rust_multiple(benchmark, buffer, file):
    """Test the speed of loading Manifest files

    Note: requires an openmw configuration and a prefix named openmw
    """
    env.set_prefix("openmw")
    file = find_file(file)

    def test():
        _get_hash(file, ["BLAKE2B", "MD5", "SHA512", "BLAKE3"], buffer)

    benchmark(test)


@pytest.mark.skipif(
    not canimport("pytest_benchmark"),
    reason="requires pytest-benchmark",
)
@pytest.mark.parametrize(
    "buffer",
    [1024 * elem for elem in range(1, 10)]
    + [1024 * 1024 * elem for elem in range(1, 10)]
    + [1024 * 1024 * 10 * elem for elem in range(1, 10)],
)
@pytest.mark.parametrize("file", ["TR_Data.bsa", "Quill of Feyfolken.omwaddon"])
def test_get_hash_rust_blake3(benchmark, buffer, file):
    """Test the speed of loading Manifest files

    Note: requires an openmw configuration and a prefix named openmw
    """
    env.set_prefix("openmw")
    file = find_file(file)

    def test():
        _get_hash(file, ["BLAKE3"], buffer)

    benchmark(test)
