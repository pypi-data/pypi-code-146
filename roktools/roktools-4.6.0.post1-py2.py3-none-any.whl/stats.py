import argparse
import sys

import numpy as np

def cdf_cli():
    argParser = argparse.ArgumentParser(description= __doc__,
                                        formatter_class=argparse.RawDescriptionHelpFormatter) #without this won't write verbatim

    argParser.add_argument('--n-bins', '-n', metavar='<int>', type=int,
                           help='Number of bins', default=10)

    args = argParser.parse_args()

    samples = []

    for sample in sys.stdin:
        try:
            value = float(sample)
        except ValueError:
            continue

        samples.append(float(sample))

    pdf, edges = np.histogram( samples, bins = args.n_bins, density = True )
    binwidth = edges[1] - edges[0]

    pdf = np.array(pdf) * binwidth
    cdf = np.cumsum(pdf)

    for i in range(args.n_bins):
        print(f"{edges[i]} {pdf[i]} {cdf[i]}")
