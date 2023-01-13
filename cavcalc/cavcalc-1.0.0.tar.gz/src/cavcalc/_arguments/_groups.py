"""The argument groups loaded by the session argument parser."""

import argparse

from .. import Q_
from ..parameters import ArgParameter, ParameterType, valid_arguments, valid_targets
from ..__version__ import __version__

from ._types import float_file_range_t, mesh_t, limits_t


def make_arguments(parser: argparse.ArgumentParser):
    _make_target_arguments(parser)
    _make_physical_parameter_arguments(parser)
    _make_data_arguments(parser)
    _make_file_arguments(parser)
    _make_plotting_arguments(parser)
    _make_misc_arguments(parser)


def _make_target_arguments(parser: argparse.ArgumentParser):
    target_group = parser.add_argument_group(
        "Compute targets", "Arguments related to the target parameter to compute."
    )
    target_group.add_argument(
        "compute",
        choices=valid_targets + ("all",),
        help="Choice of parameter to compute. Default is 'all' for "
        "computing all available parameters from the given input values.",
        nargs="?",
        default="all",
    )
    target_group.add_argument(
        "-u",
        "--units",
        help="Units of output. Only used if a compute target was specified, i.e. it is ignored "
        "if computing all available targets. Note that if this option is specified then it "
        "will override the associated unit option in the config file.",
        type=str,
    )


def _make_physical_parameter_arguments(parser: argparse.ArgumentParser):
    physical_group = parser.add_argument_group(
        "Physical parameters",
        "Arguments which are the dependencies of the target parameter function. All of "
        "these arguments can be given as <value>[<units>] (single value, units optional), or "
        '"<start> <stop> <num> [<units>]" (range of values, units optional).',
    )

    for pname in valid_arguments:
        arg_p = ArgParameter(pname)
        physical_group.add_argument(
            arg_p.cli_form,
            help=arg_p.description,
            type=float_file_range_t,
            default=Q_("1064nm") if arg_p.ptype == ParameterType.WAVELENGTH else None,
        )


def _make_data_arguments(parser: argparse.ArgumentParser):
    data_group = parser.add_argument_group(
        "Data options", "Arguments for manipulating physical parameter ranges."
    )
    data_group.add_argument(
        "--mesh",
        dest="mesh",
        help="Construct mesh-grids from specified parameter combinations.",
        type=mesh_t,
    )


def _make_file_arguments(parser: argparse.ArgumentParser):
    file_group = parser.add_argument_group(
        "File options", "Arguments for loading and saving output instances."
    )
    file_group.add_argument(
        "-load",
        "--loadfile",
        help="Name of file from which to load a serialized cavcalc output object.",
        type=str,
    )
    file_group.add_argument(
        "-save",
        "--savefile",
        help="Name of file to which the output object will be saved.",
        type=str,
    )


def _make_plotting_arguments(parser: argparse.ArgumentParser):
    plotting_group = parser.add_argument_group(
        "Plotting options", "Arguments for generating plots."
    )
    plotting_group.add_argument(
        "--plot",
        dest="plot",
        action="store_true",
        help="Plot the target data on linear scales.",
    )
    plotting_group.add_argument(
        "--cmap",
        dest="cmap",
        help="Matplotlib compliant colormap to use for the generated image plot. Ignored "
        "if no plotting action was requested, or if no meshes were defined.",
        type=str,
    )
    plotting_group.add_argument(
        "--logxplot",
        dest="semilogx",
        action="store_true",
        help="Plot the target data with log-scale x-axis. Ignored if any meshes were defined.",
    )
    plotting_group.add_argument(
        "--logyplot",
        dest="semilogy",
        action="store_true",
        help="Plot the target data with log-scale y-axis. Ignored if any meshes were defined.",
    )
    plotting_group.add_argument(
        "--logplot",
        dest="loglog",
        action="store_true",
        help="Plot the target data on a log-log scale if no meshes were defined, otherwise "
        "otherwise uses a logarithmic normalisation scale for the image plot colorbar(s).",
    )
    plotting_group.add_argument("--saveplot", help="Save the figure with the specified name.")
    plotting_group.add_argument(
        "--xlim",
        dest="xlim",
        help="Limits of x-axis.",
        type=limits_t,
    )
    plotting_group.add_argument(
        "--ylim",
        dest="ylim",
        help="Limits of y-axis.",
        type=limits_t,
    )
    plotting_group.add_argument(
        "--zlim",
        dest="zlim",
        help="Limits of color-bar scale. Ignored if no meshes were defined.",
        type=limits_t,
    )
    parser.set_defaults(plot=False, semilogx=False, semilogy=False, loglog=False)


def _make_misc_arguments(parser: argparse.ArgumentParser):
    misc_group = parser.add_argument_group(
        "Miscellaneous options",
        "Arguments for displaying information about cavcalc.",
    )
    misc_group.add_argument(
        "-V",
        "--version",
        help="Current version of cavcalc.",
        action="version",
        version=f"cavcalc v{__version__}",
    )
