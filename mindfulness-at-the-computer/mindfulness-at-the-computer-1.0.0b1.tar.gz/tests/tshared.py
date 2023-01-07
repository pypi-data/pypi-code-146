from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

import matc.shared

MANUAL_TEST_CASE_NOT_YET_COMPLETE = "Manual test case, not yet complete"
MANUAL_TEST_CASE = "Manual test case"
"""
Steps to follow:
Expected result:
Where to report result:

"""


def compare_icons(i_icon: QtGui.QIcon, i_dot_shown: bool):
    cmp_path = matc.shared.get_app_icon_path(i_dot_shown)
    # cmp_pixmap = QtGui.QPixmap("cmp_path")
    cmp_icon = QtGui.QIcon(cmp_path)
    side: int = 22
    shared_qs = QtCore.QSize(side, side)
    st_pixmap = i_icon.pixmap(shared_qs)
    cmp_pixmap = cmp_icon.pixmap(shared_qs)
    # st_cache = systray_icon.cacheKey()
    # cmp_cache = cmp_icon.cacheKey()
    for i in range(0, side):
        for j in range(0, side):
            if st_pixmap.toImage().pixel(i, j) != cmp_pixmap.toImage().pixel(i, j):
                return False
    return True


def get_close_button_from_button_box(
        i_button_box: QtWidgets.QDialogButtonBox) -> QtWidgets.QPushButton:
    for btn in i_button_box.buttons():
        btn: QtWidgets.QPushButton
        if "Close" in btn.text():
            return btn
    pytest.fail("Failed to find button in dialog button box")


def get_widget_by_text(i_base_widget: QtWidgets.QWidget, i_text: str) -> QtWidgets.QWidget:
    for w in i_base_widget.children():
        w: QtWidgets.QWidget
        if i_text in w.text():
            return w
    pytest.fail("Failed to find widget")
