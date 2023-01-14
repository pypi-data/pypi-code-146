# SPDX-FileCopyrightText: 2023 Maxwell G <gotmax@e.email>
#
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

import argparse
import logging
from collections.abc import Sequence

from .base import LOG, Command
from .dev_entries import DevEntries, DevSRPM


def main(argv: Sequence[str] | None = None, **kwargs) -> None:
    parser = argparse.ArgumentParser(
        description="fclogr is a tool for managing RPM changelogs and updates", **kwargs
    )
    log_group = parser.add_mutually_exclusive_group()
    log_group.add_argument(
        "--debug", action="store_const", dest="log_level", const="DEBUG"
    )
    log_group.add_argument(
        "--ll",
        "--log-level",
        dest="log_level",
        type=lambda t: t.upper(),
        choices=["DEBUG", "INFO"],
    )
    subparsers = parser.add_subparsers(
        title="Subcommands", dest="action", required=True
    )
    for name, cls in COMMANDS.items():
        cls.make_parser(subparsers.add_parser, standalone=False, name=name)

    args = vars(parser.parse_args(argv))
    action = args.pop("action")
    if log_level := args.pop("log_level"):
        level = getattr(logging, log_level)
        LOG.setLevel(level)

    command = COMMANDS[action](**args)
    command.run()


COMMANDS: dict[str, type[Command]] = {"dev-entries": DevEntries, "dev-srpm": DevSRPM}
