import tempfile
from pathlib import Path

# import optional hooks as-is from setuptools
# don't mind the "unused import" warnings
from setuptools.build_meta import get_requires_for_build_sdist  # noqa: F401
from setuptools.build_meta import get_requires_for_build_wheel  # noqa: F401
from setuptools.build_meta import prepare_metadata_for_build_wheel  # noqa: F401

from ._encrypt_path import encrypt_py, encrypt_zip


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    from setuptools.build_meta import build_wheel as setuptools_build_wheel

    wheel_basename = setuptools_build_wheel(
        wheel_directory,
        config_settings=config_settings,
        metadata_directory=metadata_directory,
    )

    encrypt_zip(Path(wheel_directory) / wheel_basename)

    return wheel_basename


def build_sdist(sdist_directory, config_settings=None):
    # Actually, we don't support building sdists, but it's tox's default, see
    # <https://github.com/tox-dev/tox/issues/850>. It's perhaps possible to have
    # tox build wheels instead <https://github.com/ionelmc/tox-wheel>, but for now
    # just re-enable sdist building here.
    # The major downsides of sdists is that we can't add extra runtine
    # dependencies here (x21 itself).

    # raise NotImplementedError("x21 cannot build sdists, only wheels")

    import tarfile

    from setuptools.build_meta import build_sdist as setuptools_build_sdist

    # build sdist with setuptools
    tar_basename = setuptools_build_sdist(sdist_directory, config_settings)

    # get `foobar-1.2.3` from `foobar-1.2.3.tar.gz`
    assert tar_basename.endswith(".tar.gz")
    stem = tar_basename[:-7]

    # Unpack sdist and replace the original .py with obfuscated ones
    tar_path = Path(sdist_directory) / tar_basename

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        with tarfile.open(tar_path) as tar:
            tar.extractall(tmpdir)

        for p in tmpdir.rglob("*.py"):
            encrypt_py(p)

        with tarfile.open(tar_path, "w:gz") as tar:
            # The following used to be
            # ```
            # tar.add(tmpdir, arcname="")
            # ```
            # which is wrong. It adds a leading slash in the tar file.
            tar.add(tmpdir / stem, arcname=stem)

    return tar_basename
