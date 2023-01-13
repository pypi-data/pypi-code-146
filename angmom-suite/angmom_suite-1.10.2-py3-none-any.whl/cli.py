from argparse import ArgumentParser, Action, RawDescriptionHelpFormatter
import h5py
import hpc_suite as hpc
from .multi_electron import Ion, parse_termsymbol


# Action for secondary help message
class SecondaryHelp(hpc.SecondaryHelp):
    def __init__(self, option_strings, dest=None, const=None, default=None,
                 help=None):
        super().__init__(option_strings, dest=dest, const=const,
                         default=default, help=help)

    def __call__(self, parser, values, namespace, option_string=None):
        read_args([self.const, '--help'])


class QuaxAction(Action):
    def __init__(self, option_strings, dest, nargs=1, default=None, type=None,
                 choices=None, required=False, help=None, metavar=None):

        super().__init__(
            option_strings=option_strings, dest=dest, nargs=nargs,
            default=default, type=type, choices=choices, required=required,
            help=help, metavar=metavar
        )

    def __call__(self, parser, namespace, value, option_string=None):

        if hpc.store.is_hdf5(value[0]):  # import from HDF5 database
            with h5py.File(value[0], 'r') as h:
                quax = h["quax"][...]
        else:
            raise ValueError("Invalid file type for QUAX specification.")

        setattr(namespace, self.dest, quax)


cfp_parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        add_help=False
        )

cfp_parser.add_argument(
    '--basis',
    required=True,
    choices=["j", "l", "zeeman"],
    help="""Angular momentum basis.
    Zeeman basis only available with --ground."""
)

cfp_parser.add_argument(
    '--ion',
    type=Ion.parse,
    # choices=[Ion.parse('Dy3+')],
    help='Central ion.'
)

space = cfp_parser.add_mutually_exclusive_group(required=False)

space.add_argument(
    '--space',
    nargs='+',
    type=parse_termsymbol,
    help='Symbols of the terms/levels included in the input states.'
)

space.add_argument(
    '--ground',
    action='store_true',
    help='Subset ground term/level prior to projection.'
)

cfp_parser.add_argument(
    '--symbol',
    type=parse_termsymbol,
    help='Symbol of the term/level of interest, e.g. 6H or 6H15/2.'
)

cfp_parser.add_argument(
    '--k_max',
    type=int,
    default=6,
    help='Maximum Stevens operator rank.'
)

cfp_parser.add_argument(
    '--theta',
    action='store_true',
    help='Factor out operator equivalent factors.'
)

cfp_parser.add_argument(
    '--quax',
    action=QuaxAction,
    help='Quantisation axes.'
)

cfp_parser.add_argument(
    '--comp_thresh',
    default=0.05,
    type=float,
    help='Amplitude threshold for composition contribution printing.'
)

cfp_parser.add_argument(
    '--ener_thresh',
    default=1e-7,
    type=float,
    help=('Energy difference threshold for Kramers doublet classification in '
          'zero field. If --ener_thresh and --field are both zero Kramers '
          'doublets are left unperturbed.')
)

cfp_parser.add_argument(
    '--field',
    default=0.0,
    type=float,
    help=('Apply magnetic field (in mT) to split input states. If zero, '
          'Kramers doublets are rotated into eigenstates of Jz.')
)

cfp_parser.add_argument(
    '--verbose',
    action='store_true',
    help='Print out angular momentum matrices and extra information.'
)

def read_args(arg_list=None):

    description = '''
    A package for angular momentum related functionalities.
    '''

    epilog = '''
    Lorem ipsum.
    '''

    parser = ArgumentParser(
            description=description,
            epilog=epilog,
            formatter_class=RawDescriptionHelpFormatter
            )

    subparsers = parser.add_subparsers()

    subparsers.add_parser('cfp', parents=[cfp_parser])

    args = parser.parse_args(arg_list)

    return args

