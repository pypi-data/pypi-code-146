import dataclasses
import hashlib
import os
import sys
import typing
from pathlib import Path


@dataclasses.dataclass()
class ShellFunction:
    name: str
    body: list[str]


CACHE_DIR: Path = Path(
    os.environ.get("IPKG_CACHE_DIR", default=Path.home() / ".cache" / "ipkg")
)
DRY_RUN: bool = False
INDENT: str = "  "


def tee(*values: object, file: typing.TextIO):
    print(*values, file=file)
    print(*values)


def open_cache(args: list[str] = sys.argv[1:], encoding="utf-8") -> typing.TextIO:
    if DRY_RUN:
        return sys.stdout
    else:
        sha1 = hashlib.sha1(
            string=bytes(" ".join(args) + "\n", encoding=encoding)
        ).hexdigest()
        os.makedirs(CACHE_DIR, exist_ok=True)
        return open(file=CACHE_DIR / sha1, mode="w")


def export(cache: typing.TextIO, env: dict[str, str]) -> None:
    for name, value in env.items():
        print(f'export {name}="{value}"', file=cache)


def unset(cache: typing.TextIO, names: list[str]) -> None:
    for name in names:
        print(f"unset {name}", file=cache)


def function(cache: typing.TextIO, functions: list[ShellFunction]) -> None:
    for shell_function in functions:
        print(f"function {shell_function.name} {{", file=cache)
        for line in shell_function.body:
            print(INDENT + line, file=cache)
        print("}", file=cache)


def unset_function(cache: typing.TextIO, names: list[str]) -> None:
    for name in names:
        print(f"unset -f {name}", file=cache)


def exec(cache: typing.TextIO, commands: list[list[str]]) -> None:
    for args in commands:
        print(" ".join(args), file=cache)
