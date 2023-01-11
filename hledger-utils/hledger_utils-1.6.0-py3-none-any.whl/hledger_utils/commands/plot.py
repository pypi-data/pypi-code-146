# SPDX-FileCopyrightText: 2023 Yann Büchau <nobodyinperson@posteo.de>
# SPDX-License-Identifier: GPL-3.0-or-later

# internal modules
import math
import copy
import argparse
import pickle
import operator
import time
import datetime
import io
import os
import sys
import re
import json
import subprocess
import logging
import functools
import itertools
import shlex
from contextlib import contextmanager

# internal modules
from hledger_utils.utils import flatten

# external modules
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates
from cycler import cycler
import psutil
import numpy as np

import rich
from rich import print
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.pretty import Pretty
from rich.syntax import Syntax

console = Console(stderr=True)

logger = logging.getLogger("hledger plot")


@contextmanager
def nothing():
    yield


def str_to_str_mapping(s):
    if m := re.fullmatch(r"^(?P<old>.+?)\s*(?:[👉⮕→➡️]|->)+\s*(?P<new>.+)$", s):
        return m.groups()
    else:
        raise argparse.ArgumentTypeError(
            f"Format: 'OLDNAME -> NEWNAME', not {s!r}"
        )


def str_times_float_to_str_mapping(s):
    if m := re.fullmatch(
        r"^(?P<old>.+?)\s*([*·×✖️])\s*(?P<factor>(?:\d+(?:[,.]\d*))|(?:\d*[,.]\d+))\s*(?:[👉⮕→➡️]|->)+\s*(?P<new>.+)$",
        s,
    ):
        d = m.groupdict()
        return d["old"], float(d["factor"]), d["new"]
    else:
        raise argparse.ArgumentTypeError(
            f"Format: 'OLDNAME * FLOAT -> NEWNAME', not {s!r}"
        )


def regex_to_str_mapping(s):
    if m := re.fullmatch(
        r"^(?P<pattern>.+?)\s*(?:[👉⮕→➡️]|->)+\s*(?P<name>.+)$", s
    ):
        pattern, name = m.groups()
        try:
            return re.compile(pattern), name
        except Exception as e:
            raise argparse.ArgumentTypeError(
                f"{pattern!r} is not a valid regular expression: {e}"
            )
    else:
        raise argparse.ArgumentTypeError(
            f"Format: 'REGEX -> NEWNAME', not {s!r}"
        )


def regex_to_json_dict_mapping(s):
    if m := re.fullmatch(
        r"^(?P<pattern>.+?)\s*(?:[👉⮕→➡️]|->)+\s*(?P<json>.+)$", s
    ):
        pattern, jsonstr = m.groups()
        try:
            pattern = re.compile(pattern)
        except Exception as e:
            raise argparse.ArgumentTypeError(
                f"{pattern!r} is not a valid regular expression: {e}"
            )
        try:
            jsondict = json.loads(jsonstr)
        except json.JSONDecodeError as e:
            raise argparse.ArgumentTypeError(
                f"{jsonstr!r} is invalid JSON: {e}"
            )
        if not isinstance(jsondict, dict):
            raise argparse.ArgumentTypeError(
                f"{jsonstr!r} is not a JSON object/dict!"
            )
        return pattern, jsondict
    else:
        raise argparse.ArgumentTypeError(f"Format: 'REGEX -> JSON', not {s!r}")


def regex(s):
    try:
        pattern = re.compile(s)
    except Exception as e:
        raise argparse.ArgumentTypeError(
            f"{pattern!r} is not a valid regular expression: {e}"
        )
    return pattern


parser = argparse.ArgumentParser(
    description="""

📈  Plot hledger data, browse it interactively and save the graphs

Usage: Replace 'hledger' in your command with 'hledger-plot' or 'hledger plot --', for example:

hledger balance -M Costs
      ⮕  hledger plot -- balance -M Costs (double-dash after 'hledger plot')
      ⮕  hledger-plot    balance -M Costs (invoking hledger-plot directly, no double-dash)
      ⮕  hledger plot    balance -M Costs (only works without 'hledger-plot'-specific options)

""".strip(),
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""

ℹ️  Note
=======

- Currently, only plotting 'hledger balance ...' results is supporting.
  You can get quite close to 'hledger register ...' with 'hledger balance --daily' though.
- If you get weird errors like 'hledger: Error: Unknown flag XXXX', see above how to invoke hledger-plot
- Multiple currencies are not really supported, consider converting them via --market, --value or -X or only selecting one currency with cur:€ for example.

🤷 Examples
===========

# Fine-grained past and forecasted Assets
> hledger-plot balance --depth=2 --daily ^Assets: --historical --forecast --end 2030

# Monthly Cost overview with forecast
> hledger-plot balance --depth=2 --monthly ^Costs: --forecast --end 2030

# „How much did and will I pay for that one house?” (if you tagged house transactions with '; house: MyHouse')
> hledger-plot balance not:acct:^Assets --historical --daily tag:house=MyHouse --pivot=house --forecast --end 2030

Written by Yann Büchau
""".strip(),
)
parser.add_argument(
    "-o",
    "--output",
    metavar="PATH",
    action="append",
    default=[],
    help="save plot to file (e.g. 'plot.pdf', 'plot.png', 'plot.fig.pickle', etc.). "
    "Can be specified multiple times.",
)
parser.add_argument(
    "--no-show", help="don't show the plot", action="store_true"
)
parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="verbose output. More -v ⮕ more output",
)
parser.add_argument(
    "-q",
    "--quiet",
    action="count",
    default=0,
    help="less output. More -q ⮕ less output",
)


# styling
parser_styling_group = parser.add_argument_group(
    title="🎨  Styling", description="Options controlling the plot style"
)
parser_styling_group.add_argument("--title", help="window and figure title")
parser_styling_group.add_argument(
    "--axtitle", help="axes title. Defaults to hledger query."
)
parser_styling_group.add_argument(
    "--no-today", action="store_true", help="don't add a 'today' line"
)
parser_styling_group.add_argument(
    "--stacked", help="stacked bar chart", action="store_true"
)
parser_styling_group.add_argument(
    "--barplot",
    help="create a bar chart instead of lines",
    action="store_true",
)
parser_styling_group.add_argument(
    "--rcParams",
    metavar="JSON",
    action="append",
    help="""JSON rcParams (e.g. '{"figure.figsize":"10,10"}'). """
    "Can be specified multiple times. "
    "Later keys overwrite previous existing ones. "
    "See https://matplotlib.org/stable/tutorials/introductory/customizing.html for reference.",
    type=lambda x: json.loads(x),
    default=[],
)
parser_styling_group.add_argument(
    "--xkcd",
    action="store_true",
    help="XKCD mode (Install 'Humor Sans' / 'XKCD Font' for best results)",
)
parser_styling_group.add_argument(
    "--drawstyle",
    choices={"default", "steps-mid", "steps-pre", "steps-post", "steps"},
    help="drawstyle for line plots",
)
parser_styling_group.add_argument(
    "--style",
    metavar="REGEX -> JSON",
    action="append",
    type=regex_to_json_dict_mapping,
    help="""Mapping like 'REGEX -> JSON' to add extra styling arguments for columns, "
    "e.g. '^Cost: -> {"linewidth":5,"linestyle":"dashed"}'"""
    "Can be specified multiple times.",
    default=[],
)
parser_styling_group.add_argument(
    "--account-format",
    help="Format for account name including the currency. "
    "Default is '{account} ({commodity})' "
    "if there are multiple currencies, otherwise just '{account}'. "
    "Applied before any other modifications/matching.",
    default=None,
)


# modification
parser_modify_group = parser.add_argument_group(
    title="🔢  Data Modification",
    description="Options for manipulating the data",
)
parser_modify_group.add_argument(
    "--invert", help="invert amounts (done first)", action="store_true"
)
parser_modify_group.add_argument(
    "--rename",
    metavar="OLDNAME -> NEWNAME",
    help="mapping(s) like 'OLD1 -> NEW1' for renaming columns. Can be specified multiple times.",
    action="append",
    type=str_to_str_mapping,
    default=[],
)
parser_modify_group.add_argument(
    "--sum",
    metavar="REGEX -> NEWNAME",
    type=regex_to_str_mapping,
    action="append",
    help="Mapping like 'REGEX -> NAME' to sum matching columns into a new field. "
    "Can be specified multiple times. "
    "Use e.g. --sum '.* -> total' to get a total value."
    "--sum is performed after --rename",
    default=[],
)
parser_modify_group.add_argument(
    "--sum-again",
    action="store_true",
    help="Quick'n'dirty hack to apply --sum again after --multiply and --mean."
    "This option will not be necessary anymore "
    "when hledger-plot's cli is migrated to click.",
)
parser_modify_group.add_argument(
    "--mean",
    metavar="REGEX -> NEWNAME",
    type=regex_to_str_mapping,
    action="append",
    help="Mapping like 'REGEX -> NAME' to average matching columns into a new field. "
    "Can be specified multiple times. "
    "--mean is performed after --rename",
    default=[],
)
parser_modify_group.add_argument(
    "--multiply",
    metavar="NAME * FLOAT -> NEWNAME",
    type=str_times_float_to_str_mapping,
    action="append",
    help="Mapping like 'REGEX * FLOAT -> NAME' "
    "to multiply a column with a value "
    "and store it into a new column. "
    "Can be specified multiple times. "
    "--multiply is performed after --rename",
    default=[],
)
parser_modify_group.add_argument(
    "--resample",
    metavar="INTERVAL",
    help="DataFrame.resample() argument for data resampling "
    "(e.g. '60d' for a 60-day mean, "
    "see https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.resample.html)",
)
parser_modify_group.add_argument(
    "--drop",
    metavar="REGEX",
    help="regular expressions for dropping columns right before plotting. "
    "Can be specified multiple times.",
    action="append",
    type=regex,
    default=[],
)
parser_modify_group.add_argument(
    "--only",
    metavar="REGEX",
    help="regular expressions for keeping only matching columns for plotting. "
    "Can be specified multiple times.",
    action="append",
    type=regex,
    default=[],
)


hledger_parser = argparse.ArgumentParser(prog="hledger")
hledger_parser.add_argument("--output-format", "-O")
hledger_parser.add_argument("--file", "-f")
# CAUTION: These options are handled differently across hledger versions!
hledger_parser.add_argument("--market", "--value", "-V", action="store_true")
# hledger commands
hledger_subparsers = hledger_parser.add_subparsers(
    required=True, dest="command"
)
hledger_balance_subparser = hledger_subparsers.add_parser(
    "balance", aliases=["b", "bal"]
)
hledger_balance_subparser.add_argument("--layout")
hledger_balance_subparser.add_argument(
    "--historical", "-H", action="store_true"
)
aggregation_period_args = [
    hledger_balance_subparser.add_argument(
        "--daily", "-D", action="store_true"
    ),
    hledger_balance_subparser.add_argument(
        "--weekly", "-W", action="store_true"
    ),
    hledger_balance_subparser.add_argument(
        "--monthly", "-M", action="store_true"
    ),
    hledger_balance_subparser.add_argument(
        "--quarterly", "-Q", action="store_true"
    ),
    hledger_balance_subparser.add_argument(
        "--yearly", "-Y", action="store_true"
    ),
]
aggregation_periods = tuple(
    map(operator.attrgetter("dest"), aggregation_period_args)
)
hledger_subparsers.add_parser("register", aliases=["r", "reg"])
hledger_subparsers.add_parser("print")
hledger_subparsers.add_parser("accounts", aliases=["a", "acc"])
hledger_subparsers.add_parser("prices")
hledger_subparsers.add_parser("stats")
hledger_subparsers.add_parser("tags")
hledger_subparsers.add_parser("web")


def cli(cli_args=sys.argv[1:]):
    args, hledger_args = parser.parse_known_args()
    logging.basicConfig(
        level={
            -3: "CRITICAL",
            -2: "ERROR",
            -1: "WARNING",
            0: "INFO",
            1: "DEBUG",
        }.get(
            (v := args.verbose - args.quiet),
            logging.CRITICAL + abs(v) if v < -3 else "NOTSET",
        ),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
    )
    for name in logging.root.manager.loggerDict:
        if "hledger" not in name:
            logging.getLogger(name).setLevel(10000)

    logger.debug(f"{args = }")
    logger.debug(f"{hledger_args = }")

    try:
        (
            hledger_parsed_args,
            hledger_unknown_args,
        ) = hledger_parser.parse_known_args(hledger_args)
    except BaseException as e:
        logger.warning(
            "Your hledger command {} looks broken".format(
                repr(" ".join(hledger_args))
            )
        )
        sys.exit(1)
    logger.debug(f"{hledger_parsed_args = }")
    logger.debug(f"{hledger_unknown_args = }")

    # TODO: automatically get aliases from above?
    parseable_hledger_commands = ["balance", "b", "bal"]
    if hledger_parsed_args.command not in parseable_hledger_commands:
        logger.info(
            "Currently, only the {} commands' output can be parsed and plotted".format(
                ",".join(map("'{}'".format, parseable_hledger_commands))
            )
        )
        sys.exit(1)

    hledger_executable = "hledger"
    hledger_parent_process = psutil.Process(os.getppid())
    if "hledger" in hledger_parent_process.cmdline()[0]:
        hledger_executable = hledger_parent_process.cmdline()[0]

    hledger_cmdline_parts = [hledger_executable] + hledger_args
    if hledger_parsed_args.output_format is None:
        hledger_cmdline_parts.append("-Ocsv")
    elif hledger_parsed_args.output_format != "csv":
        logger.info(
            "Please don't specify an output format for hledger other than csv"
        )
        sys.exit(1)

    hledger_cmdline_extra_args = []
    if "balance".startswith(hledger_parsed_args.command):
        if (layout := hledger_parsed_args.layout) and layout != "tidy":
            logger.error(
                "Please don't specify something else than --layout=tidy"
            )
            sys.exit(1)
        else:
            hledger_cmdline_extra_args.append("--layout=tidy")
        if not hledger_parsed_args.historical:
            logger.info(
                "ℹ️  Hint: You might want to consider adding --historical/-H to get the real balances at these times"
            )
        if not hledger_parsed_args.market and not any(
            "cur:" in arg for arg in hledger_unknown_args
        ):
            logger.info(
                "ℹ️  Hint: You might want to consider converting amounts to one currency via --market/--value/-V or selecting only one currency e.g. with 'cur:€'"
            )
        if not any(
            map(lambda x: getattr(hledger_parsed_args, x), aggregation_periods)
        ):
            logger.info("Adding --daily aggregation period for you")
            hledger_cmdline_extra_args.append("--daily")

    def hledger_to_dataframe(hledger_cmdline_parts):
        hledger_cmdline_parts.extend(hledger_cmdline_extra_args)
        hledger_cmdline = shlex.join(hledger_cmdline_parts)
        logger.info("🚀  Executing {}".format(repr(hledger_cmdline)))
        try:
            hledger = subprocess.Popen(
                hledger_cmdline_parts,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding="utf-8",
                errors="ignore",
            )
        except BaseException as e:
            logger.info(
                "Couldn't execute {}: {}".format(repr(hledger_cmdline), e)
            )
            sys.exit(1)

        # TODO: Reading the whole output at once is ridiculous.
        # WAY better: a file-object wrapper that sanitizes the output on-the-fly so that
        # pandas can then directly parse it. But I couldn't get that to work AT ALL...

        logger.info("📤  Reading hledger's output...")
        hledger_output, hledger_stderr = hledger.communicate()

        logger.debug(f"{hledger_stderr = }")
        if hledger_stderr:
            logger.warning(
                f"Command >>> {hledger_cmdline} <<< returned STDERR:\n{hledger_stderr}"
            )

        if not hledger_output:
            logger.info(
                f"Command >>> {hledger_cmdline} <<< returned no output."
            )
            sys.exit(0)

        if logger.getEffectiveLevel() < logging.DEBUG:
            console.print(
                Panel(
                    Syntax(
                        hledger_output,
                        "python",
                        line_numbers=True,
                    ),
                    title=f"Output of {hledger_cmdline}",
                )
            )

        logger.debug("Parsing output...")
        try:
            read_csv_args, read_csv_kwargs = [
                io.StringIO(hledger_output)
            ], dict(
                on_bad_lines="skip",
            )
            logger.debug(
                f"Running pd.read_csv(*{read_csv_args}, **{read_csv_kwargs})"
            )
            data = pd.read_csv(*read_csv_args, **read_csv_kwargs)

        except Exception as e:
            logger.exception(f"Error: {e}")
            logger.info(hledger_output)
            sys.exit(1)

        logger.debug("Converting times...")
        for col in ["period", "start_date", "end_date"]:
            if col in data:
                data[col] = pd.to_datetime(data[col], errors="coerce")

        logger.debug("Converting amounts...")
        for col in ["value"]:
            if col in data:
                data[col] = pd.to_numeric(data[col], errors="coerce")

        return data

    data = hledger_to_dataframe(hledger_cmdline_parts)
    commodities = list(data.commodity.unique())
    if not args.account_format:
        args.account_format = (
            "{account} ({commodity})" if len(commodities) > 1 else "{account}"
        )

    # Try to auto-format commodities right
    # TODO: Can be prevent this loop by using `hledger stats` for example to
    # know the commodities in advance? Although hledger stats also parses
    # everything so might not be much of a benefit...
    if missing_values := data["value"].isna().sum():
        logger.warning(
            f"There are {missing_values} NaNs in the converted amounts."
        )
        commodity_format_opts = list(
            itertools.chain.from_iterable(
                ("-c", f'1000000.0000 "{curr}"') for curr in commodities
            )
        )
        logger.info(f"Retrying with {shlex.join(commodity_format_opts)}")
        data = hledger_to_dataframe(
            hledger_cmdline_parts + commodity_format_opts
        )
        if missing_values := data["value"].isna().sum():
            logger.warning(
                f"Didn't help, trying to plot anyway but it'll look weird."
            )
        else:
            logger.info(f"That worked, no NaNs in the amounts anymore! 🎉 ")

    time_columns = [col for col in data if hasattr(data[col], "dt")]
    logger.debug(f"Using minimum of {time_columns = } as time")
    data = data.set_index(data[time_columns].min(axis="columns"))
    data = data.drop(columns=time_columns)
    logger.debug(f"data = \n{data}")

    data["account"] = data["account"].astype(str)

    logger.info(f"Grouping accounts and commodities")
    groupby = ["account", "commodity"]
    data = pd.concat(
        [
            g["value"].rename(
                args.account_format.format(**dict(zip(groupby, n)))
            )
            for n, g in data.groupby(groupby)
        ],
        axis="columns",
    )
    logger.debug(f"data = \n{data}")

    # some sane defaults for rcParams
    plt.rcParams["legend.handlelength"] = 5
    if len(data.columns) > 10:
        plt.rcParams["legend.fontsize"] = "x-small"
    elif len(data.columns) > 15:
        plt.rcParams["legend.fontsize"] = "xx-small"
    plt.rcParams["axes.grid"] = True
    plt.rcParams["axes.axisbelow"] = True
    # expand prop cycle
    prop_cycle = plt.rcParams["axes.prop_cycle"]
    if "linestyle" not in prop_cycle:
        prop_cycle = (
            cycler(linestyle=["solid", "dashed", "dotted"]) * prop_cycle
        )
    if "linewidth" not in prop_cycle:
        lw = plt.rcParams.get("lines.linewidth", 2)
        prop_cycle = (
            cycler(linewidth=[lw, lw + 1, lw + 2, lw + 3]) * prop_cycle
        )
    plt.rcParams["axes.prop_cycle"] = prop_cycle
    # logger.debug(f"{list(plt.rcParams['axes.prop_cycle']) = }")

    # merge all --rcParams options
    args.rcParams = functools.reduce(
        lambda a, b: {**a, **b}, filter(bool, args.rcParams), dict()
    )
    # overwrite with user's rcParams
    plt.rcParams.update(args.rcParams)

    # 🔢 Data Modification
    if args.invert:
        logger.info(f"↔️  Inverting amounts")
        data = data * -1

    logger.debug(f"data = \n{data}")
    data = data.rename(columns={x: str(x) for x in data})
    if args.rename:
        logger.debug(f"{data.columns = }")
        renames = dict(args.rename)
        logger.info(f"Renaming columns: {renames}")
        data = data.rename(columns=renames)
        logger.debug(f"{data = }")

    if args.sum:
        logger.debug(f"{args.sum = }")
        for pattern, newname in args.sum:
            if columns := list(filter(pattern.search, data)):
                data[newname] = np.nansum(
                    [data[col] for col in columns], axis=0
                )
                logger.info(
                    f"Created new column {newname!r} summing {columns}"
                )
            else:
                logger.info(
                    f"🤷  No columns matching pattern {pattern.pattern!r}"
                )

    if args.mean:
        logger.debug(f"{args.mean = }")
        for pattern, newname in args.mean:
            if columns := list(filter(pattern.search, data)):
                data[newname] = np.nanmean(
                    [data[col] for col in columns], axis=0
                )
                logger.info(
                    f"Created new column {newname!r} averaging {columns}"
                )
            else:
                logger.info(
                    f"🤷  No columns matching pattern {pattern.pattern!r}"
                )

    if args.multiply:
        logger.debug(f"{args.multiply = }")
        for oldname, factor, newname in args.multiply:
            if oldname not in data:
                logger.error(
                    f"No such column {oldname!r} to multiply with {factor}"
                )
            data[newname] = data[oldname] * factor

    if args.sum and args.sum_again:
        logger.debug(f"{args.sum = }")
        for pattern, newname in args.sum:
            if columns := list(filter(pattern.search, data)):
                data[newname] = np.nansum(
                    [data[col] for col in columns], axis=0
                )
                logger.info(
                    f"Created new column {newname!r} summing {columns}"
                )
            else:
                logger.info(
                    f"🤷  No columns matching pattern {pattern.pattern!r}"
                )

    if args.resample:
        data = data.resample(args.resample).sum()

    if args.drop:
        logger.debug(f"{args.drop = }")
        for pattern in args.drop:
            if columns := list(filter(pattern.search, data)):
                data = data.drop(columns=columns)
                logger.info(f"Dropped columns {columns!r}")
            else:
                logger.info(
                    f"🤷  No columns matching pattern {pattern.pattern!r}"
                )

    if args.only:
        logger.debug(f"{args.only = }")
        if columns := list(
            col for col in data if any(p.search(col) for p in args.only)
        ):
            data = data[columns]
            logger.info(f"Kept only columns {columns!r}")
        else:
            logger.info(f"🤷  No columns matching pattern {pattern.pattern!r}")

    logger.info("📈  Plotting...")
    with plt.xkcd() if args.xkcd else nothing():
        fig, ax = plt.subplots(num=args.title)
        if args.barplot:
            logger.warning(
                f"Barplots are kind of limited right now and don't scale well."
            )
            if args.stacked:
                data.drop(
                    columns=["Total:", "total:"], inplace=True, errors="ignore"
                )
            data["Point in Time"] = data.index.strftime("%Y-%m-%d")
            data.plot.bar(ax=ax, x="Point in Time", stacked=args.stacked)
        else:

            def only_prop_cycle(d):
                return {
                    k: v
                    for k, v in d.items()
                    if k in plt.rcParams["axes.prop_cycle"].keys
                }

            used_styles = list()
            for column in data:
                series = data[column]
                plot_kwargs = dict(drawstyle=args.drawstyle, label=column)
                if args.style:
                    # apply styles
                    for pattern, kwargs in args.style:
                        if pattern.search(column):
                            plot_kwargs.update(kwargs)
                    logger.debug(f"after applying --styles {plot_kwargs = }")

                    if pc_kw := next(
                        (
                            pc
                            for pc in list(plt.rcParams["axes.prop_cycle"])
                            if not any(
                                s == only_prop_cycle({**pc, **plot_kwargs})
                                for s in used_styles
                            )
                        ),
                        None,
                    ):
                        logger.debug(
                            f"Found previously unused style: {pc_kw = }"
                        )
                        plot_kwargs = {**pc_kw, **plot_kwargs}
                        logger.debug(
                            f"after filling with prop_cycle: {plot_kwargs = }"
                        )
                ax.plot(series.index, series, **plot_kwargs)
                used_styles.append(only_prop_cycle(plot_kwargs))
                logger.debug(f"{used_styles = }")

            if not args.no_today:
                ax.axvline(
                    pd.to_datetime(datetime.datetime.now()),
                    alpha=0.2,
                    color="black",
                    linewidth=10,
                    linestyle="solid",
                    label="today",
                    zorder=-10,
                )

        if args.title:
            fig.suptitle(args.title)
        ax.set_title(args.axtitle or " ".join(hledger_args))
        ax.set_ylabel(" ".join(f"[{c}]" for c in commodities))
        ax.legend(ncols=math.ceil(len(ax.get_lines()) / 40))

        fig.tight_layout()
        fig.set_tight_layout(True)
        fig.autofmt_xdate()

        for output_file in flatten(args.output):
            logger.info("📥  Saving plot to '{}'".format(output_file))
            if output_file.endswith(".pickle"):
                with open(output_file, "wb") as fh:
                    pickle.dump(fig, fh)
            else:
                fig.savefig(output_file)

        if not args.no_show:
            logger.info("👀  Showing plot...")
            plt.show()


if __name__ == "__main__":
    cli()
