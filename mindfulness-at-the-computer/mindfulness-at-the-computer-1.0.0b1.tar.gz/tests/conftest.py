import pytest
from PySide6 import QtGui

import matc.constants
import matc.gui.breathing
import matc.gui.intro_dlg
import matc.gui.modal_dialogs
import matc.gui.settings_dlg
import matc.main_object
import matc.shared
import matc.state


@pytest.fixture
def main_object_started_before(tmp_path, monkeypatch):
    tmp_settings_file_path = tmp_path / "tmp_settings.json"
    matc.state.initiate_state(str(tmp_settings_file_path))

    monkeypatch.setattr(matc.gui.modal_dialogs.UpdateAvailableDlg,
        "check_if_update_available_and_start", lambda: None)

    ret_main_object = matc.main_object.MainObject(False)

    qclipboard = QtGui.QGuiApplication.clipboard()
    qclipboard.clear()
    return ret_main_object


@pytest.fixture
def main_object(tmp_path, monkeypatch):
    tmp_settings_file_path = tmp_path / "tmp_settings.json"

    matc.state.initiate_state(str(tmp_settings_file_path))
    # matc.state.settings[matc.state.SK_MASTER_VOLUME] = 0

    # monkeypatch.setattr(matc.shared, "is_update_available", lambda: False)
    # monkeypatch.setattr(matc.gui.modal_dialogs.UpdateAvailableDlg, "start", lambda: None)
    monkeypatch.setattr(matc.gui.modal_dialogs.UpdateAvailableDlg,
        "check_if_update_available_and_start", lambda: None)

    monkeypatch.setattr(matc.gui.intro_dlg.IntroDlg, "start", lambda *args: None)

    ret_main_object = matc.main_object.MainObject(True)

    # ret_main_object.intro_dlg.close()
    # ret_main_object.br_dlg.close()

    qclipboard = QtGui.QGuiApplication.clipboard()
    qclipboard.clear()
    return ret_main_object


@pytest.fixture
def settings_dlg(qtbot, main_object):
    main_object.setup_settings_dlg()
    ret_settings_dialog = main_object.settings_dlg
    qtbot.addWidget(ret_settings_dialog)
    return ret_settings_dialog


@pytest.fixture
def br_dlg(qtbot, main_object):
    ret_br_dlg = main_object.br_dlg
    qtbot.addWidget(ret_br_dlg)
    return ret_br_dlg


@pytest.fixture(params=[br_vis for br_vis in matc.shared.BrVis], ids=lambda x: x.name)
def br_vis_param(request):
    return request.param


# @pytest.mark.parametrize("br_vis_param", [br_vis_param for br_vis_param in matc.shared.BrVis],
# ids=lambda x: x.name)

"""



***

Pytest plugins:
* pytest-qt - gives the qtbot fixture
  * pytest-qt does not have to be imported
  * qtbot takes care of creating a QApplication (which otherwise we'd have to create ourselves,
    `test_app = QtWidgets.QApplication(sys.argv)`)
  * wraps QtTest/QTest??? (so we don't need `from PySide6.QtTest import QTest`)

Fixtures used:
* qtbot
* tmp_path
We can see all available fixtures using this command: pytest --fixtures

QTest Documentation:
* https://doc.qt.io/qtforpython/PySide6/QtTest/QTest.html
* See also this link https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qttest/qtest.html 
which includes important
functions like mouseClick (which at the time of writing is not included in the previous link above)



We may want to use this:
https://doc.qt.io/qt-6/qstandardpaths.html#setTestModeEnabled

***And perhaps also this:***
https://doc.qt.io/qt-6/qtest.html




Run the automated tests on the different platforms *and installation methods* that are supported:
* Ubuntu
  * 20.04 PIP/PyInstaller
  * 22.04 PIP/PyInstaller
* Windows
  * 10 PIP/PyInstaller
  * 11 ???



IMPORTANT: Even if the qtbot fixture is not used, we have to send it along as a parameter. This 
is because qtbot will initialize the QtApplication, which is needed for many tests. If we don't 
then we can get seemingly a strage error: a test failing when it's run alone but not succeeding 
when other tests have been run before.


### pytest-qt

Reference: https://pytest-qt.readthedocs.io/en/latest/reference.html


### Logging within pytest tests

https://stackoverflow.com/a/51633600/2525237

> About the note that log_cli must be in pytest.ini, it seems you can use -o option to override 
value from command line. pytest -o log_cli=true --log-cli-level=DEBUG works for me.


***

# Unsure why qtbot.mouseClick doesn't work (maybe because we are using a composite widget?)
# qtbot.mouseClick(settings_dialog.columns_bv_option_cw.qrb, QtCore.Qt.LeftButton,
# delay=1000)



class NewVersionContext:
    def __enter__(self):
        self.real_version_text = matc.shared.get_version()
        matc.VERSION = "100.999.000"

    def __exit__(self, exc_type, exc_val, exc_tb):
        matc.VERSION = self.real_version_text
        
with NewVersionContext():
    main_object.check_for_update_action.trigger()


"""

# Happy path testing, then error paths

# TODO: Test not starting first time --- initial state --- using a startup json settings file

# TODO: Test ErrorDlg.on_copy_clicked and ErrorDlg.on_open_log_file_clicked
# TODO: Test exception handling: Uknown exception, KeyboardInterrupt, thrown by user

# TODO: Test changing audio files in the settings. on_file_index_changed

# TODO: Test breathing phrases: remove active, remove last
