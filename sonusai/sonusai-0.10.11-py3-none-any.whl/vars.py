"""sonusai vars

usage: vars [-h]

options:
   -h, --help   Display this help.

List custom SonusAI variables.

"""


def main():
    from docopt import docopt

    import sonusai
    from sonusai.mixture import DEFAULT_NOISE
    from sonusai.utils import trim_docstring

    docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    print('Custom SonusAI variables:')
    print('')
    print(f'  ${{default_noise}}: {DEFAULT_NOISE}')
    print('')


if __name__ == '__main__':
    main()
