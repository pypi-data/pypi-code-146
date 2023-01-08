import sys
from argparse import ArgumentParser

from PySide6.QtWidgets import QApplication


def main():
    parser = ArgumentParser(description="GUI application searching for similar images in a set.")
    parser.add_argument('--directories', '-d', nargs='+', default=[])
    parser.add_argument('--no-subdirs', '-ns', action='store_true')
    args = parser.parse_args()

    app = QApplication([])
    # QApplication must be called before using some of qt library elements
    from picture_comparator_muri.controller.application import Application
    application = Application(args)
    application.start()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
