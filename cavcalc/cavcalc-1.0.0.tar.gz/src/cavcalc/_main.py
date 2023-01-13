import os
from pint.errors import DimensionalityError, UndefinedUnitError
import sys
import warnings

from . import _SESSION, _CONFIG
from ._exiters import quit_print
from ._handler import make_handler
from .output import load, SingleOutput


def main(args=None):
    if not args:
        args = sys.argv[1:]

    args = _SESSION.parse_args(args)

    args.plot |= args.semilogx or args.semilogy or args.loglog
    if args.loglog:
        args.semilogx = True
        args.semilogy = True

    # If any plotting needs doing, then handle style initialisations here
    if args.plot:
        if "plotting" in _CONFIG:
            import matplotlib

            plotting_conf = _CONFIG["plotting"]

            if backend := plotting_conf.get("matplotlib_backend"):
                try:
                    matplotlib.use(backend)
                except Exception as ex:
                    quit_print(str(ex))

            import matplotlib.pyplot as plt

            if style := plotting_conf.get("style"):
                if style.casefold() == "cavcalc":
                    here, _ = os.path.split(os.path.realpath(__file__))
                    cc_style_file = os.path.join(here, "_default.mplstyle")
                    if not os.path.isfile(cc_style_file):
                        warnings.warn("Could not locate cavcalc package style-sheet file!")
                    else:
                        plt.style.use(cc_style_file)
                else:
                    try:
                        plt.style.use(style)
                    except Exception as ex:
                        warnings.warn(str(ex))

    if args.loadfile:
        try:
            out = load(args.loadfile)
        except Exception as ex:
            quit_print(f"The following error occurred during load: {str(ex)}")

        if args.is_single_target:
            if isinstance(out, SingleOutput):
                if out.name != args.compute:
                    quit_print(
                        f"Mismatch between target parameter, '{args.compute}', and the "
                        f"output object parameter '{out.name}' loaded from the"
                        f"specified file '{args.loadfile}'"
                    )
            else:
                if args.compute not in out.results:
                    quit_print(
                        f"The target parameter, '{args.compute}', is not in the output"
                        f"object loaded from the specified file '{args.loadfile}'"
                    )

                out = out.as_single(args.compute)
                if args.units:
                    try:
                        out.convert(args.units)
                    except (DimensionalityError, UndefinedUnitError, ValueError) as ex:
                        quit_print(str(ex))
    else:
        out = make_handler(args).run()

    if args.savefile:
        out.save(args.savefile)

    if args.plot:
        out.plot(
            xlim=args.xlim,
            ylim=args.ylim,
            zlim=args.zlim,
            filename=args.saveplot,
            logx=args.semilogx,
            logy=args.semilogy,
            logz=args.loglog,
            cmap=args.cmap,
        )
    else:
        print(out)

    return out
