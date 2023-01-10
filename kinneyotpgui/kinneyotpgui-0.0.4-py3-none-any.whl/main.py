#!/usr/bin/env python3
"""User interface for one time passwords"""

import sys

from PySide6.QtWidgets import QApplication, QDialog

import kinneyotpgui.form

def main():
    """Main loop"""

    # Create the Qt Application
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    app.setApplicationName("One Time Pad")

    # Create and show the form
    form = kinneyotpgui.form.Form()
    form.show()

    retval = form.exec()
    if retval == QDialog.Rejected:
        main()

if __name__ == '__main__':
    main()
