import secupy
import requests


def main(args):
    debug = args.verbose

    secupy.SecupyCryptoUtil(debug=debug)
