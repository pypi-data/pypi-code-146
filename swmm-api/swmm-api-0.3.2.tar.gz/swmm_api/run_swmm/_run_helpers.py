__author__ = "Markus Pichler"
__credits__ = ["Markus Pichler"]
__maintainer__ = "Markus Pichler"
__email__ = "markus.pichler@tugraz.at"
__version__ = "0.1"
__license__ = "MIT"

import os
from swmm_api import SwmmReport


class SWMMRunError(UserWarning):
    pass


def get_result_filenames(inp_fn):
    """
    get filenames for the Report and Output files

    Args:
        inp_fn (str): filename of the Input-Files

    Returns:
        tuple(str, str): filenames for the Report- and Output-file
    """
    return inp_fn.replace('.inp', '.rpt'), inp_fn.replace('.inp', '.out')


def delete_swmm_files(fn_inp, including_inp=False):
    """
    Delete the swmm project files.

    Helpful if you run just a temporary test.

    Args:
        fn_inp (str): filename of the inp-file
        including_inp (bool): if the inp-file should also be deleted.
    """
    fn_rpt, fn_out = get_result_filenames(fn_inp)
    for fn in (fn_out, fn_rpt, (fn_inp if including_inp else None)):
        if fn is not None and os.path.isfile(fn):
            os.remove(fn)


def get_report_errors(fn_rpt):
    if os.path.isfile(fn_rpt):
        rpt = SwmmReport(fn_rpt)
        errors = rpt.get_errors()
        if errors:
            return rpt._pretty_dict(errors)
        else:
            return 'No Errors.'
    else:
        return 'NO Report file created!!!'
