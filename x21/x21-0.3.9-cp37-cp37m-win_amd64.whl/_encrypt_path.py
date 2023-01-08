import re
import tarfile
import tempfile
import zipfile
from pathlib import Path

from .__about__ import __version__
from ._main import _encrypt, _get_random_string


def encrypt_paths(paths, verbose: bool = False) -> None:
    num = 0
    for path in paths:
        path = Path(path)

        if path.is_dir():
            for p in path.rglob("*.py"):
                encrypt_py(p)
                num += 1

        elif path.suffix == ".py":
            encrypt_py(path)
            num += 1

        elif path.suffix in [".whl", ".zip"]:
            n = encrypt_zip(path)
            num += n

        elif path.suffixes[-2:] == [".tar", ".gz"]:
            n = encrypt_tar_gz(path)
            num += n

        else:
            raise ValueError(f"x21: Don't know how to encrypt {path}")

    print(f"x21: Successfully encrypted {num} Python files")


def encrypt_py(path: Path) -> None:
    if path.suffix != ".py":
        raise ValueError("Must be .py file")

    with open(path) as f:
        content = f.read()

    iv = _get_random_string(16)
    scode = _encrypt("22b", content, iv)
    content = f"""from x21 import __dex_22b__

__dex_22b__(
    globals(),
    "{iv}",
    {scode}
)"""

    with open(path, "w") as f:
        f.write(content)


def encrypt_zip(zip_path: Path) -> int:
    num = 0
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        with zipfile.ZipFile(zip_path) as w:
            w.extractall(tmpdir)

        for p in tmpdir.rglob("*.py"):
            encrypt_py(p)
            num += 1

        # inject x21 dependency in METADATA file
        for item in tmpdir.iterdir():
            if item.name.endswith(".dist-info"):
                with open(item / "METADATA") as f:
                    content = f.read()

                # create upper version limit
                major, minor, micro = __version__.split(".")
                major = int(major)
                minor = int(minor)
                micro = int(micro)
                if major > 0:
                    major += 1
                    minor = 0
                    micro = 0
                elif minor > 0:
                    minor += 1
                    micro = 0
                else:
                    micro += 1
                upper_limit = f"{major}.{minor}.{micro}"

                # inject x21 Requires-Dist before first Requires-Dist
                content = re.sub(
                    "Requires-Dist:",
                    f"Requires-Dist: x21 (>={__version__},<{upper_limit})\nRequires-Dist:",
                    content,
                    count=1,
                )

                with open(item / "METADATA", "w") as f:
                    f.write(content)
                break

        # shutil.make_archive(zip_path, "zip", tmpdir)
        with zipfile.ZipFile(zip_path, "w") as zf:
            for p in tmpdir.rglob("*"):
                zf.write(p, p.relative_to(tmpdir))

    return num


def encrypt_tar_gz(tar_path: Path) -> None:
    num = 0
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        with tarfile.open(tar_path) as tar:
            tar.extractall(tmpdir)

        for p in tmpdir.rglob("*.py"):
            encrypt_py(p)
            num += 1

        with tarfile.open(tar_path, "w:gz") as tar:
            # Override the temp directory by `.` (the current dir)
            tar.add(tmpdir, arcname=".")
    return num
