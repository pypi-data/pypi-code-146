#! /usr/bin/env python
# Copyright 2020 Uwe Schmitt <uwe.schmitt@id.ethz.ch>


def main():
    from . import patch_all  # noqa F401 isort: skip
    from spyder.app.start import main

    main()


if __name__ == "__main__":
    main()
