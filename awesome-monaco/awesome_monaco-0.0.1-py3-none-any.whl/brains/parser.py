import argparse


def get_args():
    parser = argparse.ArgumentParser(description="Monaco Racing Task",
                                     epilog="I hope it will be funny")
    parser.add_argument('--files', type=str, required=True, help="Enter your folder path")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--asc', help="direct order", action="store_true")
    group.add_argument('--desc', help="undirected order", action="store_true")
    group.add_argument('--driver', help="driver name", type=str, default=None)
    args = parser.parse_args()
    return args
