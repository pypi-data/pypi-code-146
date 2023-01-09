#!python

import argparse, sys, itertools
import pandas as pd
import numpy as np
from shiftES.shiftes import effectsize, effectsize_ci

def _load_table(fn, filetype, has_header=True, sheet=0):
    """Load table using arguments given at command line.
    Headerless tables will have header made up of string integers
    starting from one, as the CL args assume one indexed and are str by default."""

    valid_types = ('a', 'c', 't', 'x')
    if filetype not in valid_types:
        raise ValueError(f"{filetype} not a valid file type token, use one of {', '.join(valid_types)}")

    # autodetect filetype
    if filetype=='a':
        lowfn = fn.lower()
        if lowfn.endswith('.tsv') or lowfn.endswith('.txt'):
            filetype = 't'
        elif lowfn.endswith('.csv'):
            filetype = 'c'
        elif lowfn.endwith('.xlsx'):
            filetype = 'x'
        else:
            raise ValueError(f"Couldn't automatically detect type of file, {fn}")

    # passed to pandas header option
    header = [None, 0][has_header]

    if filetype in 'ct':
        sep = dict(c=',', t='\t')[filetype]
        table = pd.read_csv(fn, sep=sep, header=header)
    elif filetype == 'x':
        sheet = int(sheet)
        table = pd.read_excel(fn, header=header, sheet_name=sheet)
    # the else is covered above, no other values should make it this far

    if not has_header:
        table.columns = table.columns.map(lambda x: str(int(x)+1))

    return table


def list_column_pairs(table, colA, colB):
    if (colA == 'ALL') and (colB == 'ALL'):
        cols = table.columns
        cols = cols[~table.columns.str.startswith('Unnamed:')]
        column_pairs = list(itertools.combinations(cols, 2))
    else:
        column_pairs = list(
            [ab for ab in zip(colA.split(','), colB.split(','), )]
        )

    return column_pairs

def run_from_cmdline(args):
    colA, colB = args.columnA, args.columnB

    table = _load_table(
        fn=args.file,
        filetype=args.type,
        has_header=(not args.no_header),
        sheet=int(args.sheet_number)-1,
    )

    column_pairs = list_column_pairs(table, colA, colB)
    if args.no_header:
        column_pairs = [(ab[0], ab[1]) for ab in column_pairs]
        aw, bw = 3, 3
    else:
        # for printing, width of largest sample name
        widths = [1, 1]
        for pair in column_pairs:
            for i in (0, 1):
                l = len(pair[i])
                if l > widths[i]:
                    widths[i] = l
        aw, bw = widths

    if args.ci:
        results = [('S1', 'S2', 'Omega', 'Lower 95% CI', 'Upper 95% CI')]
    else:
        results = [('S1', 'S2', 'Omega')]

    for k1, k2 in column_pairs:
        X1, X2 = table[k1], table[k2]

        # produce formatable string with word widths written in
        if args.ci:
            stats = effectsize_ci(X1, X2)
            fstr = f"{{:>{aw}}} : {{:<{bw}}} {{: .3}} [{{: .3}} {{: .3}}]"

        else:
            stats = (effectsize(X1, X2),)
            fstr = f"{{:>{aw}}} : {{:<{bw}}} {{: .3}}"

        print(fstr.format(k1, k2, *stats))
        results.append((k1,k2, *stats))

    if args.output:
        results = pd.DataFrame(results)
        fn = args.output
        kwargs = dict(index=False, header=False)
        if fn.endswith('.tsv') or fn.endswith('.txt'):
            results.to_csv(fn, sep='\t', **kwargs)
        elif fn.lower().endswith('.xlsx'):
            results.to_excel(fn, **kwargs)
        else:
            results.to_csv(fn, **kwargs)


def parse_args(cmdline_args):

    parser = argparse.ArgumentParser(
        description=(
            "Calculate robust nonparametric effect size, described by R. Wilcox, "
            "https://dx.doi.org/10.22237/jmasm/1551905677\n\n"
            "Guide to effect sizes (equiv to Cohen's d small/medium/large):\n"
                "\t|Ω|: small 0.1; medium 0.3; large 0.4\n"
        )
    )

    parser.add_argument(
        'file',
        help='Path of input file, an CSV (comma or tab sep) or Excel file.',
    )
    parser.add_argument(
        'columnA', metavar="list,of,columns", type=str,
        help="Name(s) of column (if file has headers) or number(s) of first column(s) containing data to be tested. "
             "Column numbers are 1-indexed. Putting 'ALL' for both columnA/B will test every pair of ",
    )
    parser.add_argument(
        'columnB', metavar="list,of,columns", type=str,
        help="Name of column/number of second column.",
    )
    parser.add_argument(
        '-o', '--output', default=None,
        help="File to write the results to, if none just prints"
    )
    parser.add_argument(
        '-c', '--ci',default=False,
        action='store_true',
        help="Set flag to calculate confidence intervals using the bootstrap method. Use -b to change"
             " number of boostrap iterations (default: 500)"
    )
    parser.add_argument(
        '-b', '--nboot', type=int, default=500,
        help="Change number of bootstrap iterations when calculating confidence intervals. Default: 500."
    )
    parser.add_argument(
        '-t', '--type', default='a',
        help="Input file type, default 'a' for autodetect, 'c' for comma-separated-values, 't' for tab-sep-vals, "
             "'x' for .xlsx . If 'a' the script will guess based on the file name."
    )
    parser.add_argument(
        '-n', '--no-header',
        action='store_true',
        default=False,
        help="Set to indicate that first row contains data and columns will give numerical position."
    )
    parser.add_argument(
        '--sheet-number', default=1,
        help="Excel only: if the sheet is not the first one, give its position here. 1-indexed"
    )

    return parser.parse_args(cmdline_args)

if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    run_from_cmdline(args)