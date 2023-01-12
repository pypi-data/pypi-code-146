#!/usr/bin/env python3

import argparse
import json
import functools
import itertools
import os
import sys
from dataclasses import dataclass, replace
from datetime import datetime
from pathlib import Path
from typing import Callable, cast, ParamSpec, Sequence, TypeVar

from marshmallow import Schema, fields, post_load


@dataclass
class Config:
    default_holder: str | None = None
    default_license: str | None = None


class ConfigSchema(Schema):
    default_holder = fields.Str()
    default_license = fields.Str()

    @post_load
    def make_config(self, data: dict[str, str], **_: object) -> Config:
        return Config(**data)


class GenlicError(Exception):
    ...


class NoSuitableConfigDir(GenlicError):
    ...


class UnknownLicense(GenlicError):
    ...


T = TypeVar("T")
R = TypeVar("R")


def fmap(maybe: T | None, f: Callable[[T], R | None]) -> R | None:
    return None if maybe is None else f(maybe)


def ordered_config_dirs() -> list[Path]:
    config_home = (
        fmap(os.environ.get("XDG_CONFIG_HOME"), lambda config_home: [Path(config_home)])
        or []
    )
    config_dirs = (
        fmap(
            os.environ.get("XDG_CONFIG_DIRS"),
            lambda dirs: list(map(Path, dirs.split(":"))),
        )
        or []
    )
    default = (
        fmap(os.environ.get("HOME"), lambda directory: [Path(directory) / ".config"])
        or []
    )
    directories = itertools.chain(config_home, config_dirs, default)
    return [directory / "genlic" / "config.json" for directory in directories]


def get_config_path() -> Path:
    config_dirs = ordered_config_dirs()
    if not config_dirs:
        raise NoSuitableConfigDir(
            "Unable to determine a suitable configuration directory, consider setting $HOME,"
            " $XDG_CONFIG_HOME or $XDG_CONFIG_DIRS"
        )
    maybe_existing_config = next((path for path in config_dirs if path.exists()), None)
    return maybe_existing_config or config_dirs[0]


def load_config(path: Path) -> Config | None:
    config_path = path or get_config_path()

    try:
        with open(config_path, mode="r") as f:
            config_data = json.load(f)
        schema = ConfigSchema()
        return cast(Config, schema.load(config_data))
    except Exception:
        return None


LICENSE_FMTS = {
    "mit": """\
Copyright (c) {year} {holder}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""",
    "bsd": """\
Copyright (c) {year} {holder}

Redistribution and use in source and binary forms, with or without modification, are permitted\
provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of condition\
and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of\
conditions and the following disclaimer in the documentation and/or other materials provided\
with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to\
endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR\
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND\
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR\
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL\
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,\
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER\
IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT\
OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
""",
}


def list_licenses() -> None:
    print("\n".join(LICENSE_FMTS))


def get_license_fmt(license_name: str | None) -> tuple[str, str | None]:
    new_default = None
    if license_name is None:
        while license_name not in LICENSE_FMTS:
            print("Which license would you like to use? Options:")
            list_licenses()
            new_default = license_name = input("> ")
    try:
        return LICENSE_FMTS[license_name], new_default
    except KeyError:
        license_list = "\n".join(LICENSE_FMTS)
        raise UnknownLicense(
            f'"{license_name}" is not a supported license. Please choose from:\n{license_list}'
        )


def get_holder(holder: str | None) -> tuple[str, str | None]:
    if holder is not None:
        return holder, None
    new_holder = input("Who is the copyright holder?\n> ").strip()
    return new_holder, new_holder


def get_year(year: str | None) -> str:
    return year if year is not None else datetime.now().strftime("%Y")


def run(
    config: Config | None,
    config_path: Path,
    license_name: str | None,
    holder: str | None,
    year: str | None,
    output_path: Path,
) -> None:
    config = config or Config()
    license_fmt, new_default_license_name = get_license_fmt(
        license_name or config.default_license
    )
    holder, new_default_holder = get_holder(holder or config.default_holder)
    year = get_year(year)
    license_content = license_fmt.format(holder=holder, year=year)
    with open(output_path, "w") as f:
        f.write(license_content)
    if new_default_license_name is not None or new_default_holder is not None:

        def create_entry(field_name: str, new_default: str | None) -> dict[str, str]:
            return {} if new_default is None else {field_name: new_default}

        license_name_entry = create_entry("default_license", new_default_license_name)
        holder_entry = create_entry("default_holder", new_default_holder)
        new_config = replace(config, **license_name_entry, **holder_entry)
        config_data = ConfigSchema().dumps(new_config)
        config_path.parent.mkdir(exist_ok=True, parents=True)
        with open(config_path, "w") as f:
            f.write(config_data)


P = ParamSpec("P")


def catch_genlic_errors(main: Callable[P, R]) -> Callable[P, R | int]:
    @functools.wraps(main)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | int:
        try:
            return main(*args, **kwargs)
        except GenlicError as e:
            print(e.args[0], file=sys.stderr)
            return 1

    return wrapper


@catch_genlic_errors
def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="genlic",
        description="Generate license text!",
    )
    parser.add_argument(
        "license_name",
        help='Name of the license to generate or "list" to list the available licenses',
        default=None,
        nargs="?",
    )
    parser.add_argument("--holder", help="License holder override to use")
    parser.add_argument("--year", help="Copyright year override to use")
    parser.add_argument(
        "--config",
        help="Config path override to use",
        type=Path,
        default=get_config_path(),
    )
    parser.add_argument(
        "--output_path",
        "-o",
        help="Where to write the LICENSE file",
        type=Path,
        default=Path("LICENSE"),
    )
    args = parser.parse_args(argv)

    if args.license_name == "list":
        list_licenses()
        return 0

    config = load_config(args.config)
    run(
        config, args.config, args.license_name, args.holder, args.year, args.output_path
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
