import argparse


class Args:

    @classmethod
    def initialize_args(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument('config', type=str, nargs=1, help='the relevant config section, e.g. local')
        return parser
