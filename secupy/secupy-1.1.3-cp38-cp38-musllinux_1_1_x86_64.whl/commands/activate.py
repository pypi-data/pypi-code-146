import secupy
import requests


def main(args):
    debug = args.verbose
    label = args.label
    token = args.token

    licenser = secupy.SecupyLicenseUtil(debug=debug)
    if licenser.activate_license(token, label):
        print("License activated successfully")
