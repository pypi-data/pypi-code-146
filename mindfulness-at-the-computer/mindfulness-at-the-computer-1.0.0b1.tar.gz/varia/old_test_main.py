import sys
import unittest

import matc.gui.breathing_phrase_list_wt
import matc.gui.breathing_settings_wt
import matc.gui.rest_action_list_wt
import matc.gui.rest_dlg
import matc.gui.rest_settings_wt
import matc.gui.safe_delete_dlg
import matc.gui.toggle_switch_wt
import matc.gui.toggle_switch_wt
import matc.gui.warning_dlg
from PyQt5 import QtCore
from PyQt5 import QtTest
from PyQt5 import QtWidgets

import matc.gui.breathing
import matc.gui.settings_dlg
import matc.shared

test_app = QtWidgets.QApplication(sys.argv)


# -has to be set here (rather than in __main__) to avoid an error


class MainTest(unittest.TestCase):
    """
    "@unittest.skip" can be used to skip a test
    """

    @classmethod
    def setUpClass(cls):
        matc.shared.testing_bool = True

    def setUp(self):
        pass

    def test_toggle_switch(self):
        ts_widget = matc.gui.toggle_switch_wt.ToggleSwitchWt()
        ts_widget.show()
        ts_widget.turn_on_off_qcb.setChecked(True)

        self.assertTrue(ts_widget.turn_on_off_qcb.isChecked())
        QtTest.QTest.mouseClick(ts_widget.turn_on_off_qcb, QtCore.Qt.LeftButton)
        self.assertFalse(ts_widget.turn_on_off_qcb.isChecked())
        QtTest.QTest.mouseClick(ts_widget.turn_on_off_qcb, QtCore.Qt.LeftButton)

    def test_main_window(self):
        main_window = matc.gui.settings_win.SettingsDlg()

    def test_breathing_dialog(self):
        matc.shared.active_phrase_id = 1
        breathing_dialog = matc.gui.breathing_dlg.BreathingGraphicsView()

    def test_reminder_settings_dock(self):
        breathing_reminder_settings = matc.gui.breathing_settings_wt.BreathingSettingsWt()

    def test_rest_action_list_dock(self):
        rest_action_list = matc.gui.rest_action_list_wt.RestActionListWt()

    def test_rest_reminder_settings_dock(self):
        rest_reminder_settings = matc.gui.rest_settings_wt.RestSettingsWt()

    def test_rest_dialog(self):
        rest_dialog = matc.gui.rest_dlg.BreathingDlg()

    def test_safe_delete_dialog(self):
        safe_delete_dialog = matc.gui.safe_delete_dlg.SafeDeleteDlg("testing")
        # self.assertTrue(safe_delete_dialog.show.isVisible())
        # self.assertTrue(safe_delete_dialog.description_qll.isVisibleTo(safe_delete_dialog))
        # self.assertTrue(safe_delete_dialog.isVisibleTo(None))
        ok_dialog_button = safe_delete_dialog.button_box.button(QtWidgets.QDialogButtonBox.Ok)
        QtTest.QTest.mouseClick(ok_dialog_button, QtCore.Qt.LeftButton)
        # self.assertFalse(safe_delete_dialog.isVisible())
        QtWidgets.QApplication.processEvents()
        # self.assertFalse(safe_delete_dialog.description_qll.isVisibleTo(safe_delete_dialog))

    def test_add_dlg(self):
        add_dlg = matc.gui.warning_dlg.WarningDlg("testing")
        ok_dialog_button = add_dlg.button_box.button(QtWidgets.QDialogButtonBox.Ok)
        QtTest.QTest.mouseClick(ok_dialog_button, QtCore.Qt.LeftButton)
        QtWidgets.QApplication.processEvents()

    """
    def test_starting_breathing(self):
        main_win_widget = matc.gui.main_win.MbMainWindow()
        main_win_widget.menu_bar.
    """


if __name__ == "__main__":
    unittest.main()

"""
def __init__(self, *args, **kwargs):
    super(MainTest, self).__init__(*args, **kwargs)
    # -https://stackoverflow.com/questions/17353213/init-for-unittest-testcase

pl_widget.list_widget.itemWidget()

Things to test:
*


        QtCore.QCoreApplication.processEvents()
        QtWidgets.QApplication.processEvents()  # <-------------------
        QtTest.QTest.qWait(3000)
        res_bl = self.click_on_list_widget_entry(pl_widget.list_widget, TEXT_FOR_ENTRY_TO_CLICK_STR)
        if not res_bl:
            self.fail()

    def test_take_a_break_now(self):
        take_break_qpb = self.matc_main_obj.main_window.rest_settings_widget.rest_reminder_test_qpb
        rr_dlg = self.matc_main_obj.main_window.rest_reminder_dialog
        QtTest.QTest.mouseClick(take_break_qpb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseClick(rr_dlg.close_qpb, QtCore.Qt.LeftButton)


"""
